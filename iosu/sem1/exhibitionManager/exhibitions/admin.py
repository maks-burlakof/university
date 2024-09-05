from django.contrib import admin, messages

from .models import *


admin.site.site_header = 'Выставка продукции'
admin.site.site_title = 'Админ-панель'
admin.site.index_title = ''


class ModelAdmin(admin.ModelAdmin):
    change_list_template = 'change_list.html'

    def changelist_view(self, request, extra_context=None):
        from django.db.models.fields import Field, BigAutoField
        from django.core.exceptions import FieldDoesNotExist
        from django.core.management import call_command
        from io import StringIO
        from django.db import DEFAULT_DB_ALIAS, connections
        from django.db.utils import OperationalError

        field_types = {
            'str': models.CharField(max_length=100, null=True, blank=True, default=None),
            'int': models.IntegerField(null=True, blank=True, default=None),
            'bool': models.BooleanField(null=True, blank=True, default=None),
            'datetime': models.DateTimeField(null=True, blank=True, default=None),
        }

        def validate_post():
            if not request.POST.get('db_field'):
                messages.add_message(request, messages.ERROR, 'Укажите название поля')
                return False
            if request.POST.get('db_field_type') is not None and not field_types.get(request.POST.get('db_field_type')):
                messages.add_message(request, messages.ERROR, 'Укажите тип поля')
                return False
            return True

        if request.POST and request.POST.get('db_action') and validate_post():
            field_name = request.POST.get('db_field')

            if request.POST.get('db_action') == 'add':
                try:
                    self.model._meta.get_field(field_name)
                    messages.error(request, f"Поле '{field_name}' уже существует в таблице.")
                except FieldDoesNotExist:
                    field_type = field_types.get(request.POST.get('db_field_type'))
                    self.model.add_to_class(field_name, field_type)
                    messages.success(request, f"Поле '{field_name}' успешно добавлено в таблицу.")
                    with StringIO() as out:
                        call_command('makemigrations', 'exhibitions', stdout=out)
                        call_command('migrate', stdout=out)
                        print('Apply migrations: ', out.getvalue())
                        messages.success(request, f'{out.getvalue()}')

            elif request.POST.get('db_action') == 'delete':
                try:
                    field = self.model._meta.get_field(field_name)
                except FieldDoesNotExist:
                    messages.error(request, f"Поле '{field_name}' не существует в таблице.")
                else:
                    try:
                        with connections[DEFAULT_DB_ALIAS].schema_editor() as schema_editor:
                            schema_editor.remove_field(self.model, field)
                        messages.success(request, f"Поле '{field_name}' успешно удалено из таблицы.")
                        with StringIO() as out:
                            call_command('makemigrations', 'exhibitions', stdout=out)
                            call_command('migrate', stdout=out)
                            print('Apply migrations: ', out.getvalue())
                            messages.success(request, f'{out.getvalue()}')
                    except OperationalError:
                        messages.error(request, 'Ошибка при удалении поля из БД.')

        fields = [field for field in self.model._meta.get_fields() if isinstance(field, Field) and not isinstance(field, BigAutoField)]

        extra_context = {
            'fields': fields,
            'field_types': field_types,
            **(extra_context or {}),
        }
        return super(ModelAdmin, self).changelist_view(request, extra_context=extra_context)


@admin.register(Exhibition)
class ExhibitionAdmin(ModelAdmin):
    list_display = ('__str__', 'start_date', 'end_date')


@admin.register(ExhibitionPlace)
class ExhibitionPlaceAdmin(ModelAdmin):
    list_filter = ('exhibition',)
    list_display = ('__str__', 'exhibition')
    ordering = ('exhibition', 'number')
    pass


class ProductsInline(admin.StackedInline):
    model = Products
    readonly_fields = ('name', 'amount', 'price')
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'address', 'email')
    list_display_links = ('id', '__str__')
    inlines = (ProductsInline,)


@admin.register(ParticipationExhibition)
class ParticipationExhibitionAdmin(ModelAdmin):
    pass


@admin.register(RentExhibitionPlace)
class RentExhibitionPlaceAdmin(ModelAdmin):
    list_display = ('__str__', 'start_date', 'end_date')
    pass


@admin.register(Products)
class ProductsAdmin(ModelAdmin):
    list_display = ('__str__', 'amount', 'price', 'company')
    pass


@admin.register(AdvertisementType)
class AdvertisementTypeAdmin(ModelAdmin):
    pass


@admin.register(Advertisement)
class AdvertisementAdmin(ModelAdmin):
    list_display = ('__str__', 'start_date', 'end_date', 'price')


class VisitorsTicketsInline(admin.TabularInline):
    model = VisitorsTickets
    extra = 0
    can_delete = True


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    inlines = (VisitorsTicketsInline,)


@admin.register(Visitor)
class VisitorAdmin(ModelAdmin):
    list_display = ('__str__', 'phone', 'email')
    inlines = (VisitorsTicketsInline,)


@admin.register(VisitorsTickets)
class VisitorsTicketsAdmin(ModelAdmin):
    list_display = ('__str__', 'purchase_date')
