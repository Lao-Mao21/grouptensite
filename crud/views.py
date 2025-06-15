from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models, transaction, IntegrityError
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Q, Case, When, DecimalField, F
from django.views.decorators.http import require_POST, require_http_methods
from django.conf import settings
from .models import (
    ManageRoom, 
    ManageGuest, 
    GuestAccounts, 
    AdminAccounts, 
    GuestArchive, 
    PaymentTransaction
)
from .backends import MockPaymentService, StripePaymentService, guest_login_required
import json
from django.contrib.auth.hashers import make_password
import math

def update_booking_statuses():
    """
    Update booking and room statuses automatically based on current time
    """
    current_time = timezone.now()
    
    # Update bookings whose check-in time has passed
    bookings_to_update = ManageGuest.objects.filter(
        status='reserved',
        check_in__lte=current_time,
        check_out__gt=current_time,
        payment_status='paid'
    )
    
    for booking in bookings_to_update:
        booking.status = 'occupied'
        booking.save()
        
        # Update room status
        room = booking.room_id
        room.room_status = 'occupied'
        room.save()
    
    # Update expired bookings
    expired_bookings = ManageGuest.objects.filter(
        status__in=['occupied', 'reserved'],
        check_out__lte=current_time
    )
    
    for booking in expired_bookings:
        booking.status = 'checked_out'
        booking.save()
        
        # Update room status
        room = booking.room_id
        room.room_status = 'available'
        room.save()

# Admin Views
@login_required
def logout_admin(request):
    logout(request)
    return redirect('/login_admin/')

def login_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Check if username exists
        if not AdminAccounts.objects.filter(username=username).exists():
            error_message = "Username does not exist"
            messages.error(request, error_message)
            return render(request, "web/admin/login_admin.html", {
                "username": username,
                "error_type": "username",
                "error": error_message
            })
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('admin_dashboard')
        else:
            error_message = "Incorrect password"
            messages.error(request, error_message)
            return render(request, "web/admin/login_admin.html", {
                "username": username,
                "error_type": "password",
                "error": error_message
            })
        
    return render(request, "web/admin/login_admin.html")

# Fixed functions with proper indentation

@login_required
def add_room(request):
    if request.method == "POST":
        try:
            room_number = request.POST.get("room_number", "").strip()
            room_type   = request.POST.get("room_type")
            bed_type    = request.POST.get("bed_type")
            room_price  = request.POST.get("room_price")
            bed_count   = request.POST.get("bed_count")
            floor       = request.POST.get("floor")
            room_status = request.POST.get("room_status", "available")

            # Validate mandatory numeric fields
            if not bed_count or not bed_count.isdigit():
                raise ValueError("Bed count must be a number")

            # Uniqueness validation before hitting DB unique constraint
            if ManageRoom.objects.filter(room_number=room_number).exists():
                messages.error(request, "Room number already exists.")
                raise ValueError("duplicate")

            ManageRoom.objects.create(
                room_number=room_number,
                room_type=room_type,
                bed_type=bed_type,
                bed_count=int(bed_count),
                floor=floor,
                room_price=room_price,
                room_status=room_status
            )

            messages.success(request, "Room added successfully.")
            return redirect('manage_rooms')

        except IntegrityError as ie:
            messages.error(request, f'Database error: {ie}')
        except ValueError as ve:
            if str(ve) != "duplicate":
                messages.error(request, str(ve))
        except Exception as e:
            messages.error(request, f'Error adding room: {str(e)}')

        # fall-through renders form again with entered data
        return render(request, "web/admin/add_room.html", {
            "room_number": room_number,
            "room_type": room_type,
            "bed_type": bed_type,
            "bed_count": bed_count,
            "floor": floor,
            "room_price": room_price,
            "room_status": room_status
        })
    return render(request, "web/admin/add_room.html")

@login_required
def pricing(request):
    """Handle the pricing page view"""
    try:
        # Get all rooms with search functionality
        search = request.GET.get('search', '')
        rooms = ManageRoom.objects.all()
        if search:
            rooms = rooms.filter(
                Q(room_number__icontains=search) |
                Q(room_type__icontains=search)
            )

        # Paginate the rooms
        paginator = Paginator(rooms, 5)  # Show rooms per page
        page_number = request.GET.get('page', 1)
        rooms = paginator.get_page(page_number)

        # Get room types data for statistics
        room_type_data = {}
        all_rooms = ManageRoom.objects.all()
        for room in all_rooms:
            room_type = room.room_type
            if room_type not in room_type_data:
                room_type_data[room_type] = {
                    'id': room_type,
                    'name': room.get_room_type_display(),
                    'min_price': float('inf'),
                    'max_price': 0,
                    'total_rooms': 0,
                    'available_rooms': 0
                }
            
            room_type_data[room_type]['total_rooms'] += 1
            if room.room_status == 'available':
                room_type_data[room_type]['available_rooms'] += 1
            
            if room.room_price < room_type_data[room_type]['min_price']:
                room_type_data[room_type]['min_price'] = float(room.room_price)
            if room.room_price > room_type_data[room_type]['max_price']:
                room_type_data[room_type]['max_price'] = float(room.room_price)

        # Convert to list and sort by min price
        room_types = list(room_type_data.values())
        room_types.sort(key=lambda x: x['min_price'])

        # Get price types from the model
        room_price_type = ManageRoom.PRICE_TYPE_CHOICES

        context = {
            'rooms': rooms,
            'room_types': room_types,
            'room_price_type': room_price_type,
            'current_year': timezone.now().year,
            'search': search
        }
        
        return render(request, 'web/admin/pricing.html', context)
        
    except Exception as e:
        print(f"Error in pricing view: {str(e)}")  # Add logging
        messages.error(request, f'Error loading pricing page: {str(e)}')
        return redirect('admin_dashboard')

@login_required
def set_price(request):
    if request.method == "POST":
        try:
            room_id = request.POST.get("room_id")
            room_price = request.POST.get("room_price")
            price_type = request.POST.get("price_type")
            
            if not all([room_id, room_price, price_type]):
                messages.error(request, "Please fill in all required fields.")
                return redirect('/pricing/')
            
            room = ManageRoom.objects.get(room_id=room_id)
            room.room_price = room_price
            room.room_price_type = price_type
            room.save()
            
            messages.success(request, 'Room price updated successfully.')
            return redirect('/pricing/')
            
        except ManageRoom.DoesNotExist:
            messages.error(request, 'Room not found.')
            return redirect('/pricing/')
        except Exception as e:
            messages.error(request, f'Error updating room price: {str(e)}')
            return redirect('/pricing/')
            
    return redirect('pricing')

