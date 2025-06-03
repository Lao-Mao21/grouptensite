// Form validation and enhancement functionality
function setupFormValidation(formId, options = {}) {
    const form = document.getElementById(formId);
    if (!form) return;

    // Setup date constraints
    const setupDateConstraints = () => {
        const checkInInput = form.querySelector('[name="check_in"]');
        const checkOutInput = form.querySelector('[name="check_out"]');
        
        if (checkInInput && checkOutInput) {
            const now = new Date();
            const nowString = now.toISOString().slice(0, 16);
            
            checkInInput.min = nowString;
            
            checkInInput.addEventListener('change', function() {
                checkOutInput.min = this.value;
                if (checkOutInput.value && checkOutInput.value <= this.value) {
                    checkOutInput.value = '';
                }
            });
        }
    };

    // Setup room selection
    const setupRoomSelection = () => {
        const roomSelect = form.querySelector('[name="room_id"]');
        if (!roomSelect) return;

        const updateRoomDetails = () => {
            const selectedOption = roomSelect.options[roomSelect.selectedIndex];
            if (!selectedOption) return;

            // Update hidden inputs
            ['bed_count', 'bed_type', 'floor', 'room_type'].forEach(field => {
                const input = form.querySelector(`[name="${field}"]`);
                if (input && selectedOption.dataset[field]) {
                    input.value = selectedOption.dataset[field];
                }
            });

            // Update price if available
            const priceDisplay = form.querySelector('#room-price-display');
            if (priceDisplay && selectedOption.dataset.price) {
                priceDisplay.textContent = `₱${parseFloat(selectedOption.dataset.price).toLocaleString()}`;
            }
        };

        roomSelect.addEventListener('change', updateRoomDetails);
        updateRoomDetails(); // Initial update
    };

    // Setup payment validation
    const setupPaymentValidation = () => {
        const paymentInput = form.querySelector('[name="payment"]');
        if (!paymentInput) return;

        paymentInput.addEventListener('input', function() {
            // Remove non-numeric characters except decimal point
            this.value = this.value.replace(/[^\d.]/g, '');
            
            // Ensure only one decimal point
            const parts = this.value.split('.');
            if (parts.length > 2) {
                this.value = parts[0] + '.' + parts.slice(1).join('');
            }
            
            // Limit to two decimal places
            if (parts[1] && parts[1].length > 2) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    };

    // Form submission handling
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Basic validation
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('border-red-500');
                
                // Add or update error message
                let errorMsg = field.parentElement.querySelector('.error-message');
                if (!errorMsg) {
                    errorMsg = document.createElement('p');
                    errorMsg.className = 'error-message text-red-500 text-sm mt-1';
                    field.parentElement.appendChild(errorMsg);
                }
                errorMsg.textContent = 'This field is required';
            } else {
                field.classList.remove('border-red-500');
                const errorMsg = field.parentElement.querySelector('.error-message');
                if (errorMsg) errorMsg.remove();
            }
        });

        if (isValid) {
            // If using AJAX submission
            if (options.useAjax) {
                const formData = new FormData(form);
                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert(data.error || 'An error occurred');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while submitting the form');
                });
            } else {
                form.submit(); // Regular form submission
            }
        }
    });

    // Initialize all validations
    setupDateConstraints();
    setupRoomSelection();
    setupPaymentValidation();
}

// Initialize form validation when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Setup validation for all forms
    setupFormValidation('add-room-form');
    setupFormValidation('book-guest-form');
    setupFormValidation('reserve-guest-form');

    // Handle room selection and populate hidden fields
    const roomSelect = document.getElementById('room_id');
    if (roomSelect) {
        roomSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            document.getElementById('bed_count').value = selectedOption.dataset.bedCount || '';
            document.getElementById('bed_type').value = selectedOption.dataset.bedType || '';
            document.getElementById('floor').value = selectedOption.dataset.floor || '';
            document.getElementById('room_type').value = selectedOption.dataset.roomType || '';
        });
    }

    // Handle modal close buttons
    const closeButtons = document.querySelectorAll('[id$="-form-btn"]');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modalId = this.id.replace('-btn', '-modal');
            document.getElementById(modalId).style.display = 'none';
        });
    });

    // Form validation
    const bookGuestForm = document.getElementById('book-guest-form');
    if (bookGuestForm) {
        bookGuestForm.addEventListener('submit', function(e) {
            const checkIn = new Date(document.getElementById('check_in').value);
            const checkOut = new Date(document.getElementById('check_out').value);
            
            if (checkIn >= checkOut) {
                e.preventDefault();
                alert('Check-out date must be after check-in date');
                return;
            }

            if (checkIn < new Date()) {
                e.preventDefault();
                alert('Check-in date cannot be in the past');
                return;
            }
        });
    }
}); 