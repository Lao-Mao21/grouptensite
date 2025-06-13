# Fixed functions with proper indentation

@login_required
def add_room(request):
    if request.method == "POST":
        try:
            room_number = request.POST.get("room_number")
            room_type = request.POST.get("room_type")
            bed_type = request.POST.get("bed_type")
            room_price = request.POST.get("room_price")
            room_status = request.POST.get("room_status", "available")
            
            # Create new room
            room = ManageRoom.objects.create(
                room_number=room_number,
                room_type=room_type,
                bed_type=bed_type,
                room_price=room_price,
                room_status=room_status
            )
            
            messages.success(request, 'Room added successfully.')
            return redirect('manage_rooms')
        except IntegrityError:
            messages.error(request, 'Room number already exists.')
            return render(request, "web/admin/add_room.html", {
                "room_number": room_number,
                "room_type": room_type,
                "bed_type": bed_type,
                "room_price": room_price,
                "room_status": room_status
            })
        except Exception as e:
            messages.error(request, f'Error adding room: {str(e)}')
            return redirect('manage_rooms')
    return render(request, "web/admin/add_room.html")

@login_required
def set_price(request):
    if request.method == "POST":
        try:
            room_id = request.POST.get("room_id")
            new_price = request.POST.get("room_price")
            
            room = ManageRoom.objects.get(room_id=room_id)
            room.room_price = new_price
            room.save()
            
            messages.success(request, 'Room price updated successfully.')
            return redirect('manage_rooms')
        except ManageRoom.DoesNotExist:
            messages.error(request, 'Room not found.')
            return redirect('manage_rooms')
        except Exception as e:
            messages.error(request, f'Error updating room price: {str(e)}')
            return redirect('manage_rooms')
    return redirect('manage_rooms')

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