@login_required
def edit_room(request, room_id):
    try:
        room = get_object_or_404(ManageRoom, room_id=room_id)
        if request.method == "POST":
            room.room_number = request.POST.get("room_number")
            room.room_type = request.POST.get("room_type")
            room.bed_type = request.POST.get("bed_type")
            room.room_price = request.POST.get("room_price")
            room.room_status = request.POST.get("room_status")
            room.save()
            
            messages.success(request, 'Room updated successfully.')
            return redirect('manage_rooms')
            
        return render(request, "web/admin/edit_room.html", {
            "room": room
        })
    except Exception as e:
        messages.error(request, f'Error updating room: {str(e)}')
        return redirect('manage_rooms')

@login_required
def delete_room(request, room_id):
    try:
        room = ManageRoom.objects.get(room_id=room_id)
        if request.method == "POST":
            room.delete()
            messages.success(request, 'Room deleted successfully.')
            return redirect('manage_rooms')
        return render(request, "web/admin/confirm_delete_room.html", {
            "room": room
        })
    except ManageRoom.DoesNotExist:
        messages.error(request, 'Room not found.')
        return redirect('manage_rooms')
    except Exception as e:
        messages.error(request, f'Error deleting room: {str(e)}')
        return redirect('manage_rooms')

@login_required
def edit_guest(request, booking_id):
    try:
        booking = get_object_or_404(ManageGuest, id=booking_id)
        if request.method == "POST":
            # Update guest booking details
            booking.check_in = parse_datetime(request.POST.get('check_in'))
            booking.check_out = parse_datetime(request.POST.get('check_out'))
            booking.payment_status = request.POST.get('payment_status')
            booking.save()

            messages.success(request, 'Guest booking updated successfully.')
            return redirect('manage_guests')

        return render(request, "web/admin/edit_guest.html", {
            "booking": booking,
            "payment_status_choices": ManageGuest.PAYMENT_STATUS_CHOICES
        })
    except Exception as e:
        messages.error(request, f'Error updating guest booking: {str(e)}')
        return redirect('manage_guests')

@login_required
def admin_dashboard(request):
    # Get current year and month
    current_year = timezone.now().year
    current_month = timezone.now().month

    # Get main statistics
    available_rooms = ManageRoom.objects.filter(room_status="available")
    available_rooms_count = available_rooms.count()
    reserved_rooms = ManageRoom.objects.filter(room_status="reserved").count()
    today = timezone.now().date()
    todays_bookings = ManageGuest.objects.filter(check_in__date=today).count()
    todays_reservations = ManageRoom.objects.filter(room_status="reserved").count()

    # Get monthly sales data for bar chart
    monthly_sales = [0] * 12  # Initialize array with zeros
    yearly_sales = ManageGuest.objects.filter(
        check_in__year=current_year,
        payment_status='paid'
    ).values('check_in__month').annotate(
        total=Sum('room_id__room_price')
    )
    
    for sale in yearly_sales:
        month_idx = sale['check_in__month'] - 1
        monthly_sales[month_idx] = float(sale['total'] or 0)

    # Get room type distribution for pie chart
    room_sales = ManageGuest.objects.filter(
        check_in__year=current_year,
        check_in__month=current_month,
        payment_status='paid'
    ).values(
        'room_id__room_type'
    ).annotate(
        total=Sum('room_id__room_price')
    )

    pie_data = []
    for sale in room_sales:
        pie_data.append({
            'name': sale['room_id__room_type'],
            'value': float(sale['total'] or 0)
        })

    context = {
        'available_rooms': available_rooms,
        'available_rooms_count': available_rooms_count,
        'reserved_rooms': reserved_rooms,
        'todays_bookings': todays_bookings,
        'todays_reservations': todays_reservations,
        'current_year': current_year,
        'current_month': timezone.now().strftime('%B'),
        'monthly_sales': monthly_sales,
        'pie_data': pie_data,
    }

    return render(request, "web/admin/admin_dashboard.html", context)

@login_required
def manage_rooms(request):
    # Update statuses before displaying
    update_booking_statuses()
    
    # Determine the selected status from query params; default to 'all'
    status = request.GET.get('room_status', 'all')
    search = request.GET.get('search', '')
    
    # Get rooms with their latest guest booking and payment status
    rooms_list = ManageRoom.objects.all()

    # Apply status filter only if a specific room status is selected
    if status and status != 'all':
        rooms_list = rooms_list.filter(room_status=status)

    # Apply search across multiple fields for better usability
    if search:
        rooms_list = rooms_list.filter(
            Q(room_number__icontains=search) |
            Q(room_type__icontains=search) |
            Q(floor__icontains=search)
        )

    # Annotate rooms with their latest guest's payment status
    for room in rooms_list:
        if room.room_status == 'occupied':
            # For occupied rooms, show as paid since they must be paid to be occupied
            room.current_payment_status = 'paid'
        elif room.room_status == 'reserved':
            # Get the latest active booking for reserved rooms
            latest_booking = ManageGuest.objects.filter(
                room_id=room,
                status='reserved',
                check_out__gt=timezone.now()  # Only consider active bookings
            ).order_by('-created_at').first()
            
            room.current_payment_status = latest_booking.payment_status if latest_booking else 'pending'
        else:
            # For available, maintenance, or cleaning rooms
            room.current_payment_status = 'No booking'
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(rooms_list, 4)
    rooms = paginator.get_page(page_number)
    
    # Get all guests and rooms for the booking form
    all_guests = GuestAccounts.objects.all()
    all_rooms = ManageRoom.objects.all()
    
    return render(request, "web/admin/manage_rooms.html", {
        "rooms": rooms,
        "selected_status": status,
        "search": search,
        "all_guests": all_guests,
        "all_rooms": all_rooms,
        "payment_status_choices": ManageGuest.PAYMENT_STATUS_CHOICES,
    })

