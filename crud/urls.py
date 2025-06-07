from django.urls import path
from . import views 

urlpatterns = [
    path('login_admin/', views.login_admin, name='login_admin'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_rooms/', views.manage_rooms, name='manage_rooms'),
    path('manage_guests/', views.manage_guests, name='manage_guests'),
    path('add_guest/', views.add_guest, name='add_guest'),
    path('book_guest/', views.book_guest, name='book_guest'),
    path('add_room/', views.add_room, name='add_room'),
    path('edit_room/<int:room_id>/', views.edit_room, name='edit_room'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('delete_guest/<int:guest_id>/', views.delete_guest, name='delete_guest'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
    path('login/', views.login, name='login'),
    path('pricing/', views.pricing, name='pricing'),
    path('set_price/', views.set_price, name='set_price'),
    path('edit_guest/<int:guest_id>/', views.edit_guest, name='edit_guest'),
    path('add_admin/', views.add_admin, name='add_admin'),
    path('manage_admin/', views.manage_admin, name='manage_admin'),
    path('edit_admin/<int:admin_id>/', views.edit_admin, name='edit_admin'),
    path('delete_admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
]