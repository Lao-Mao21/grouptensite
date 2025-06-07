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

// Get data from Django context
const months = JSON.parse(document.getElementById('months-data').textContent);
const annualData = JSON.parse(document.getElementById('annual-data').textContent);
const pieData = JSON.parse(document.getElementById('pie-data').textContent);

// Calculate percentages for pie chart
const totalPie = pieData.reduce((a, b) => a + b, 0);
const piePercentages = pieData.map(value => ((value / totalPie) * 100).toFixed(1));

// Helper function to capitalize first letter
const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);

// Update percentage displays
document.getElementById('single-percentage').textContent = `${piePercentages[0]}%`;
document.getElementById('double-percentage').textContent = `${piePercentages[1]}%`;
document.getElementById('suite-percentage').textContent = `${piePercentages[2]}%`;
document.getElementById('deluxe-percentage').textContent = `${piePercentages[3]}%`;

// Annual Revenue Bar Chart
new Chart(document.getElementById('annualRevenueChart'), {
    type: 'bar',
    data: {
        labels: months,
        datasets: [
            { 
                label: capitalize('single'), 
                backgroundColor: '#3737ff', 
                data: annualData['single'],
                borderRadius: 4
            },
            { 
                label: capitalize('double'), 
                backgroundColor: '#00ff00', 
                data: annualData['double'],
                borderRadius: 4
            },
            { 
                label: capitalize('suite'), 
                backgroundColor: '#eab308', 
                data: annualData['suite'],
                borderRadius: 4
            },
            { 
                label: capitalize('deluxe'), 
                backgroundColor: '#00e6e6', 
                data: annualData['deluxe'],
                borderRadius: 4
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += new Intl.NumberFormat('en-PH', {
                                style: 'currency',
                                currency: 'PHP'
                            }).format(context.parsed.y);
                        }
                        return label;
                    }
                }
            }
        },
        scales: { 
            y: { 
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return new Intl.NumberFormat('en-PH', {
                            style: 'currency',
                            currency: 'PHP',
                            maximumSignificantDigits: 3
                        }).format(value);
                    }
                }
            }
        }
    }
});

// Monthly Top Sales Pie Chart
new Chart(document.getElementById('monthlyTopSalesChart'), {
    type: 'pie',
    data: {
        labels: ['Single', 'Double', 'Suite', 'Deluxe'],
        datasets: [{
            data: piePercentages,
            backgroundColor: ['#3737ff', '#00ff00', '#eab308', '#00e6e6']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const value = context.raw;
                        const label = context.label || '';
                        return `${label}: ${value}%`;
                    }
                }
            }
        }
    }
});