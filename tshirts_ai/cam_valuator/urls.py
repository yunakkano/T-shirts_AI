from django.urls import path
from . import views

app_name = 'cam_valuator'

urlpatterns = [
    path('', views.index, name='index'),
    path('cam_valuate/', views.cam_valuate, name='cam_valuate'),
    path('save_result/', views.save_result, name='save_result')
]
