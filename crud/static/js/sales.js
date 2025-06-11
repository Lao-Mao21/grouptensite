document.addEventListener('DOMContentLoaded', function () {
    // Annual Revenue Chart
    const annualCtx = document.getElementById('annualRevenueChart');
    if (annualCtx) {
        const annualData = JSON.parse(document.getElementById('annual-data').textContent);
        const months = JSON.parse(document.getElementById('months-data').textContent);
        const roomTypes = JSON.parse(document.getElementById('room-types-data').textContent);
        
        const datasets = roomTypes.map((roomType, index) => {
            const colors = [
                'rgba(59, 130, 246, 0.7)',
                'rgba(22, 163, 74, 0.7)',
                'rgba(234, 179, 8, 0.7)',
                'rgba(6, 182, 212, 0.7)'
            ];
            return {
                label: roomType.charAt(0).toUpperCase() + roomType.slice(1),
                data: annualData[roomType] || [],
                backgroundColor: colors[index % colors.length],
            };
        });

        new Chart(annualCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: months,
                datasets: datasets
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
        const pieLabels = JSON.parse(document.getElementById('pie-labels').textContent);
        const pieValues = JSON.parse(document.getElementById('pie-values').textContent);

        new Chart(pieCtx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: pieLabels,
                datasets: [{
                    data: pieValues,
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