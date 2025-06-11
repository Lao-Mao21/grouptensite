document.addEventListener('DOMContentLoaded', function () {
    // Annual Revenue Chart
    const annualCtx = document.getElementById('annualRevenueChart');
    if (annualCtx) {
        const annualData = JSON.parse(document.getElementById('annual-data').textContent);
        const months = JSON.parse(document.getElementById('months-data').textContent);
        
        new Chart(annualCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'Single',
                        data: annualData.single,
                        backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    },
                    {
                        label: 'Double',
                        data: annualData.double,
                        backgroundColor: 'rgba(22, 163, 74, 0.7)',
                    },
                    {
                        label: 'Suite',
                        data: annualData.suite,
                        backgroundColor: 'rgba(234, 179, 8, 0.7)',
                    },
                    {
                        label: 'Deluxe',
                        data: annualData.deluxe,
                        backgroundColor: 'rgba(6, 182, 212, 0.7)',
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Monthly Top Sales Pie Chart
    const pieCtx = document.getElementById('monthlyTopSalesChart');
    if (pieCtx) {
        const pieData = JSON.parse(document.getElementById('pie-data').textContent);
        const roomTypes = JSON.parse(document.getElementById('room-types-data').textContent);

        new Chart(pieCtx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: roomTypes.map(rt => rt.charAt(0).toUpperCase() + rt.slice(1)),
                datasets: [{
                    data: pieData,
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.7)',
                        'rgba(22, 163, 74, 0.7)',
                        'rgba(234, 179, 8, 0.7)',
                        'rgba(6, 182, 212, 0.7)'
                    ],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        });
    }
});