from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from exhibitions import views


urlpatterns = [
    path('', views.index, name='index'),
    path('document/<int:rent_id>', views.print_document, name='document'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
]
