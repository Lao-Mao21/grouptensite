from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ManageRoom, ManageGuest, GuestAccounts, AdminAccounts
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Q
from django.shortcuts import render

# Admin Views
@login_required
def logout_admin(request):
    logout(request)
    return redirect('/login_admin/')

def login_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"Attempting login with username: {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Authentication successful")
            login(request, user)
            return redirect("/admin_dashboard/")
        else:
            print("Authentication failed")
            return render(request, "web/admin/login_admin.html", {"error": "Invalid credentials"})
    return render(request, "web/admin/login_admin.html")

@login_required
def admin_dashboard(request):
    available_rooms = ManageRoom.objects.filter(room_status="available").count()
    available_rooms_qs = ManageRoom.objects.filter(room_status="available")
    reserved_rooms = ManageRoom.objects.filter(room_status="reserved").count()
    monthly_sales = ManageGuest.objects.filter(payment_status="paid").count()
    today = timezone.now().date()
    todays_bookings = ManageGuest.objects.filter(check_in__date=today).count()
    return render(request, "web/admin/admin_dashboard.html", {
        "available_rooms": available_rooms,
        "available_rooms": available_rooms_qs,
        "reserved_rooms": reserved_rooms,
        "monthly_sales": monthly_sales,
        "todays_bookings": todays_bookings,
    })

@login_required
def manage_rooms(request):
    status = request.GET.get('room_status', 'available')
    search = request.GET.get('search', '')
    
    # Get rooms with their latest guest booking and payment status
    rooms_list = ManageRoom.objects.all()
    if status:
        rooms_list = rooms_list.filter(room_status=status)
    if search:
        rooms_list = rooms_list.filter(room_number__icontains=search)

    # Annotate rooms with their latest guest's payment status
    for room in rooms_list:
        latest_booking = ManageGuest.objects.filter(room_id=room).order_by('-created_at').first()
        room.current_payment_status = latest_booking.payment_status if latest_booking else 'No booking'
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(rooms_list, 10)
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
    # Today's bookings
    todays_bookings_list = ManageGuest.objects.filter(check_in__date=timezone.now().date())
    reservations_list = ManageGuest.objects.filter(status='reserved')

    today_page_number = request.GET.get('today_page', 1)
    reservation_page_number = request.GET.get('reservation_page', 1)

    todays_bookings_paginator = Paginator(todays_bookings_list, 10)
    reservations_paginator = Paginator(reservations_list, 10)

    todays_bookings = todays_bookings_paginator.get_page(today_page_number)
    reservations = reservations_paginator.get_page(reservation_page_number)

    all_guests = GuestAccounts.objects.all()
    all_rooms = ManageRoom.objects.all()
    # Search functionality
    if request.method == "POST":
        search = request.POST.get('search', '')
        if search:
            todays_bookings = todays_bookings.filter(guest_id__full_name__icontains=search)
            reservations = reservations.filter(guest_id__full_name__icontains=search)
    else:
        search = request.GET.get('search', '')
        if search:
            todays_bookings = todays_bookings.filter(guest_id__full_name__icontains=search)
            reservations = reservations.filter(guest_id__full_name__icontains=search)
    return render(request, "web/admin/manage_guests.html", {
        "todays_bookings": todays_bookings,
        "reservations": reservations,
        "all_guests": all_guests,
        "all_rooms": all_rooms,
        "search": search,
        "now": timezone.now(),
    })

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
        nationality = request.POST.get("nationality")
        emergency_contact = request.POST.get("emergency_contact")
        notes = request.POST.get("notes")
        new_guest = GuestAccounts(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            username=username,
            full_name=full_name,
            gender=gender,
            email=email,
            phone_number=phone_number,
            address=address,
            password=password,
            nationality=nationality,
            emergency_contact=emergency_contact,
            notes=notes,
        )
        new_guest.save()
        return redirect("/manage_guests/")
    return render(request, "web/admin/add_guest.html")

