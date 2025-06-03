document.addEventListener('DOMContentLoaded', function() {
    var dateEl = document.getElementById('current-date');
    if (dateEl) {
        var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        var today = new Date();
        dateEl.textContent = today.toLocaleDateString(undefined, options);
    }
});