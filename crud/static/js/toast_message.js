document.addEventListener('DOMContentLoaded', function() {
    // Only show toasts if we came from a form submission
    if (document.referrer && document.referrer.includes(window.location.host)) {
        const toasts = document.querySelectorAll('[id^="toast-"]');
        
        toasts.forEach((toast, index) => {
            // Remove hidden class
            toast.classList.remove('hidden');
            
            // Show toast with slight delay between each
            setTimeout(() => {
                toast.style.transform = 'translateX(0)';
            }, 100 * (index + 1));

            // Hide toast after delay
            setTimeout(() => {
                toast.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    toast.remove();
                }, 300);
            }, 5000 + (100 * index));
        });
    } else {
        // If we didn't come from a form submission, clear any existing messages
        const toastContainer = document.getElementById('toast-container');
        if (toastContainer) {
            toastContainer.remove();
        }
    }
});