@login_required
def add_room(request):
    if request.method == "POST":
        room_number = request.POST.get("room_number")
        room_type = request.POST.get("room_type")
        bed_count = request.POST.get("bed_count")
        floor = request.POST.get("floor")
        bed_type = request.POST.get("bed_type")
        room_status = request.POST.get("room_status")
        available_at = request.POST.get("available_at")
        payment_status = request.POST.get("payment_status", "pending")
        room_price_type = request.POST.get("room_price_type", "custom")
        room_price = request.POST.get("room_price", 0)

        ManageRoom.objects.create(
            room_number=room_number,
            room_type=room_type,
            bed_count=bed_count,
            floor=floor,
            bed_type=bed_type,
            room_status=room_status,
            room_price_type=room_price_type,
            available_at=available_at,
            payment_status=payment_status,
            room_price=room_price
        )
        return redirect('manage_rooms')
    return render(request, "web/admin/add_room.html")

@login_required
def set_price(request):
    if request.method == "POST":
        room_id = request.POST.get("room_id")
        room_price = request.POST.get("room_price")
        
        if not room_id or not room_price:
            return HttpResponse("Room ID and price are required", status=400)
            
        try:
            room = ManageRoom.objects.get(room_id=room_id)
            room.room_price = room_price
            room.save()
            return redirect('pricing')
        except ManageRoom.DoesNotExist:
            return HttpResponse("Room not found", status=404)
            
    return redirect('pricing')

@login_required
def sales_report(request):
    # Annual Revenue by month and room type
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    room_types = ['single', 'double', 'suite', 'deluxe']  # Updated to match model's ROOM_TYPE_CHOICES
    annual_data = {rtype: [0]*12 for rtype in room_types}

    current_year = timezone.now().year
    current_month = timezone.now().month
    current_month_name = months[current_month - 1]  # Get current month name

    for idx, month in enumerate(months, 1):
        for rtype in room_types:
            # Get all paid bookings for this room type and month
            bookings = ManageGuest.objects.filter(
                room_id__room_type=rtype,
                payment_status='paid',
                check_in__year=current_year,
                check_in__month=idx
            ).select_related('room_id')
            
            # Calculate total revenue by summing room prices
            total = sum(booking.room_id.room_price for booking in bookings)
            annual_data[rtype][idx-1] = float(total)

    # Monthly Top Sales (Pie Chart)
    pie_data = []
    total_monthly_sales = 0
    monthly_sales_by_type = {}

    for rtype in room_types:
        # Get all paid bookings for this room type in current month
        bookings = ManageGuest.objects.filter(
            room_id__room_type=rtype,
            payment_status='paid',
            check_in__year=current_year,
            check_in__month=current_month
        ).select_related('room_id')
        
        # Calculate total revenue
        total = sum(booking.room_id.room_price for booking in bookings)
        monthly_sales_by_type[rtype] = float(total)
        total_monthly_sales += float(total)

    # Calculate percentages for pie chart
    for rtype in room_types:
        percentage = (monthly_sales_by_type[rtype] / total_monthly_sales * 100) if total_monthly_sales > 0 else 0
        pie_data.append(percentage)

    # Daily sales for current month
    from calendar import monthrange
    days_in_month = monthrange(current_year, current_month)[1]
    daily_sales = []
    
    for day in range(1, days_in_month + 1):
        # Get paid bookings for this day
        paid_bookings = ManageGuest.objects.filter(
            payment_status='paid',
            check_in__year=current_year,
            check_in__month=current_month,
            check_in__day=day
        ).select_related('room_id')
        
        total_booking = paid_bookings.count()
        
        # Get cancelled bookings
        total_cancellation = ManageGuest.objects.filter(
            payment_status='cancelled',
            check_in__year=current_year,
            check_in__month=current_month,
            check_in__day=day
        ).count()
        
        # Calculate refunded amount
        refunded_bookings = ManageGuest.objects.filter(
            payment_status='refunded',
            check_in__year=current_year,
            check_in__month=current_month,
            check_in__day=day
        ).select_related('room_id')
        refunded = sum(booking.room_id.room_price for booking in refunded_bookings)
        
        # Calculate total sales
        total_sales = sum(booking.room_id.room_price for booking in paid_bookings)
        
        daily_sales.append({
            "day": day,
            "total_booking": total_booking,
            "total_cancellation": total_cancellation,
            "refunded": float(refunded),
            "total_sales": float(total_sales),
        })

    paginator = Paginator(daily_sales, 7)  # Show 7 rows per page
    page_number = request.GET.get('page', 1)
    sales_page = paginator.get_page(page_number)

    context = {
        "months": months,
        "room_types": room_types,
        "annual_data": annual_data,
        "pie_data": pie_data,
        "sales_report": sales_page,
        "current_month_name": current_month_name,  # Add current month name to context
    }
    return render(request, "web/admin/sales.html", context)

