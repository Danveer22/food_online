from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('customerDashboard/', views.customerDashboard, name="customerDashboard"),
    path('restaurantDashboard/', views.restaurantDashboard, name="restaurantDashboard"),
    path('myAccount/', views.myAccount, name="myAccount"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('vendor/', include('vendor.urls')),
    path('customer/', include('customers.urls')),

]