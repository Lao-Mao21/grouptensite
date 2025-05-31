document.addEventListener('DOMContentLoaded', function() {
    const showBtn = document.getElementById('show-book-form');
    const modal = document.getElementById('book-guest-form-modal');
    const closeBtn = document.getElementById('close-book-form');

    if (showBtn && modal) {
        showBtn.addEventListener('click', function() {
            modal.style.display = 'flex';
        });
    }
    if (closeBtn && modal) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    // Optional: Close modal when clicking outside the form
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});