document.addEventListener('DOMContentLoaded', function() {
    // Table switcher logic
    const todayBtn = document.getElementById('show-today');
    const reservationsBtn = document.getElementById('show-reservations');
    const todayTable = document.getElementById('today-table');
    const reservationsTable = document.getElementById('reservations-table');

    function showTable(active) {
        if (active === 'reservations') {
            todayTable.style.display = 'none';
            reservationsTable.style.display = '';
            reservationsBtn.classList.add('bg-blue-600', 'text-white');
            reservationsBtn.classList.remove('bg-gray-300', 'text-gray-700');
            todayBtn.classList.remove('bg-blue-600', 'text-white');
            todayBtn.classList.add('bg-gray-300', 'text-gray-700');
        } else {
            todayTable.style.display = '';
            reservationsTable.style.display = 'none';
            todayBtn.classList.add('bg-blue-600', 'text-white');
            todayBtn.classList.remove('bg-gray-300', 'text-gray-700');
            reservationsBtn.classList.remove('bg-blue-600', 'text-white');
            reservationsBtn.classList.add('bg-gray-300', 'text-gray-700');
        }
    }

    todayBtn.addEventListener('click', function() { showTable('today'); });
    reservationsBtn.addEventListener('click', function() { showTable('reservations'); });

    // On page load, show the correct table based on active_table param
    document.addEventListener('DOMContentLoaded', function() {
        const params = new URLSearchParams(window.location.search);
        const activeTable = params.get('active_table');
        showTable(activeTable === 'reservations' ? 'reservations' : 'today');
    });
});
