from django.urls import path
from . import views 

urlpatterns = [
    path('login_admin/', views.login_admin, name='login_admin'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_rooms/', views.manage_rooms, name='manage_rooms'),
    path('manage_guests/', views.manage_guests, name='manage_guests'),
    path('add_guest/', views.add_guest, name='add_guest'),
    path('add_room/', views.add_room, name='add_room'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
    path('login/', views.login, name='login')
]