@login_required
def todays_bookings(request):
    today = timezone.now().date()
    todays_bookings = ManageGuest.objects.filter(check_in__date=today)
    return render(request, "web/admin/todays_bookings.html", {"todays_bookings": todays_bookings})

@login_required
@csrf_exempt
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
@csrf_exempt
def book_guest(request):
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

        # Print received data for debugging
        print("Received form data:")
        print(f"full_name: {full_name}")
        print(f"gender: {gender}")
        print(f"contact_number: {contact_number}")
        print(f"nationality: {nationality}")
        print(f"address: {address}")
        print(f"expected_arrival: {expected_arrival}")
        print(f"room_id: {room_id}")
        print(f"guest_count: {guest_count}")
        print(f"check_in_time: {check_in_time}")
        print(f"check_out_time: {check_out_time}")
        print(f"payment_mode: {payment_mode}")

        # Validate required fields
        if not all([full_name, gender, contact_number, nationality, address, 
                   room_id, guest_count, check_in_time, check_out_time, payment_mode]):
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
            
            return HttpResponse(f"Missing required fields: {', '.join(missing_fields)}", status=400)

        try:
            # Split full name into parts (assuming format: "First Middle Last")
            name_parts = full_name.split()
            first_name = name_parts[0]
            last_name = name_parts[-1]
            middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""

            # Create guest account if it doesn't exist
            guest, created = GuestAccounts.objects.get_or_create(
                full_name=full_name,
                defaults={
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name,
                    'username': f"guest_{first_name.lower()}_{last_name.lower()}",
                    'gender': gender.lower(),
                    'phone_number': contact_number,
                    'nationality': nationality,
                    'address': address,
                    'password': 'defaultpass123',  # You should implement proper password handling
                    'email': f"guest_{first_name.lower()}_{last_name.lower()}@example.com"  # You should collect email in form
                }
            )

            # Get the room
            room = ManageRoom.objects.get(room_id=room_id)
            if room.room_status != "available":
                return HttpResponse("Room is not available", status=400)

            # Convert check-in and check-out times
            check_in = parse_datetime(check_in_time)
            if not check_in:
                return HttpResponse("Invalid check-in time", status=400)

            check_out = parse_datetime(check_out_time)
            if not check_out:
                return HttpResponse("Invalid check-out time", status=400)

            # Set expected arrival if not provided
            expected_arrival_dt = parse_datetime(expected_arrival) if expected_arrival else check_in

            # Create booking
            ManageGuest.objects.create(
                guest_id=guest,
                guest_name=guest.full_name,
                room_id=room,
                status="reserved",
                guest_count=int(guest_count),
                check_in=check_in,
                check_out=check_out,
                expected_arrival=expected_arrival_dt,
                payment_status="pending",
                payment_mode=payment_mode
            )

            # Update room status
            room.room_status = "reserved"
            room.save()

            return redirect(request.META.get('HTTP_REFERER', '/'))

        except Exception as e:
            return HttpResponse(str(e), status=400)

    # For GET requests, render the booking form
    available_rooms = ManageRoom.objects.filter(room_status="available")
    room_types = [choice[0] for choice in ManageRoom.ROOM_TYPE_CHOICES]
    all_guests = GuestAccounts.objects.all()  # Get all guests
    
    return render(request, "web/admin/book_guest.html", {
        "available_rooms": available_rooms,
        "room_types": room_types,
        "all_guests": all_guests,  # Pass all_guests to template
    })

def edit_room(request, room_id):
    room = ManageRoom.objects.get(room_id=room_id)
    if request.method == "POST":
        room.room_number = request.POST.get("room_number")
        room.room_type = request.POST.get("room_type")
        room.bed_count = request.POST.get("bed_count")
        room.floor = request.POST.get("floor")
        room.bed_type = request.POST.get("bed_type")
        room.room_status = request.POST.get("room_status")
        room.room_price = request.POST.get("room_price")
        room.available_at = request.POST.get("available_at")
        room.payment_status = request.POST.get("payment_status", room.payment_status)
        room.save()
        return redirect('manage_rooms')
    return render(request, "web/admin/edit_room.html", {
        "room": room
    })

@login_required
def delete_room(request, room_id):
    room = ManageRoom.objects.get(room_id=room_id)
    if request.method == "POST":
        room.delete()
        return redirect('manage_rooms')
    return render(request, "web/admin/confirm_delete_room.html", {
        "room": room
    })

