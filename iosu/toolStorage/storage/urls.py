from django.urls import path
from django.contrib.auth import views as auth_views

from .views import views, admin, ajax

urlpatterns = [
    path('', views.index, name='index'),
    path('employee/', views.employee, name='employee'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # documents
    path('documents/created-products-during-dates/', views.docs_created_products_during_dates, name='docs-created-products-during-dates'),

    # ajax
    path('ajax/finish-production/', ajax.finish_production, name='ajax-finish-production'),
    path('ajax/service-equipment/', ajax.service_equipment, name='ajax-service-equipment'),
]
