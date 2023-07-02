from django.urls import path, include
from .import views


urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('customerDashboard/', views.customerDashboard, name="customerDashboard"),
    path('restaurantDashboard/', views.restaurantDashboard, name="restaurantDashboard"),
    path('myAccount/', views.myAccount, name="myAccount"),

]