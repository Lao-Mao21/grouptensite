// Table filtering functionality
function setupTableFilter(tableId, inputId) {
    const filterInput = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!filterInput || !table) return;

    filterInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

        for (let row of rows) {
            let text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchText) ? '' : 'none';
        }

        // Show "no results" row if all rows are hidden
        let visibleRows = 0;
        for (let row of rows) {
            if (row.style.display !== 'none') visibleRows++;
        }

        // Get or create the "no results" row
        let noResultsRow = table.querySelector('.no-results-row');
        if (!noResultsRow) {
            noResultsRow = document.createElement('tr');
            noResultsRow.className = 'no-results-row';
            const td = document.createElement('td');
            td.setAttribute('colspan', '10'); // Large enough for all columns
            td.className = 'text-center py-4 text-gray-500';
            td.textContent = 'No matching results found';
            noResultsRow.appendChild(td);
            table.getElementsByTagName('tbody')[0].appendChild(noResultsRow);
        }
        noResultsRow.style.display = visibleRows === 0 ? '' : 'none';
    });
}

// Initialize all table filters when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Setup filters for manage_rooms tables
    setupTableFilter('rooms-table', 'rooms-filter');
    
    // Setup filters for manage_guests tables
    setupTableFilter('today-bookings-table', 'today-bookings-filter');
    setupTableFilter('reservations-table', 'reservations-filter');
}); 