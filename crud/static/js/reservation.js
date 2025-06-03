// Reservation Modal logic
    const showReservationBtn = document.getElementById('show-reservation-form');
    const reserveGuestFormModal = document.getElementById('reserve-guest-form-modal');
    const closeReserveFormBtn = document.getElementById('close-reserve-form');

    if (showReservationBtn && reserveGuestFormModal) {
        showReservationBtn.addEventListener('click', function() {
            reserveGuestFormModal.style.display = 'flex';
        });
    }
    if (closeReserveFormBtn && reserveGuestFormModal) {
        closeReserveFormBtn.addEventListener('click', function() {
            reserveGuestFormModal.style.display = 'none';
        });
        // Optional: close modal when clicking outside the form
        reserveGuestFormModal.addEventListener('click', function(e) {
            if (e.target === reserveGuestFormModal) {
                reserveGuestFormModal.style.display = 'none';
            }
        });
    }