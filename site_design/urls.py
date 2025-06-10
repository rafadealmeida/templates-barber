from django.urls import path
from site_design.views import index


urlpatterns = [
    path('', index,name='index'),
]