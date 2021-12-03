from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('delete/', views.delete),
    path('update/', views.update),
    path('timer/', views.timer)
]