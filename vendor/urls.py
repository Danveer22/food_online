from django.urls import path, include
from .import views
from accounts import views as AccountViews

urlpatterns = [
  path('', AccountViews.restaurantDashboard, name='vendor'),
  path('profile/', views.vprofile, name='vprofile'),
  path('menu-builder/', views.menu_builder, name='menu_builder'),
  path('menu-builder/category/<int:pk>/', views.foodCategory, name='foodCategory'),
  path('menu-builder/category/add/', views.add_category, name='add_category'),
  path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
  path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
]
