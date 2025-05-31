from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ManageRoom, ManageGuest, GuestAccounts
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count
from django.shortcuts import render

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            return render(request, "web/admin/login.html", {"error": "Invalid credentials"})
    return render(request, "web/admin/login.html")

def login_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("web/admin/admin_dashboard/")
        else:
            return render(request, "web/admin/login.html", {"error": "Invalid credentials"})
    return render(request, "web/admin/login.html")

def admin_dashboard(request):
    available_rooms = ManageRoom.objects.filter(room_status="available").count()
    reserved_rooms = ManageRoom.objects.filter(room_status="reserved").count()
    monthly_sales = ManageGuest.objects.filter(payment_status="paid").count()
    today = timezone.now().date()
    todays_bookings = ManageGuest.objects.filter(check_in__date=today).count()
    return render(request, "web/admin/admin_dashboard.html", {
        "available_rooms": available_rooms,
        "reserved_rooms": reserved_rooms,
        "monthly_sales": monthly_sales,
        "todays_bookings": todays_bookings,
    })

def manage_rooms(request):
    status = request.GET.get('room_status', 'available')
    search = request.GET.get('search', '')
    rooms_list = ManageRoom.objects.all()
    if status:
        rooms_list = rooms_list.filter(room_status=status)
    if search:
        rooms_list = rooms_list.filter(room_number__icontains=search)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(rooms_list, 10)
    rooms = paginator.get_page(page_number)
    return render(request, "web/admin/manage_rooms.html", {
        "rooms": rooms,
        "selected_status": status,
        "search": search,
    })

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
    return render(request, "web/admin/manage_guests.html", {
        "todays_bookings": todays_bookings,
        "reservations": reservations,
        "all_guests": all_guests,
        "all_rooms": all_rooms,
    })

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

def add_room(request):
    if request.method == "POST":
        room_number = request.POST.get("room_number")
        room_type = request.POST.get("room_type")
        bed_count = request.POST.get("bed_count")
        floor = request.POST.get("floor")
        room_status = request.POST.get("room_status")
        room_price = request.POST.get("room_price")
        available_at = request.POST.get("available_at")
        # available_at = parse_datetime(available_at)
        ManageRoom.objects.create(
            room_number=room_number,
            room_type=room_type,
            bed_count=bed_count,
            floor=floor,
            room_status=room_status,
            room_price=room_price,
            available_at=available_at,
        )
        return redirect('manage_rooms')
    return render(request, "web/admin/add_room.html")

def sales_report(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        if start_date and end_date:
            # start_date = parse_datetime(start_date)
            # end_date = parse_datetime(end_date)
            sales = ManageGuest.objects.filter(
                payment_status="paid",
                check_in__date__range=(start_date, end_date)
            )
        else:
            sales = ManageGuest.objects.filter(payment_status="paid")
        return render(request, "web/admin/sales_report.html", {"sales": sales})
    return render(request, "web/admin/sales_report.html")

def todays_bookings(request):
    today = timezone.now().date()
    todays_bookings = ManageGuest.objects.filter(check_in__date=today)
    return render(request, "web/admin/todays_bookings.html", {"todays_bookings": todays_bookings})

@csrf_exempt
def add_reservation(request):
    if request.method == "POST":
        guest_id = request.POST.get("guest_id")
        room_id = request.POST.get("room_id")
        status = request.POST.get("status", "reserved")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        payment = request.POST.get("payment")

        # Create reservation (ManageGuest)
        ManageGuest.objects.create(
            guest_id_id=guest_id,
            room_id_id=room_id,
            status=status,
            check_in=check_in,
            check_out=check_out,
            payment_status=payment,
        )
        return redirect("/manage_guests/")
    all_guests = GuestAccounts.objects.all()
    all_rooms = ManageRoom.objects.all()
    return render(request, "web/admin/add_reservation.html", {
        "all_guests": all_guests,
        "all_rooms": all_rooms,
    })

def sales_report(request):
    # Annual Revenue by month and room type
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    room_types = ['FAMILY', 'VIP', 'Deluxe']
    annual_data = {rtype: [0]*12 for rtype in room_types}

    for idx, month in enumerate(months, 1):
        for rtype in room_types:
            total = ManageGuest.objects.filter(
                room_id__room_type=rtype,
                payment_status='paid',
                check_in__month=idx
            ).aggregate(total=Sum('payment_status'))['total'] or 0
            annual_data[rtype][idx-1] = float(total)

    # Pie chart: total sales per room type for May
    pie_data = []
    for rtype in room_types:
        total = ManageGuest.objects.filter(
            room_id__room_type=rtype,
            payment_status='paid',
            check_in__month=5
        ).aggregate(total=Sum('payment_status'))['total'] or 0
        pie_data.append(float(total))

    # Daily sales for May
    from calendar import monthrange
    days_in_may = monthrange(timezone.now().year, 5)[1]
    daily_sales = []
    for day in range(1, days_in_may+1):
        total_booking = ManageGuest.objects.filter(
            payment_status='paid',
            check_in__month=5,
            check_in__day=day
        ).count()
        total_cancellation = ManageGuest.objects.filter(
            payment_status='cancelled',
            check_in__month=5,
            check_in__day=day
        ).count()
        refunded = ManageGuest.objects.filter(
            payment_status='refunded',
            check_in__month=5,
            check_in__day=day
        ).aggregate(total=Sum('payment_status'))['total'] or 0
        total_sales = ManageGuest.objects.filter(
            payment_status='paid',
            check_in__month=5,
            check_in__day=day
        ).aggregate(total=Sum('payment_status'))['total'] or 0
        daily_sales.append({
            "day": day,
            "total_booking": total_booking,
            "total_cancellation": total_cancellation,
            "refunded": refunded,
            "total_sales": total_sales,
        })

    paginator = Paginator(daily_sales, 7)  # Show 5 rows per page
    page_number = request.GET.get('page', 1)
    sales_page = paginator.get_page(page_number)

    context = {
        "months": months,
        "room_types": room_types,
        "annual_data": annual_data,
        "pie_data": pie_data,
        "sales_report": sales_page,
    }
    return render(request, "web/admin/sales.html", context)