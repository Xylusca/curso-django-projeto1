from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('recepis/<int:id>/', views.recipe),


]
