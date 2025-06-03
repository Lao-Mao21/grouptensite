document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('book-guest-form');
    const roomSelect = document.getElementById('room_id');
    const guestSelect = document.getElementById('guest_id');
    const checkInInput = document.getElementById('check_in');
    const checkOutInput = document.getElementById('check_out');
    const displayRoomType = document.getElementById('display-room-type');
    const displayBedType = document.getElementById('display-bed-type');
    const displayFloor = document.getElementById('display-floor');
    const displayPrice = document.getElementById('display-price');
    const paymentSelect = document.getElementById('payment');

    // Initialize payment select
    if (paymentSelect) {
        // Add change event listener
        paymentSelect.addEventListener('change', function(e) {
            const selectedOption = this.options[this.selectedIndex];
            if (selectedOption.value === '') {
                // If default option is selected, select the first non-disabled option
                for (let i = 0; i < this.options.length; i++) {
                    if (!this.options[i].disabled) {
                        this.options[i].selected = true;
                        break;
                    }
                }
            }
            // Force the select to update visually
            this.blur();
            this.focus();
        });

        // Ensure a valid option is selected initially
        if (paymentSelect.value === '') {
            for (let i = 0; i < paymentSelect.options.length; i++) {
                if (!paymentSelect.options[i].disabled) {
                    paymentSelect.options[i].selected = true;
                    break;
                }
            }
        }
    }
    
    // Store form data
    let formData = {
        guest_id: '',
        room_id: '',
        check_in: '',
        check_out: '',
        bed_count: '',
        bed_type: '',
        floor: '',
        room_type: ''
    };

    // Function to update room details display
    function updateRoomDisplay() {
        if (!formData.room_type) return;
        
        displayRoomType.textContent = formData.room_type.charAt(0).toUpperCase() + formData.room_type.slice(1);
        displayBedType.textContent = formData.bed_type.charAt(0).toUpperCase() + formData.bed_type.slice(1);
        displayFloor.textContent = `${formData.floor}F`;
        const selectedOption = roomSelect.options[roomSelect.selectedIndex];
        displayPrice.textContent = selectedOption.dataset.price ? `₱${parseFloat(selectedOption.dataset.price).toLocaleString()}` : '-';
    }

    // Function to update hidden fields
    function updateHiddenFields() {
        document.getElementById('bed_count').value = formData.bed_count;
        document.getElementById('bed_type').value = formData.bed_type;
        document.getElementById('floor').value = formData.floor;
        document.getElementById('room_type').value = formData.room_type;
    }

    // Update room details when a room is selected
    roomSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        
        formData.room_id = this.value;
        formData.bed_count = selectedOption.dataset.bedCount || '';
        formData.bed_type = selectedOption.dataset.bedType || '';
        formData.floor = selectedOption.dataset.floor || '';
        formData.room_type = selectedOption.dataset.roomType || '';

        updateHiddenFields();
        updateRoomDisplay();
    });

    // Store guest selection
    guestSelect.addEventListener('change', function() {
        formData.guest_id = this.value;
    });

    // Date validation and storage
    const now = new Date();
    const nowString = now.toISOString().slice(0, 16);
    checkInInput.min = nowString;
    
    // Handle check-in date changes
    checkInInput.addEventListener('change', function() {
        formData.check_in = this.value;
        checkOutInput.min = this.value;
        
        // Only reset check-out if it's now invalid
        if (checkOutInput.value && checkOutInput.value <= this.value) {
            checkOutInput.value = '';
            formData.check_out = '';
        }
    });

    // Handle check-out date changes
    checkOutInput.addEventListener('change', function() {
        formData.check_out = this.value;
    });

    // Handle form reset
    form.addEventListener('reset', function() {
        formData = {
            guest_id: '',
            room_id: '',
            check_in: '',
            check_out: '',
            bed_count: '',
            bed_type: '',
            floor: '',
            room_type: ''
        };
        displayRoomType.textContent = '-';
        displayBedType.textContent = '-';
        displayFloor.textContent = '-';
        displayPrice.textContent = '-';
        
        // Reset payment select to default
        if (paymentSelect) {
            const defaultOption = paymentSelect.querySelector('option[value=""]');
            if (defaultOption) {
                defaultOption.selected = true;
            }
        }
    });

    // Handle form submission
    form.addEventListener('submit', function(e) {
        // Validate all required fields are filled
        if (!formData.guest_id || !formData.room_id || !formData.check_in || !formData.check_out) {
            e.preventDefault();
            alert('Please fill in all required fields');
            return false;
        }
        
        // Validate check-out is after check-in
        if (new Date(formData.check_out) <= new Date(formData.check_in)) {
            e.preventDefault();
            alert('Check-out date must be after check-in date');
            return false;
        }

        // Validate payment is selected
        if (paymentSelect && (!paymentSelect.value || paymentSelect.value === '')) {
            e.preventDefault();
            alert('Please select a payment status');
            return false;
        }
    });

    // Modal handling
    const modal = document.getElementById('book-guest-form-modal');
    const closeButtons = document.querySelectorAll('#close-book-form');
    
    // Close modal functionality
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            modal.style.display = 'none';
            form.reset(); // Reset form when closing modal
        });
    });

    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            form.reset(); // Reset form when closing modal
        }
    });

    // Open modal functionality
    const openModalButton = document.querySelector('[onclick*="book-guest-form-modal"]');
    if (openModalButton) {
        openModalButton.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = 'flex';
        });
    }
}); 