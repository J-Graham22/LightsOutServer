from django.urls import path
from . import views

urlpatterns = [
    path('lights_out_solver', views.lights_out_solver, name='lights_out_solver'),
]