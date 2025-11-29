document.addEventListener('DOMContentLoaded', function() {
    // Bar chart for severity distribution
    const ctxBar = document.getElementById('severityChart').getContext('2d');
    new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: ['Low', 'Medium', 'High', 'Critical'],
            datasets: [{
                label: 'Incidents',
                data: [50, 100, 75, 25],
                backgroundColor: ['#3b82f6', '#eab308', '#f97316', '#ef4444'],
                borderColor: ['#3b82f6', '#eab308', '#f97316', '#ef4444'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Line chart for trends
    const ctxLine = document.getElementById('trendsChart').getContext('2d');
    new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Incidents',
                data: [20, 35, 50, 40],
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});