from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Public URLs (accessible to everyone)
    path('', views.nova_hotel, name='nova_hotel'),  # Main entry point
    path('nova_hotel/', views.nova_hotel, name='nova_hotel'),  # Alternative route
    path('register/', views.register, name='register'),
    path('guest/login/', views.guest_login, name='guest_login'),
    
    # Guest URLs (protected by guest_login_required)
    path('guest/account/', views.guest_account, name='guest_account'),
    path('guest/logout/', views.guest_logout, name='guest_logout'),
    path('guest/booking/', views.booking_web, name='booking_web'),
    path('guest/change-password/', views.guest_change_password, name='guest_change_password'),
    path('guest/process-payment/', views.process_payment, name='process_payment'),
    path('guest/confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('check-room-availability/<str:room_type>/<str:room_number>/', views.check_room_availability, name='check_room_availability'),
    
    # Admin URLs (protected by login_required)
    path('login_admin/', views.login_admin, name='login_admin'),
    path('logout_admin/', login_required(views.logout_admin), name='logout_admin'),
    path('admin_dashboard/', login_required(views.admin_dashboard), name='admin_dashboard'),
    path('manage_rooms/', login_required(views.manage_rooms), name='manage_rooms'),
    path('manage_guests/', login_required(views.manage_guests), name='manage_guests'),
    path('add_room/', login_required(views.add_room), name='add_room'),
    path('edit_room/<int:room_id>/', login_required(views.edit_room), name='edit_room'),
    path('delete_room/<int:room_id>/', login_required(views.delete_room), name='delete_room'),
    path('add_guest/', login_required(views.add_guest), name='add_guest'),
    path('edit_guest/<int:booking_id>/', login_required(views.edit_guest), name='edit_guest'),
    path('check_out/<int:guest_id>/', login_required(views.check_out), name='check_out'),
    path('add_reservation/', login_required(views.add_reservation), name='add_reservation'),
    path('todays_bookings/', login_required(views.todays_bookings), name='todays_bookings'),
    path('sales_report/', login_required(views.sales_report), name='sales_report'),
    path('pricing/', login_required(views.pricing), name='pricing'),
    path('set_price/', login_required(views.set_price), name='set_price'),
    path('book_guest/', login_required(views.book_guest), name='book_guest'),
    path('manage_admin/', login_required(views.manage_admin), name='manage_admin'),
    path('add_admin/', login_required(views.add_admin), name='add_admin'),
    path('edit_admin/<int:admin_id>/', login_required(views.edit_admin), name='edit_admin'),
    path('delete_admin/<int:admin_id>/', login_required(views.delete_admin), name='delete_admin'),
    path('change_admin_password/<int:admin_id>/', login_required(views.change_admin_password), name='change_admin_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)