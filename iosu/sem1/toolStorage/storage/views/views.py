from functools import wraps

from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.core.management import call_command
from django.db import connection, reset_queries
from django.db.models import Count, Max, Value, CharField, F, Sum, Case, When, IntegerField
from django.db.models.functions import Concat, Cast, ExtractMonth
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse

from storage.models import *
from storage.forms import LoginForm, CreateEmployeeForm


def log_queries(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        reset_queries()
        response = view_func(*args, **kwargs)
        queries = connection.queries
        # for query in queries:
        #     print(query['sql'])
        return response
    return wrapper


@log_queries
def index(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = authenticate(request, username=username, password=password)
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Неверный логин или пароль')
        else:
            if user:
                login(request, user)
                return redirect('employee')
            else:
                messages.add_message(request, messages.ERROR, 'Неверный логин или пароль')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'index.html', context)


@log_queries
def employee(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Необходимо авторизоваться')
        return redirect('index')

    responsible_equipment = Equipment.objects.filter(responsible_employee=request.user.employee).select_related('type')
    responsible_production = (Production.objects
                              .filter(technological_map__equipment__responsible_employee=request.user.employee)
                              .select_related('technological_map', 'technological_map__product')
                              .order_by('-start_date'))

    context = {
        'responsible_equipment': responsible_equipment,
        'responsible_production': responsible_production,
    }
    if request.user.is_superuser:
        if request.method == 'POST':
            create_employee_form = CreateEmployeeForm(request.POST)
            if create_employee_form.is_valid():
                try:
                    user = User.objects.create_user(
                        username=request.POST.get('username'),
                        password=request.POST.get('password'),
                    )
                    employee = Employee.objects.create(
                        user=user,
                        first_name=create_employee_form.cleaned_data.get('first_name'),
                        last_name=create_employee_form.cleaned_data.get('last_name'),
                        middle_name=create_employee_form.cleaned_data.get('middle_name'),
                        gender=create_employee_form.cleaned_data.get('gender'),
                        position=create_employee_form.cleaned_data.get('position'),
                    )
                except Exception as e:
                    messages.add_message(request, messages.ERROR, e)
                else:
                    messages.add_message(request, messages.SUCCESS, 'Сотрудник добавлен')
                    return redirect('employee')
        else:
            create_employee_form = CreateEmployeeForm()

        # Queries

        high_usable_tool = Tools.objects.annotate(
            usage_count=Count('technologicalmapstools__technological_map__production')
        ).filter(usage_count__gt=0).order_by('wear_degree').first()

        unique_tools_num_for_equipment = Equipment.objects.annotate(
            unique_tools_count=Count('technologicalmap__technologicalmapstools__tools', distinct=True)
        ).order_by('-unique_tools_count')

        high_wear_tools = Tools.objects.filter(wear_degree__lt=1000).order_by('wear_degree')[:5]

        tools = Tools.objects.all()
        tool_annotations = dict((f'tool_{tool.pk}', Sum(
            Case(
                When(
                    technologicalmap__tools=tool,
                    then=F('technologicalmap__technologicalmapstools__number_of_required_tools')
                ),
                default=0,
                output_field=IntegerField()
            )
        )) for tool in Tools.objects.all())
        turning_equipment_with_used_tools = Equipment.objects.select_related('type').annotate(
            **tool_annotations
        ).filter(type=1)

        production_for_turning_equipment = Production.objects.filter(
            technological_map__equipment__type_id=1
        ).annotate(
            month=ExtractMonth('start_date')
        ).values('month').annotate(
            total_products=Count('id')
        )

        equipment_union_tools = Equipment.objects.annotate(
            type_name=Value('Оборудование', output_field=CharField())
        ).annotate(
            display_name=Cast('name', CharField())
        ).values('type_name', 'display_name').union(
            Tools.objects.annotate(
                type_name=Value('Инструмент', output_field=CharField())
            ).annotate(
                display_name=Concat('name', Value(' - '), 'wear_degree', Value(', '), 'total_amount', Value(' шт.'), output_field=CharField())
            ).values('type_name', 'display_name'),
            all=True
        )

        equipment_with_tools_extra = Equipment.objects.prefetch_related(
            models.Prefetch(
                'technologicalmap_set',
                queryset=TechnologicalMap.objects.prefetch_related(
                    models.Prefetch(
                        'technologicalmapstools_set',
                        queryset=TechnologicalMapsTools.objects.select_related('tools')
                    )
                )
            )
        )

        context.update({
            'employees': Employee.objects.select_related('position').all(),
            'create_employee_form': create_employee_form,
            # Queries
            'high_usable_tool': high_usable_tool,
            'unique_tools_num_for_equipment': unique_tools_num_for_equipment,
            'high_wear_tools': high_wear_tools,
            'turning_equipment_with_used_tools': turning_equipment_with_used_tools,
            'tools': tools,
            'production_for_turning_equipment': production_for_turning_equipment,
            'equipment_union_tools': equipment_union_tools,
            'equipment_with_tools_extra': equipment_with_tools_extra,
            # Database
            'models': [model.__name__ for model in apps.get_app_config('storage').get_models()],
        })

        return render(request, 'admins_page.html', context)
    else:
        return render(request, 'workers_page.html', context)


def docs_created_products_during_dates(request):
    from_date_param = request.GET.get('from')
    to_date_param = request.GET.get('to')

    if from_date_param and to_date_param:
        from_date = timezone.datetime.strptime(from_date_param, "%Y-%m-%d")
        to_date = timezone.datetime.strptime(to_date_param, "%Y-%m-%d")

        production_list = Production.objects.select_related('technological_map', 'technological_map__product').filter(
            start_date__range=[from_date, to_date]
        )
    else:
        messages.add_message(request, messages.ERROR, 'Неверно указаны даты')
        production_list = from_date = to_date = ''

    context = {
        'production_list': production_list,
        'from_date': from_date,
        'to_date': to_date,
    }
    return render(request, 'documents/created_products_during_dates.html', context)


def add_field(request):
    field_types = {
        'str': models.CharField(max_length=100, null=True, blank=True, default=None),
        'int': models.IntegerField(null=True, blank=True, default=None),
        'bool': models.BooleanField(null=True, blank=True, default=None),
    }
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        field_type = field_types['str']  # request.POST.get('field_type')
        table_name = request.POST.get('table_name')
        try:
            table = globals()[table_name]
            table._meta.get_field(field_name)
            messages.error(request, f"Поле '{field_name}' уже существует в таблице '{table_name}'.")
        except FieldDoesNotExist:
            table.add_to_class(field_name, field_type)
            messages.success(request, f"Поле '{field_name}' успешно добавлено в таблицу '{table_name}'.")
            call_command('makemigrations', 'storage')
            call_command('migrate')
            messages.success(request, 'Миграции применены.')

    return redirect(f"{reverse('employee')}#database")


def remove_field(request):
    from django.db import DEFAULT_DB_ALIAS, connections
    from django.db.utils import OperationalError

    response = redirect(f"{reverse('employee')}#database")
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        table_name = request.POST.get('table_name')

        try:
            table = globals()[table_name]
            field = table._meta.get_field(field_name)
        except FieldDoesNotExist:
            messages.error(request, f"Поле '{field_name}' не существует в таблице '{table_name}'.")
            return response

        try:
            with connections[DEFAULT_DB_ALIAS].schema_editor() as schema_editor:
                schema_editor.remove_field(table, field)
            messages.success(request, f"Поле '{field_name}' успешно удалено из таблицы '{table_name}'.")
            call_command('makemigrations', 'storage')
            call_command('migrate')
            messages.success(request, 'Миграции применены.')
        except OperationalError:
            messages.error(request, 'Ошибка при удалении поля из БД.')
            return response

    return response
