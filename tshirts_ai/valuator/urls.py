from django.urls import path
from django.urls import re_path
from . import views

app_name = 'valuator'

urlpatterns = [
    path('', views.index, name='index'),
    path('valuate/', views.valuate, name='valuate'),
    path('save_result/', views.save_result, name='save_result'),
    re_path(r'valuate/(?P<tshirt_id>[0-9]+)/$', views.tshirt_detail,
        name="tshirt_detail")
]