@login_required
def manage_guests(request):
    # Update statuses before displaying
    update_booking_statuses()
    
    search_query = request.GET.get('search', '')
    active_table = request.GET.get('active_table', 'today')

    # Base querysets with search filters
    base_search = (
        Q(guest_name__icontains=search_query) |  # Search by guest name for direct bookings
        Q(guest_id__full_name__icontains=search_query) |  # Search by guest account name
        Q(room_id__room_number__icontains=search_query) |
        Q(room_id__room_type__icontains=search_query) |
        Q(payment_status__icontains=search_query)
    )

    # Today's bookings with search - exclude checked out guests
    today = timezone.now().date()
    todays_bookings = ManageGuest.objects.filter(
        (
            Q(check_in__date=today) |  # Today's check-ins
            Q(status='occupied', check_out__date__gte=today)  # Currently occupied rooms
        ) & 
        ~Q(status='checked_out') &  # Exclude checked out guests
        base_search
    ).select_related('guest_id', 'room_id').order_by('check_in')

    # Calculate total amount for each booking in today's list
    for booking in todays_bookings:
        duration = booking.check_out - booking.check_in
        if booking.room_id.room_price_type == 'per hour':
            units = max(1, math.ceil(duration.total_seconds() / 3600))
        else:
            units = max(1, (booking.check_out.date() - booking.check_in.date()).days)
        booking.total_amount = booking.room_id.room_price * units

    # Guest reservations: bookings still upcoming (reserved) or occupied but not yet checked in today
    reservations_qs = ManageGuest.objects.filter(
        (
            Q(status__iexact='reserved') |
            (Q(status__iexact='occupied') & Q(check_in__date__gt=today))
        )
    ).filter(base_search).select_related('guest_id', 'room_id').order_by('check_in')

    # Use only actual reservations (no placeholders)
    reservations = list(reservations_qs)

    # Calculate total amount for each reservation
    for booking in reservations:
        # Compute total charge based on room price type
        duration = booking.check_out - booking.check_in
        if booking.room_id.room_price_type == 'per hour':
            units = max(1, math.ceil(duration.total_seconds() / 3600))
        else:
            units = max(1, (booking.check_out.date() - booking.check_in.date()).days)
        booking.total_amount = booking.room_id.room_price * units
        
        # Update room status if needed
        if booking.status == 'reserved' and booking.room_id.room_status != 'reserved':
            booking.room_id.room_status = 'reserved'
            booking.room_id.save()

    # Paginate the results - change the number of items per page
    paginator_today = Paginator(todays_bookings, 5)
    paginator_reservations = Paginator(reservations, 5)

    page_today = request.GET.get('today_page', 1)
    page_reservations = request.GET.get('reservation_page', 1)

    try:
        todays_bookings = paginator_today.page(page_today)
    except (PageNotAnInteger, EmptyPage):
        todays_bookings = paginator_today.page(1)

    try:
        reservations = paginator_reservations.page(page_reservations)
    except (PageNotAnInteger, EmptyPage):
        reservations = paginator_reservations.page(1)

    context = {
        'todays_bookings': todays_bookings,
        'reservations': reservations,
        'search_query': search_query,
        'active_table': active_table,
    }

    return render(request, "web/admin/manage_guests.html", context)

@login_required
def add_guest(request):
    if request.method == "POST":
        # Create a new GuestAccounts entry
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        middle_name = request.POST.get("middle_name")
        username = request.POST.get("username")
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        nationality = request.POST.get("nationality")
        date_of_birth = request.POST.get('date_of_birth')
        emergency_contact = request.POST.get("emergency_contact")
        notes = request.POST.get("notes")

        if GuestAccounts.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            # Pass all the form data back to the template
            context = {
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "username": username,
                "gender": gender,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "nationality": nationality,
                "date_of_birth": date_of_birth,
                "emergency_contact": emergency_contact,
                "notes": notes,
                # Add any other fields
            }
            return render(request, 'web/admin/add_guest.html', context)

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            # Pass all the form data back to the template
            context = {
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "username": username,
                "gender": gender,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "nationality": nationality,
                "date_of_birth": date_of_birth,
                "emergency_contact": emergency_contact,
                "notes": notes,
                # Add any other fields
            }
            return render(request, 'web/admin/add_guest.html', context)

        if not all([first_name, last_name, username, gender, email, phone_number, address, password]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'web/admin/add_admin.html', context)

        try:
            guest = GuestAccounts(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                full_name=f"{first_name} {middle_name if middle_name else ''} {last_name}".strip(),
                username=username,
                email=email,
                phone_number=phone_number,
                gender=gender,
                date_of_birth=date_of_birth,
                nationality=nationality,
                address=address,
                password=password,  # Model's save method will hash this
                last_login=timezone.now()
            )

            # If the model has 'is_active' field, set it explicitly to True
            if hasattr(guest, 'is_active'):
                guest.is_active = True

            guest.save()
            messages.success(request, "Guest added successfully!")
            return redirect("/manage_guests/")
        except ValueError as e:
            messages.error(request, str(e))
            context = {
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "username": username,
                "gender": gender,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "nationality": nationality,
                "date_of_birth": date_of_birth,
                "emergency_contact": emergency_contact,
                "notes": notes,
            }
            return render(request, 'web/admin/add_guest.html', context)
    return render(request, "web/admin/add_guest.html")

@login_required
def check_out(request, guest_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    try:
        with transaction.atomic():  # Use transaction to ensure data consistency
            guest_booking = ManageGuest.objects.select_for_update().get(id=guest_id)
            room = guest_booking.room_id
            
            # Check if the room has a valid status for check-out
            if room.room_status not in ['occupied', 'reserved']:
                return JsonResponse({
                    'success': False,
                    'error': f'Invalid room status for check-out. Current status: {room.room_status}'
                }, status=400)
            
            # Check if payment is completed
            if guest_booking.payment_status != 'paid':
                return JsonResponse({
                    'success': False,
                    'error': 'Cannot check out: Payment is not completed.'
                }, status=400)

            # Update guest booking status
            guest_booking.status = 'checked_out'
            guest_booking.save()

            # Update room status
            room.room_status = 'available'
            room.save()

            # Create archive entry
            GuestArchive.objects.create(
                guest_id=guest_booking.guest_id,
                room_id=room,
                check_in=guest_booking.check_in,
                check_out=guest_booking.check_out,
                payment_status=guest_booking.payment_status,
                payment_mode=guest_booking.payment_mode,
                guest_count=guest_booking.guest_count,
                status='checked_out'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Guest checked out successfully.'
            })

    except ManageGuest.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Guest booking not found.'
        }, status=404)
        
    except Exception as e:
        print(f"Error during checkout: {str(e)}")  # Add logging
        return JsonResponse({
            'success': False,
            'error': f'Error during check out: {str(e)}'
        }, status=500)

