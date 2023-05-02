from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name="home"),
    path('recepis/category/<int:category_id>/',
         views.category, name="category"),
    path('recepis/<int:id>/', views.recipe, name="recipe"),


]
