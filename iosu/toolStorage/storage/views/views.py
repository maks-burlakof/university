from functools import wraps

from django.db import connection, reset_queries
from django.db.models import Count, F
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from storage.models import *
from storage.forms import LoginForm, CreateEmployeeForm


def log_queries(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        reset_queries()
        response = view_func(*args, **kwargs)
        queries = connection.queries
        for query in queries:
            print(query['sql'])
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

        high_usable_tools = Tools.objects.annotate(
            usage_count=Count('technologicalmapstools__technological_map__production')
        ).filter(usage_count__gt=0).order_by('-usage_count')[:5]

        unique_tools_num_for_equipment = Equipment.objects.annotate(
            unique_tools_count=Count('technologicalmap__technologicalmapstools__tools', distinct=True)
        ).order_by('-unique_tools_count')

        high_wear_tools = Tools.objects.filter(wear_degree__lt=1000).order_by('wear_degree')[:5]

        tools_for_turning_equipment = Tools.objects.filter(
            technologicalmapstools__technological_map__equipment__type_id=1
        ).distinct()

        equipment_with_tools = Equipment.objects.prefetch_related(
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
            'high_usable_tools': high_usable_tools,
            'unique_tools_num_for_equipment': unique_tools_num_for_equipment,
            'high_wear_tools': high_wear_tools,
            'tools_for_turning_equipment': tools_for_turning_equipment,
            'equipment_with_tools': equipment_with_tools,
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
