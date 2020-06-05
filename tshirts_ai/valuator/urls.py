from django.urls import path
from . import views

app_name = 'valuator'

urlpatterns = [
    path('', views.index, name='index'),
    path('valuate/', views.valuate, name='valuate'),
]