@login_required
def sales_report(request):
    # Get current year and month
    current_year = timezone.now().year
    current_month = timezone.now().month

    # Get current month's sales data
    sales = ManageGuest.objects.filter(
        check_in__year=current_year,
        check_in__month=current_month,
        payment_status='paid'
    ).values('check_in__day').annotate(
        day=F('check_in__day'),
        total_sales=Sum('room_id__room_price'),
        total_booking=Count('id')
    ).order_by('check_in__day')

    # Get room type distribution for pie chart
    room_sales = ManageGuest.objects.filter(
        check_in__year=current_year,
        check_in__month=current_month,
        payment_status='paid'
    ).values(
        'room_id__room_type'
    ).annotate(
        total=Sum('room_id__room_price')
    )

    pie_data = []
    for sale in room_sales:
        pie_data.append({
            'name': sale['room_id__room_type'],
            'value': float(sale['total'] or 0)
        })

    # Get monthly sales for the year
    monthly_sales = [0] * 12
    yearly_sales = ManageGuest.objects.filter(
        check_in__year=current_year,
        payment_status='paid'
    ).values('check_in__month').annotate(
        total=Sum('room_id__room_price')
    )
    
    for sale in yearly_sales:
        month_idx = sale['check_in__month'] - 1
        monthly_sales[month_idx] = float(sale['total'] or 0)

    context = {
        'current_year': current_year,
        'current_month': timezone.now().strftime('%B'),  # Full month name
        'monthly_sales': monthly_sales,
        'pie_data': pie_data,
        'sales_report': sales
    }

    return render(request, 'web/admin/sales.html', context)

@login_required
def todays_bookings(request):
    today = timezone.now().date()
    todays_bookings = ManageGuest.objects.filter(check_in__date=today)

    # Calculate total amount for each booking in today's list
    for booking in todays_bookings:
        duration = booking.check_out - booking.check_in
        if booking.room_id.room_price_type == 'per hour':
            units = max(1, math.ceil(duration.total_seconds() / 3600))
        else:
            units = max(1, (booking.check_out.date() - booking.check_in.date()).days)
        booking.total_amount = booking.room_id.room_price * units

    # Guest reservations: bookings still upcoming (reserved) or occupied but not yet checked in today
    reservations_qs = ManageGuest.objects.filter(
        (
            Q(status__iexact='reserved') |
            (Q(status__iexact='occupied') & Q(check_in__date__gt=today))
        )
    ).filter(
        ~Q(status='checked_out')
    ).select_related('guest_id', 'room_id').order_by('check_in')

    # Use only actual reservations (no placeholders)
    reservations = list(reservations_qs)

    # Calculate total amount for each reservation
    for booking in reservations:
        # Compute total charge based on room price type
        duration = booking.check_out - booking.check_in
        if booking.room_id.room_price_type == 'per hour':
            units = max(1, math.ceil(duration.total_seconds() / 3600))
        else:
            units = max(1, (booking.check_out.date() - booking.check_in.date()).days)
        booking.total_amount = booking.room_id.room_price * units
        
        # Update room status if needed
        if booking.status == 'reserved' and booking.room_id.room_status != 'reserved':
            booking.room_id.room_status = 'reserved'
            booking.room_id.save()

    # Paginate the results - change the number of items per page
    paginator_today = Paginator(todays_bookings, 5)
    paginator_reservations = Paginator(reservations, 5)

    page_today = request.GET.get('today_page', 1)
    page_reservations = request.GET.get('reservation_page', 1)

    try:
        todays_bookings = paginator_today.page(page_today)
    except (PageNotAnInteger, EmptyPage):
        todays_bookings = paginator_today.page(1)

    try:
        reservations = paginator_reservations.page(page_reservations)
    except (PageNotAnInteger, EmptyPage):
        reservations = paginator_reservations.page(1)

    context = {
        'todays_bookings': todays_bookings,
        'reservations': reservations,
        'current_year': timezone.now().year,
        'current_month': timezone.now().strftime('%B'),
        'total_todays_bookings': todays_bookings.paginator.count,
        'total_todays_reservations': reservations_qs.count(),
    }

    return render(request, "web/admin/todays_bookings.html", context)

