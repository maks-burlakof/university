from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models.fields import Field, BigAutoField

from storage.models import *


@csrf_exempt
@login_required
def finish_production(request):
    production_pk = request.POST.get('productionId')
    number_of_defects = request.POST.get('numOfDefects')
    is_success = False
    message = ''
    try:
        production = Production.objects.get(pk=production_pk)
        if production.technological_map.equipment.responsible_employee == request.user.employee:
            if not production.is_finished:
                production.end_date = timezone.now()
                production.number_of_defects = number_of_defects if number_of_defects else 0
                production.save()
                is_success = True
            else:
                message = 'Production object already marked as finished'
        else:
            message = 'You are not responsible employee for this equipment and production'
    except Exception as e:
        message = str(e)

    response = {
        'is_success': is_success,
        'message': message,
    }
    return JsonResponse(response)


@csrf_exempt
@login_required
def service_equipment(request):
    equipment_pk = request.POST.get('equipmentId')
    is_success = False
    message = ''
    try:
        equipment = Equipment.objects.get(pk=equipment_pk)
        if equipment.responsible_employee == request.user.employee:
            equipment.date_of_last_service = timezone.now()
            equipment.save()
            is_success = True
        else:
            message = 'You are not responsible employee for this equipment'
    except Exception as e:
        message = str(e)

    response = {
        'is_success': is_success,
        'message': message,
    }
    return JsonResponse(response)


@csrf_exempt
@login_required
def get_model_fields(request):
    model = request.GET.get('model')
    is_success = False
    message = ''
    editable_fields = []
    try:
        all_fields = globals()[model]._meta.get_fields()
        for field in all_fields:
            if isinstance(field, Field) and not isinstance(field, BigAutoField):
                editable_fields.append(field.name)
        is_success = True
    except Exception as e:
        message = str(e)

    response = {
        'is_success': is_success,
        'message': message,
        'fields': editable_fields,
    }
    return JsonResponse(response)
