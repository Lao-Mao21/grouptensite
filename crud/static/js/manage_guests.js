// Table switcher logic
function initializeTableSwitcher() {
    const todayRadio = document.getElementById('show-today');
    const reservationsRadio = document.getElementById('show-reservations');
    const todayTable = document.getElementById('today-table');
    const reservationsTable = document.getElementById('reservations-table');
    const reservationsFilterContainer = document.getElementById('reservations-filter-container');
    const todayBookingsFilter = document.getElementById('today-bookings-filter');

    function showTable(active) {
        if (active === 'reservations') {
            todayTable.style.display = 'none';
            reservationsTable.style.display = '';
            reservationsFilterContainer.style.display = '';
            todayBookingsFilter.style.display = 'none';
            reservationsRadio.checked = true;
            todayRadio.checked = false;
        } else {
            todayTable.style.display = '';
            reservationsTable.style.display = 'none';
            reservationsFilterContainer.style.display = 'none';
            todayBookingsFilter.style.display = '';
            todayRadio.checked = true;
            reservationsRadio.checked = false;
        }
    }

    todayRadio.addEventListener('change', () => showTable('today'));
    reservationsRadio.addEventListener('change', () => showTable('reservations'));

    // On page load, show the correct table based on active_table param
    const params = new URLSearchParams(window.location.search);
    const activeTable = params.get('active_table');
    showTable(activeTable === 'reservations' ? 'reservations' : 'today');
}

// Modal handling
function setupModal(buttonId, modalId, closeButtonId) {
    const button = document.getElementById(buttonId);
    const modal = document.getElementById(modalId);
    const closeButton = document.getElementById(closeButtonId);

    if (button && modal && closeButton) {
        button.addEventListener('click', () => {
            modal.style.display = 'flex';
        });

        closeButton.addEventListener('click', () => {
            modal.style.display = 'none';
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
}

// Form handling
function setupDateValidation(checkInInput, checkOutInput) {
    if (!checkInInput || !checkOutInput) return;
    
    checkInInput.addEventListener('change', function() {
        checkOutInput.min = this.value;
        if (checkOutInput.value && checkOutInput.value <= this.value) {
            checkOutInput.value = '';
        }
    });
}

function setupRoomSelection(roomSelect, bedCountInput, bedTypeInput, floorInput, roomTypeInput) {
    if (!roomSelect) return;
    
    roomSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        bedCountInput.value = selectedOption.dataset.bedCount;
        bedTypeInput.value = selectedOption.dataset.bedType;
        floorInput.value = selectedOption.dataset.floor;
        roomTypeInput.value = selectedOption.dataset.roomType;
    });

    // Trigger initial values
    if (roomSelect.options.length > 0) {
        roomSelect.dispatchEvent(new Event('change'));
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize table switcher
    initializeTableSwitcher();

    // Setup modals
    setupModal('show-book-form', 'book-guest-form-modal', 'close-book-form');
    setupModal('show-reservation-form', 'reserve-guest-form-modal', 'close-reserve-form');

    // Get form elements
    const elements = {
        booking: {
            roomSelect: document.getElementById('room_id'),
            bedCountInput: document.getElementById('bed_count'),
            bedTypeInput: document.getElementById('bed_type'),
            floorInput: document.getElementById('floor'),
            roomTypeInput: document.getElementById('room_type'),
            checkInInput: document.getElementById('check_in'),
            checkOutInput: document.getElementById('check_out')
        },
        reservation: {
            roomSelect: document.getElementById('reserve_room_id'),
            bedCountInput: document.getElementById('reserve_bed_count'),
            bedTypeInput: document.getElementById('reserve_bed_type'),
            floorInput: document.getElementById('reserve_floor'),
            roomTypeInput: document.getElementById('reserve_room_type'),
            checkInInput: document.getElementById('reserve_check_in'),
            checkOutInput: document.getElementById('reserve_check_out')
        }
    };

    // Set min datetime for all date inputs to current time
    const now = new Date();
    const nowString = now.toISOString().slice(0, 16);
    [elements.booking.checkInInput, elements.reservation.checkInInput].forEach(input => {
        if (input) input.min = nowString;
    });

    // Setup date validation for both forms
    setupDateValidation(elements.booking.checkInInput, elements.booking.checkOutInput);
    setupDateValidation(elements.reservation.checkInInput, elements.reservation.checkOutInput);

    // Setup room selection for both forms
    setupRoomSelection(
        elements.booking.roomSelect,
        elements.booking.bedCountInput,
        elements.booking.bedTypeInput,
        elements.booking.floorInput,
        elements.booking.roomTypeInput
    );
    setupRoomSelection(
        elements.reservation.roomSelect,
        elements.reservation.bedCountInput,
        elements.reservation.bedTypeInput,
        elements.reservation.floorInput,
        elements.reservation.roomTypeInput
    );
}); 