@login_required
def pricing(request):
    # Get all rooms with pagination
    search = request.GET.get('search', '')
    rooms_list = ManageRoom.objects.all().order_by('room_number')
    
    if search:
        rooms_list = rooms_list.filter(
            Q(room_number__icontains=search) |
            Q(room_type__icontains=search) |
            Q(floor__icontains=search) |
            Q(room_price_type__icontains=search)
        )
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(rooms_list, 5)
    rooms = paginator.get_page(page_number)
    
    # Get choices for dropdowns
    room_type_choices = ManageRoom.ROOM_TYPE_CHOICES
    bed_type_choices = ManageRoom.BED_TYPE_CHOICES
    room_price_type = ManageRoom.PRICE_TYPE_CHOICES
    
    context = {
        "rooms": rooms,
        "room_price_type": room_price_type,
        "room_type_choices": room_type_choices,
        "bed_type_choices": bed_type_choices,
        "search": search,
    }
    
    return render(request, "web/admin/pricing.html", context)

@login_required
def delete_guest(request, guest_id):
    guest = ManageGuest.objects.get(id=guest_id)
    if request.method == "POST":
        # Update room status back to available if it was occupied by this guest
        room = guest.room_id
        if room.room_status in ['occupied', 'reserved']:
            room.room_status = 'available'
            room.save()
        guest.delete()
        return redirect('manage_guests')
    return render(request, "web/admin/confirm_delete_guest.html", {
        "guest": guest
    })

@login_required
def edit_guest(request, guest_id):
    guest = ManageGuest.objects.get(id=guest_id)
    if request.method == "POST":
        # Get form data
        guest.guest_name = request.POST.get("guest_name")
        guest.guest_count = request.POST.get("guest_count")
        guest.check_in = request.POST.get("check_in")
        guest.check_out = request.POST.get("check_out")
        guest.expected_arrival = request.POST.get("expected_arrival")
        guest.payment_mode = request.POST.get("payment_mode")
        guest.payment_status = request.POST.get("payment_status", guest.payment_status)
        guest.status = request.POST.get("status", guest.status)
        guest.save()
        return redirect('manage_guests')
    
    return render(request, "web/admin/edit_guest.html", {
        "guest": guest,
        "payment_modes": ["cash", "card", "gcash"],
        "statuses": ["reserved", "checked_in", "checked_out", "cancelled"],
        "payment_statuses": ["pending", "paid", "refunded", "cancelled"]
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
        
        if password != confirm_password:
            return HttpResponse("Passwords do not match", status=400)
        
        # Create admin account
        admin = AdminAccounts.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            password=password,
            gender=gender,
            date_of_birth=date_of_birth,
            is_active=is_active
        )
        return redirect('manage_admin')
    return render(request, "web/admin/add_admin.html")

@login_required        
def manage_admin(request):
    admins = AdminAccounts.objects.all()
    return render(request, "web/admin/manage_admins.html", {
        "admins": admins
    })

@login_required
def edit_admin(request, admin_id):
    admin = AdminAccounts.objects.get(id=admin_id)
    if request.method == "POST":
        admin.first_name = request.POST.get("first_name")
        admin.last_name = request.POST.get("last_name")
        admin.middle_name = request.POST.get("middle_name")
        admin.username = request.POST.get("username")
        admin.email = request.POST.get("email")
        admin.phone_number = request.POST.get("phone_number")
        admin.address = request.POST.get("address")
        admin.password = request.POST.get("password")
        admin.gender = request.POST.get("gender")
        admin.date_of_birth = request.POST.get("date_of_birth")
        admin.is_active = request.POST.get("is_active")
        admin.save()
        return redirect('manage_admins')
    return render(request, "web/admin/edit_admin.html", {
        "admin": admin
    })

@login_required
def delete_admin(request, admin_id):
    admin = AdminAccounts.objects.get(id=admin_id)
    if request.method == "POST":
        admin.delete()
        return redirect('manage_admins')
    return render(request, "web/admin/confirm_delete_admin.html", {
        "admin": admin
    })

# Guest Views
def landing_page(request):
    return render(request, "web/guest/Landing_page.html")

# def login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("admin_dashboard")
#         else:
#             return render(request, "web/admin/login.html", {"error": "Invalid credentials"})
#     return render(request, "web/admin/login.html")