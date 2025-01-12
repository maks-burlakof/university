from core_app.views import HealthCheckView
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("healthcheck", HealthCheckView.as_view(), name="healthcheck"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
