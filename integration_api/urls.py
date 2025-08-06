from django.urls import path
from .views import ExternalAdminUserCreateView

urlpatterns = [
    path("admin-users/", ExternalAdminUserCreateView.as_view(), name="external-admin-create"),
]
