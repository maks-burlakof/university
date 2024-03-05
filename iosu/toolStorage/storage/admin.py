from django.contrib import admin

from .models import *


admin.site.site_header = 'ToolLand'
admin.site.site_title = 'ToolLand админ-панель'
admin.site.index_title = ''


class EmployeeInline(admin.StackedInline):
    model = Employee
    readonly_fields = ('user', 'first_name', 'last_name', 'middle_name', 'gender')
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(JobPosition)
class JobPositionAdmin (admin.ModelAdmin):
    inlines = (EmployeeInline,)


@admin.register(Employee)
class EmployeeAdmin (admin.ModelAdmin):
    list_display = ('__str__', 'position')


class TechnologicalMapsInline(admin.StackedInline):
    model = TechnologicalMap
    readonly_fields = ('number', 'equipment')
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(Product)
class ProductAdmin (admin.ModelAdmin):
    list_display = ('__str__', 'average_production_time')
    inlines = (TechnologicalMapsInline,)


@admin.register(EquipmentType)
class EquipmentTypeAdmin (admin.ModelAdmin):
    pass


@admin.register(Equipment)
class EquipmentAdmin (admin.ModelAdmin):
    list_display = ('name', 'type', 'responsible_employee', 'date_of_last_service')
    list_editable = ('date_of_last_service',)
    list_filter = ('responsible_employee',)


@admin.register(Tools)
class ToolsAdmin (admin.ModelAdmin):
    list_display = ('__str__', 'total_amount', 'wear_degree')
    list_editable = ('total_amount',)


class TechnologicalMapsToolsInline(admin.TabularInline):
    model = TechnologicalMapsTools


@admin.register(TechnologicalMap)
class TechnologicalMapAdmin (admin.ModelAdmin):
    list_display = ('__str__', 'product')
    inlines = (TechnologicalMapsToolsInline,)


# @admin.register(TechnologicalMapsTools)
# class TechnologicalMapsToolsAdmin (admin.ModelAdmin):
#     pass


@admin.register(Production)
class ProductionAdmin (admin.ModelAdmin):
    list_display = ('__str__', 'is_finished', 'start_date', 'end_date', 'time_efficiency', 'number_of_required_products', 'number_of_defects', 'amount_efficiency')
    readonly_fields = ('is_finished',)
