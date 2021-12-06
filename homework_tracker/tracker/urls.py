from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('delete/', views.delete),
    path('update/', views.update),
    path('timer/', views.timer),
    path('update-timer/', views.update_timer),
    path('delete-timer/', views.delete_timer),
    path('time-dashboard/', views.time_dashboard),
    path('task-dashboard/', views.task_dashboard)
]