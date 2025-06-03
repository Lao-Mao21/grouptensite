// Chart.js scripts (replace with your real data)
 // Annual Revenue Bar Chart (dummy data)
new Chart(document.getElementById('annualRevenueChart'), {
    type: 'bar',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [
            { label: 'FAMILY', backgroundColor: '#3737ff', data: [340, 290, 300, 310, 400, 200, 0, 0, 0, 0, 0, 0] },
            { label: 'VIP', backgroundColor: '#00ff00', data: [150, 200, 250, 300, 500, 100, 0, 0, 0, 0, 0, 0] },
            { label: 'Deluxe', backgroundColor: '#00e6e6', data: [180, 210, 320, 280, 300, 250, 0, 0, 0, 0, 0, 0] }
        ]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
    }
});

// Monthly Top Sales Pie Chart (dummy data)
new Chart(document.getElementById('monthlyTopSalesChart'), {
    type: 'pie',
    data: {
        labels: ['FAMILY', 'VIP', 'Deluxe'],
        datasets: [{
            data: [43, 20, 37],
            backgroundColor: ['#3737ff', '#00ff00', '#00e6e6']
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } }
    }
});

// Replace dummy data with Django context data
const months = JSON.parse(document.getElementById('months-data').textContent);
const annualData = JSON.parse(document.getElementById('annual-data').textContent);
const pieData = JSON.parse(document.getElementById('pie-data').textContent);

// Update Annual Revenue Chart
const annualRevenueChart = new Chart(document.getElementById('annualRevenueChart'), {
    type: 'bar',
    data: {
        labels: months,
        datasets: [
            { label: 'FAMILY', backgroundColor: '#3737ff', data: annualData.family },
            { label: 'VIP', backgroundColor: '#00ff00', data: annualData.vip },
            { label: 'Deluxe', backgroundColor: '#00e6e6', data: annualData.deluxe }
        ]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
    }
});

// Update Monthly Top Sales Chart
const monthlyTopSalesChart = new Chart(document.getElementById('monthlyTopSalesChart'), {
    type: 'pie',
    data: {
        labels: ['FAMILY', 'VIP', 'Deluxe'],
        datasets: [{
            data: [pieData.family, pieData.vip, pieData.deluxe],
            backgroundColor: ['#3737ff', '#00ff00', '#00e6e6']
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } }
    }
});