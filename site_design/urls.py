from django.urls import path,include
from site_design.views import index


urlpatterns = [
    path('', index,name='index'),
    path("external/", include("integration_api.urls")),
]