@login_required
def add_reservation(request):
    if request.method == "POST":
        guest_id = request.POST.get("guest_id")
        room_id = request.POST.get("room_id")
        status = request.POST.get("status", "reserved")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        payment = request.POST.get("payment")
        bed_count = request.POST.get("bed_count")
        bed_type = request.POST.get("bed_type")
        floor = request.POST.get("floor")

        # Validate inputs
        if not guest_id or not room_id or not check_in or not check_out:
            return HttpResponse("Invalid input", status=400)
        try:
            check_in = parse_datetime(check_in)
            check_out = parse_datetime(check_out)
            if check_in >= check_out:
                return HttpResponse("Check-in date must be before check-out date", status=400)
        except ValueError:
            return HttpResponse("Invalid date format", status=400)

        # Check if the room is available
        room = ManageRoom.objects.filter(room_id=room_id, room_status="available").first()
        if not room:
            return HttpResponse("Room is not available", status=400)

        # Check if the guest exists
        if not GuestAccounts.objects.filter(guest_id=guest_id).exists():
            return HttpResponse("Guest does not exist", status=400)

        # Validate payment status
        if payment not in ["paid", "pending", "cancelled"]:
            return HttpResponse("Invalid payment status", status=400)

        # Validate check-in and check-out dates
        if check_in < timezone.now() or check_out <= check_in:
            return HttpResponse("Invalid check-in or check-out date", status=400)

        # Validate that the room is not already booked for the given dates
        if ManageGuest.objects.filter(
            room_id_id=room_id,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists():
            return HttpResponse("Room is already booked for the selected dates", status=400)

        # Validate that the guest is not already booked in another room for the same dates
        if ManageGuest.objects.filter(
            guest_id_id=guest_id,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists():
            return HttpResponse("Guest is already booked in another room for the selected dates", status=400)

        # Get the guest account
        guest = GuestAccounts.objects.get(guest_id=guest_id)
        
        # Create reservation entry
        ManageGuest.objects.create(
            guest_id=guest,
            guest_name=guest.full_name,
            room_id_id=room_id,
            status=status,
            bed_count=bed_count,
            bed_type=bed_type,
            floor=floor,
            check_in=check_in,
            check_out=check_out,
            expected_arrival=check_in,
            payment_status=payment
        )

        # Update room status
        room = ManageRoom.objects.get(room_id=room_id)
        room.room_status = status
        room.save()

        return redirect("/manage_guests/")
    all_guests = GuestAccounts.objects.all()
    all_rooms = ManageRoom.objects.all()
    return render(request, "web/admin/add_reservation.html", {
        "all_guests": all_guests,
        "all_rooms": all_rooms,
    })

@login_required
def book_guest(request):
    # Update statuses before processing
    update_booking_statuses()
    
    if request.method == "POST":
        # Get form data
        full_name = request.POST.get("full_name")
        gender = request.POST.get("gender")
        contact_number = request.POST.get("contact_number")
        nationality = request.POST.get("nationality")
        address = request.POST.get("address")
        expected_arrival = request.POST.get("expected_arrival")
        room_id = request.POST.get("room_number")  # This is the room_id from the select
        guest_count = request.POST.get("guest_count")
        check_in_time = request.POST.get("check_in")
        check_out_time = request.POST.get("check_out")
        payment_mode = request.POST.get("payment_mode")
        booking_type = request.POST.get('booking_type')

        # Validate required fields
        if not all([full_name, gender, contact_number, nationality, address, 
                   room_id, guest_count, check_in_time, check_out_time, payment_mode, booking_type]):
            missing_fields = []
            if not full_name: missing_fields.append("Full Name")
            if not gender: missing_fields.append("Gender")
            if not contact_number: missing_fields.append("Contact Number")
            if not nationality: missing_fields.append("Nationality")
            if not address: missing_fields.append("Address")
            if not room_id: missing_fields.append("Room")
            if not guest_count: missing_fields.append("Guest Count")
            if not check_in_time: missing_fields.append("Check In Time")
            if not check_out_time: missing_fields.append("Check Out Time")
            if not payment_mode: missing_fields.append("Payment Mode")
            if not booking_type: missing_fields.append("Booking Type")
            
            return HttpResponse(f"Missing required fields: {', '.join(missing_fields)}", status=400)

        try:
            # Get the room
            room = ManageRoom.objects.get(room_id=room_id)
            if room.room_status != "available":
                return HttpResponse("Room is no longer available", status=400)

            # Convert check-in and check-out times
            check_in = parse_datetime(check_in_time)
            if not check_in:
                return HttpResponse("Invalid check-in time", status=400)

            check_out = parse_datetime(check_out_time)
            if not check_out:
                return HttpResponse("Invalid check-out time", status=400)

            # Set expected arrival if not provided
            expected_arrival_dt = parse_datetime(expected_arrival) if expected_arrival else check_in

            # Set initial status based on booking type
            if booking_type == 'immediate':
                initial_status = 'occupied'
                room_status = 'occupied'
            else:  # reservation
                initial_status = 'reserved'
                room_status = 'reserved'

            # Create booking without requiring a guest account
            booking = ManageGuest.objects.create(
                guest_id=None,  # No guest account required
                guest_name=full_name,  # Store the name directly
                room_id=room,
                status=initial_status,
                guest_count=int(guest_count),
                check_in=check_in,
                check_out=check_out,
                expected_arrival=expected_arrival_dt,
                payment_status='paid',  # Always set to paid
                payment_mode=payment_mode
            )

            # Update room status
            room.room_status = room_status
            room.save()

            return redirect('/manage_guests/')

        except Exception as e:
            return HttpResponse(str(e), status=400)

    # For GET requests, render the booking form
    available_rooms = ManageRoom.objects.filter(room_status="available")
    room_types = [choice[0] for choice in ManageRoom.ROOM_TYPE_CHOICES]
    
    return render(request, "web/admin/book_guest.html", {
        "available_rooms": available_rooms,
        "room_types": room_types,
    })

@login_required
def add_admin(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        middle_name = request.POST.get("middle_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        is_active = request.POST.get("is_active")
        
        if AdminAccounts.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            context = {
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "username": username,
                "gender": gender,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "date_of_birth": date_of_birth,
            }
            return render(request, 'web/admin/add_admin.html', context)

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            context = {
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "username": username,
                "gender": gender,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "date_of_birth": date_of_birth,
            }
            return render(request, 'web/admin/add_admin.html', context)

        if not all([first_name, last_name, username, gender, email, phone_number, address, password]):
            messages.error(request, "Please fill in all required fields.")
            context = {
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "username": username,
                "gender": gender,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "date_of_birth": date_of_birth,
            }
            return render(request, 'web/admin/add_admin.html', context)
        
        try:
            # Check if password is already in use
            hashed_password = make_password(password)
            if (AdminAccounts.objects.filter(password=hashed_password).exists() or 
                GuestAccounts.objects.filter(password=hashed_password).exists()):
                messages.error(request, "This password is already in use. Please choose a different password.")
                context = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "middle_name": middle_name,
                    "username": username,
                    "gender": gender,
                    "email": email,
                    "phone_number": phone_number,
                    "address": address,
                    "date_of_birth": date_of_birth,
                }
                return render(request, 'web/admin/add_admin.html', context)

            # Create admin account
            full_name = f"{first_name} {middle_name} {last_name}".strip()
            admin = AdminAccounts.objects.create(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                username=username,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                address=address,
                password=hashed_password,  # Use the hashed password
                gender=gender,
                date_of_birth=date_of_birth,
                is_active=True if is_active else True
            )
            messages.success(request, 'Admin account created successfully.')
            return redirect('manage_admin')
        except ValueError as e:
            messages.error(request, str(e))
            context = {
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "username": username,
                "gender": gender,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "date_of_birth": date_of_birth,
            }
            return render(request, 'web/admin/add_admin.html', context)
    return render(request, "web/admin/add_admin.html")

@login_required        
def manage_admin(request):
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Start with all admins
    admins_list = AdminAccounts.objects.all()
    
    # Apply search if provided
    if search_query:
        admins_list = admins_list.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    # Apply status filter if provided
    if status_filter:
        if status_filter == 'active':
            admins_list = admins_list.filter(is_active=True)
        elif status_filter == 'inactive':
            admins_list = admins_list.filter(is_active=False)
    
    # Order by first name
    admins_list = admins_list.order_by('first_name')
    
    # Paginate results
    paginator = Paginator(admins_list, 5)  # Show admins per page
    page = request.GET.get('page', 1)
    
    try:
        admins = paginator.page(page)
    except PageNotAnInteger:
        admins = paginator.page(1)
    except EmptyPage:
        admins = paginator.page(paginator.num_pages)
    
    # Prepare context
    context = {
        "admins": admins,
        "search_query": search_query,
        "status_filter": status_filter,
        "total_admins": admins_list.count(),
        "active_admins": admins_list.filter(is_active=True).count(),
        "inactive_admins": admins_list.filter(is_active=False).count()
    }
    
    return render(request, "web/admin/manage_admins.html", context)

@login_required
def edit_admin(request, admin_id):
    try:
        admin = AdminAccounts.objects.get(admin_id=admin_id)
        if request.method == "POST":
            # Check if username already exists for other admins
            if AdminAccounts.objects.filter(username=request.POST.get("username")).exclude(admin_id=admin_id).exists():
                messages.error(request, 'Username already exists. Please choose another.')
                return redirect('manage_admin')

            # Update admin details
            admin.first_name = request.POST.get("first_name")
            admin.last_name = request.POST.get("last_name")
            admin.middle_name = request.POST.get("middle_name", "")
            admin.username = request.POST.get("username")
            admin.email = request.POST.get("email")
            admin.phone_number = request.POST.get("phone_number")
            admin.address = request.POST.get("address")
            admin.gender = request.POST.get("gender")
            admin.date_of_birth = request.POST.get("date_of_birth") or None
            admin.is_active = request.POST.get("is_active") == "on"
            
            # Update full name
            admin.full_name = f"{admin.first_name} {admin.middle_name} {admin.last_name}".strip()
            
            # Validate required fields
            if not all([admin.first_name, admin.last_name, admin.username, 
                       admin.email, admin.phone_number, admin.address]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, "web/admin/manage_admins.html", {
                    "admin": admin,
                    "error": "Please fill in all required fields."
                })
            
            admin.save()
            messages.success(request, 'Admin account updated successfully.')
            return redirect('manage_admin')
            
        # For GET requests, render the edit form
        return render(request, "web/admin/manage_admins.html", {
            "admin": admin,
            "edit_mode": True
        })
    except AdminAccounts.DoesNotExist:
        messages.error(request, 'Admin account not found.')
        return redirect('manage_admin')
    except Exception as e:
        messages.error(request, f'Error updating admin: {str(e)}')
        return redirect('manage_admin')

@login_required
def delete_admin(request, admin_id):
    try:
        admin = AdminAccounts.objects.get(admin_id=admin_id)
        if request.method == "POST":
            admin.delete()
            messages.success(request, 'Admin account deleted successfully.')
            return redirect('/manage_admin/')
        return render(request, "web/admin/confirm_delete_admin.html", {
            "admin": admin
        })
    except AdminAccounts.DoesNotExist:
        messages.error(request, 'Admin account not found.')
        return redirect('/manage_admin/')
    except Exception as e:
        messages.error(request, f'Error deleting admin: {str(e)}')
        return redirect('/manage_admin/')

@login_required
def change_admin_password(request, admin_id):
    if request.method == 'POST':
        try:
            admin = AdminAccounts.objects.get(admin_id=admin_id)
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Validate current password
            if not admin.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return render(request, "web/admin/manage_admins.html", {
                    "admin": admin,
                    "error": "Current password is incorrect.",
                    "show_password_modal": True
                })

            # Validate new password
            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return render(request, "web/admin/manage_admins.html", {
                    "admin": admin,
                    "error": "New passwords do not match.",
                    "show_password_modal": True
                })

            # Validate password length
            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, "web/admin/manage_admins.html", {
                    "admin": admin,
                    "error": "Password must be at least 8 characters long.",
                    "show_password_modal": True
                })

            # Check if new password is already in use
            hashed_password = make_password(new_password)
            if (AdminAccounts.objects.exclude(admin_id=admin_id).filter(password=hashed_password).exists() or 
                GuestAccounts.objects.filter(password=hashed_password).exists()):
                messages.error(request, 'This password is already in use. Please choose a different password.')
                return render(request, "web/admin/manage_admins.html", {
                    "admin": admin,
                    "error": "This password is already in use. Please choose a different password.",
                    "show_password_modal": True
                })

            # Update password
            admin.password = hashed_password
            admin.save()

            messages.success(request, 'Password changed successfully.')
            return redirect('manage_admin')

        except AdminAccounts.DoesNotExist:
            messages.error(request, 'Admin account not found.')
            return redirect('manage_admin')
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, "web/admin/manage_admins.html", {
                "admin": admin,
                "error": str(e),
                "show_password_modal": True
            })
        except Exception as e:
            messages.error(request, f'Error changing password: {str(e)}')
            return render(request, "web/admin/manage_admins.html", {
                "admin": admin,
                "error": f'Error changing password: {str(e)}',
                "show_password_modal": True
            })

    # For GET requests, show the password change form
    try:
        admin = AdminAccounts.objects.get(admin_id=admin_id)
        return render(request, "web/admin/manage_admins.html", {
            "admin": admin,
            "show_password_modal": True
        })
    except AdminAccounts.DoesNotExist:
        messages.error(request, 'Admin account not found.')
        return redirect('manage_admin')

# Guest Views
def nova_hotel(request):
    # This should remain public - no decorator needed
    context = {}
    
    if 'guest_id' in request.session:
        try:
            guest = GuestAccounts.objects.get(guest_id=request.session['guest_id'])
            context.update({
                'guest': guest
            })
        except GuestAccounts.DoesNotExist:
            pass
    
    return render(request, 'web/guest/nova_hotel.html', context)

def register(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Get form data
                first_name = request.POST.get('first_name')
                middle_name = request.POST.get('middle_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                phone_number = request.POST.get('phone_number')
                gender = request.POST.get('gender')
                date_of_birth = request.POST.get('date_of_birth')
                nationality = request.POST.get('nationality')
                address = request.POST.get('address')
                username = request.POST.get('username')
                password = request.POST.get('password')

                # Validate required fields
                if not all([first_name, last_name, email, phone_number, gender, 
                          date_of_birth, nationality, address,
                          username, password]):
                    return JsonResponse({
                        'success': False,
                        'error': 'Please fill in all required fields.'
                    })

                # Check if username already exists
                if GuestAccounts.objects.filter(username=username).exists():
                    return JsonResponse({
                        'success': False,
                        'error': 'Username already exists. Please choose another.'
                    })

                # Check if password is already in use
                hashed_password = make_password(password)
                if AdminAccounts.objects.filter(password=hashed_password).exists() or GuestAccounts.objects.filter(password=hashed_password).exists():
                    return JsonResponse({
                        'success': False,
                        'error': 'This password is already in use. Please choose a different password.'
                    })

                # Create GuestAccounts instance
                guest = GuestAccounts(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    full_name=f"{first_name} {middle_name if middle_name else ''} {last_name}".strip(),
                    username=username,
                    email=email,
                    phone_number=phone_number,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    nationality=nationality,
                    address=address,
                    password=hashed_password,  # Model's save method will hash this
                    last_login=timezone.now()
                )

                # If the model has 'is_active' field, set it explicitly to True
                if hasattr(guest, 'is_active'):
                    guest.is_active = True

                guest.save()

                # Set session data
                request.session['guest_id'] = guest.guest_id
                request.session['guest_name'] = guest.full_name

                return JsonResponse({
                    'success': True,
                    'redirect_url': '/nova_hotel/'  # Change to redirect to 
                })

        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

def logo(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        # other context variables
    }
    return render(request, 'navbar.html', context)

@guest_login_required
def guest_account(request):
    try:
        guest = GuestAccounts.objects.get(guest_id=request.session.get('guest_id'))
        
        bookings = ManageGuest.objects.select_related(
            'guest_id', 
            'room_id'
        ).filter(
            guest_id=guest
        ).exclude(
            status='checked_out'
        ).order_by('-created_at')
        
        for booking in bookings:
            try:
                transaction = PaymentTransaction.objects.filter(booking=booking).first()
                booking.transaction_info = transaction
            except PaymentTransaction.DoesNotExist:
                booking.transaction_info = None
        
        context = {
            'guest': guest,
            'bookings': bookings,
        }
        
        return render(request, 'web/guest/guest_account.html', context)
    except GuestAccounts.DoesNotExist:
        messages.error(request, "Guest account not found.")
        return redirect('/nova_hotel/')

@guest_login_required
def guest_change_password(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            guest = GuestAccounts.objects.get(guest_id=request.session.get('guest_id'))
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not guest.check_password(current_password):
                return JsonResponse({
                    'success': False,
                    'error': 'Current password is incorrect'
                })

            if new_password != confirm_password:
                return JsonResponse({
                    'success': False,
                    'error': 'Passwords do not match'
                })

            # Check if new password is already in use
            hashed_password = make_password(new_password)
            if (AdminAccounts.objects.filter(password=hashed_password).exists() or 
                GuestAccounts.objects.exclude(guest_id=guest.guest_id).filter(password=hashed_password).exists()):
                return JsonResponse({
                    'success': False,
                    'error': 'This password is already in use. Please choose a different password'
                })

            guest.password = new_password
            guest.save()

            return JsonResponse({
                'success': True,
                'message': 'Password changed successfully'
            })

        except GuestAccounts.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Guest account not found'
            })
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    })

@require_http_methods(["GET"])
def check_room_availability(request, room_type, room_number):
    """Check if a room is available for the given dates"""
    try:
        # Get the room by type and number
        room = get_object_or_404(ManageRoom, room_type=room_type, room_number=str(room_number))
        
        # Check if room exists and is available
        if room.room_status != 'available':
            return JsonResponse({
                'success': False,
                'room_status': room.room_status,
                'message': f'Room {room.room_number} is currently {room.room_status}'
            })

        # If dates are provided, check for booking conflicts
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
        
        if check_in and check_out:
            try:
                check_in = parse_datetime(check_in)
                check_out = parse_datetime(check_out)
                
                # Validate dates
                if check_in >= check_out:
                    return JsonResponse({
                        'success': False,
                        'message': 'Check-out must be after check-in'
                    })

                # Check for overlapping bookings
                overlapping = ManageGuest.objects.filter(
                    room_id=room,
                    status__in=['pending', 'confirmed', 'occupied', 'reserved'],
                    check_in__lt=check_out,
                    check_out__gt=check_in
                ).exists()

                if overlapping:
                    return JsonResponse({
                        'success': False,
                        'message': f'Room {room.room_number} is not available for selected dates'
                    })
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid date format'
                })

        return JsonResponse({
            'success': True,
            'room_status': 'available',
            'message': f'Room {room.room_number} is available'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@guest_login_required
def booking_web(request):
    try:
        guest_account = GuestAccounts.objects.get(guest_id=request.session['guest_id'])
        
        rooms = ManageRoom.objects.all()
        room_type_data = {}
        
        for room in rooms:
            room_type = room.room_type
            if room_type not in room_type_data:
                room_type_data[room_type] = {
                    'id': room_type,
                    'name': room.get_room_type_display(),
                    'price': float('inf'),
                    'max_price': 0,
                    'available_rooms': [],
                    'image': f"{room_type.lower()}.jpg",
                    'total_rooms': 0,
                    'room_status': 'unavailable'
                }
            
            room_type_data[room_type]['total_rooms'] += 1
            
            if room.room_price < room_type_data[room_type]['price']:
                room_type_data[room_type]['price'] = float(room.room_price)
            if room.room_price > room_type_data[room_type]['max_price']:
                room_type_data[room_type]['max_price'] = float(room.room_price)
            
            if room.room_status == 'available':
                room_type_data[room_type]['available_rooms'].append(room)
                room_type_data[room_type]['room_status'] = 'available'

        room_types = []
        for room_type_info in room_type_data.values():
            room_type_info['available'] = len(room_type_info['available_rooms'])
            room_types.append(room_type_info)

        room_types.sort(key=lambda x: x['price'])

        available_rooms = ManageRoom.objects.filter(
            room_status='available'
        ).order_by('room_type', 'room_number')

        context = {
            'guest_account': guest_account,
            'room_types': room_types,
            'available_rooms': available_rooms,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY
        }
        
        return render(request, 'web/guest/booking_web.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading booking page: {str(e)}')
        return redirect('/nova_hotel/')

def guest_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # First check if account exists
            try:
                guest = GuestAccounts.objects.get(username=username)
            except GuestAccounts.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Account does not exist',
                    'field': 'username',
                    'formData': {
                        'username': username,
                        'password': password
                    }
                })

            # Then check password
            user = authenticate(request, username=username, password=password, backend='crud.backends.GuestAccountsBackend')
            if user is not None:
                # Log the user in
                login(request, user)
                
                # Set session data
                request.session['guest_id'] = user.guest_id
                request.session['guest_name'] = user.full_name
                
                # Update last login
                user.last_login = timezone.now()
                user.save()
                
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/guest/account/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Incorrect password',
                    'field': 'password',
                    'formData': {
                        'username': username,
                        'password': password
                    }
                })
                
        except Exception as e:
            print(f"Login error: {str(e)}")  # For debugging
            return JsonResponse({
                'success': False,
                'error': 'An error occurred during login. Please try again.',
                'formData': {
                    'username': username,
                    'password': password
                }
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

@require_POST
def guest_logout(request):
    """Handle guest logout."""
    try:
        # Clear any guest-specific session data
        if 'guest_id' in request.session:
            del request.session['guest_id']
        if 'guest_name' in request.session:
            del request.session['guest_name']
        
        # Perform Django logout
        logout(request)
        
        # Add success message
        messages.success(request, 'You have been successfully logged out.')
        
        return HttpResponseRedirect('/nova_hotel/')
    except Exception as e:
        # Log the error (in a real application)
        print(f"Error during logout: {str(e)}")
        messages.error(request, 'An error occurred during logout. Please try again.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def process_booking_payment(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        
    try:
        data = json.loads(request.body)
        booking_id = data.get('booking_id')
        amount = data.get('amount')
        
        if not booking_id or not amount:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
            
        booking = ManageGuest.objects.get(id=booking_id)
        
        # Create payment transaction
        payment = PaymentTransaction.objects.create(
            booking=booking,
            amount=amount,
            status='pending'
        )
        
        # Initialize payment service (default to Mock if setting absent)
        if getattr(settings, 'USE_STRIPE', False):
            payment_service = StripePaymentService()
        else:
            payment_service = MockPaymentService()
            
        # Process payment
        result = payment_service.process_payment(payment)
        
        if result.get('success'):
            booking.payment_status = 'paid'
            booking.save()
            payment.status = 'completed'
            payment.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Payment processed successfully'
            })
        else:
            payment.status = 'failed'
            payment.save()
            return JsonResponse({
                'error': result.get('error', 'Payment processing failed')
            }, status=400)
            
    except ManageGuest.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@guest_login_required
def process_payment(request):
    try:
        data = json.loads(request.body)
        
        guest = GuestAccounts.objects.get(guest_id=request.session.get('guest_id'))
        room = get_object_or_404(ManageRoom, room_id=data['booking_id'])
        
        # Check if room is available
        if room.room_status != 'available':
            return JsonResponse({
                'success': False,
                'error': 'Room is no longer available'
            })
        
        check_in = parse_datetime(data['booking_details']['check_in'])
        check_out = parse_datetime(data['booking_details']['check_out'])
        expected_arrival = parse_datetime(data['booking_details']['expected_arrival'])
        
        # Validate dates
        if check_in >= check_out:
            return JsonResponse({
                'success': False,
                'error': 'Check-out must be after check-in'
            })
            
        # Check for overlapping bookings for this specific room
        overlapping = ManageGuest.objects.filter(
            room_id=room,
            status__in=['pending', 'confirmed', 'occupied', 'reserved'],
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()
        
        if overlapping:
            return JsonResponse({
                'success': False,
                'error': 'Room is not available for selected dates'
            })
        
        use_stripe = getattr(settings, 'USE_STRIPE', False)

        # Always create the booking first so we have a valid FK for any payment rows
        booking = ManageGuest.objects.create(
            guest_id=guest,
            guest_name=guest.full_name,
            room_id=room,
            status='reserved',
            guest_count=int(data['booking_details']['guest_count']),
            check_in=check_in,
            check_out=check_out,
            expected_arrival=expected_arrival,
            payment_status='paid' if not use_stripe else 'pending',
            payment_mode='card'
        )

        # Update room status immediately
        room.room_status = 'reserved'
        room.save()

        # If Stripe is enabled, create a PaymentTransaction and process it
        if use_stripe:
            payment_service = StripePaymentService()

            payment = PaymentTransaction.objects.create(
                guest=guest,
                booking=booking,
                amount=float(data['booking_details'].get('total_amount', 0)),
                status='pending',
                payment_method='card'
            )

            result = payment_service.process_payment(payment)

            if result.get('success'):
                payment.status = 'completed'
                booking.payment_status = 'paid'
                success = True
                message = 'Booking confirmed successfully'
            else:
                payment.status = 'failed'
                booking.payment_status = 'pending'
                success = False
                message = 'Payment processing failed'

            payment.save()
            booking.save()

            if success:
                return JsonResponse({'success': True, 'message': message})
            else:
                return JsonResponse({'success': False, 'error': message})

        # For mock payments we skip recording card/payment details entirely
        return JsonResponse({
            'success': True,
            'message': 'Booking confirmed successfully (mock payment)'
        })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def confirm_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_intent_id = data.get('payment_intent_id')
            
            # Confirm payment with Stripe
            payment_service = StripePaymentService()
            confirmation = payment_service.confirm_payment(payment_intent_id)
            
            if not confirmation['success']:
                return JsonResponse({
                    'success': False,
                    'error': confirmation['error']
                })
            
            # Update transaction status
            transaction = PaymentTransaction.objects.get(stripe_payment_intent_id=payment_intent_id)
            transaction.status = 'completed' if confirmation['status'] == 'succeeded' else 'failed'
            transaction.payment_details = confirmation
            transaction.save()
            
            # Update booking status if payment successful
            if confirmation['status'] == 'succeeded':
                booking = transaction.booking
                booking.status = 'confirmed'
                booking.save()
            
            return JsonResponse({
                'success': True,
                'status': confirmation['status']
            })
            
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Transaction not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@guest_login_required
def cancel_booking(request, booking_id):
    """Allow a logged-in guest to cancel their own future reservation."""
    try:
        booking = get_object_or_404(ManageGuest, id=booking_id, guest_id=request.session.get('guest_id'))

        # Only allow cancellation if booking has not started yet and is not already cancelled/checked out
        if booking.status in ['reserved', 'confirmed'] and booking.check_in > timezone.now():
            booking.status = 'cancelled'
            # If payment was already captured, mark it for refund
            if booking.payment_status == 'paid':
                booking.payment_status = 'refunded'
            booking.save()

            # Free up the room
            room = booking.room_id
            room.room_status = 'available'
            room.save()

            # Mark any related payment transaction as refunded
            PaymentTransaction.objects.filter(booking=booking).update(status='refunded')

            messages.success(request, 'Booking cancelled successfully.')
        else:
            messages.error(request, 'This booking cannot be cancelled.')

    except Exception as e:
        messages.error(request, f'Error cancelling booking: {e}')

    return redirect('guest_account')