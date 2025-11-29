async function submitComment(comment) {
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ comment: comment })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        updateResults(data);
    } catch (error) {
        console.error('Error submitting comment:', error);
        alert('An error occurred while analyzing the comment. Please try again.');
    }
}

function updateResults(data) {
    const resultsContainer = document.getElementById('results-container');
    const placeholder = document.getElementById('results-placeholder');
    const grid = document.getElementById('results-grid');
    const chartCanvas = document.getElementById('resultsChart');

    // Hide placeholder and show grid
    placeholder.style.display = 'none';
    grid.style.display = 'grid';

    // Clear previous results
    grid.innerHTML = '';

    // Categories and their display names
    const categories = [
        { key: 'toxic', label: 'Toxic', color: 'red' },
        { key: 'severe_toxic', label: 'Severe Toxic', color: 'orange' },
        { key: 'obscene', label: 'Obscene', color: 'purple' },
        { key: 'threat', label: 'Threat', color: 'red' },
        { key: 'insult', label: 'Insult', color: 'yellow' },
        { key: 'identity_hate', label: 'Identity Hate', color: 'pink' }
    ];

    // Create cards for each category
    categories.forEach(cat => {
        const probability = (data[cat.key] * 100).toFixed(1);
        const card = document.createElement('div');
        card.className = 'flex flex-col gap-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 p-4';
        card.innerHTML = `
            <div class="flex items-center justify-between">
                <p class="font-semibold text-gray-800 dark:text-gray-200">${cat.label}</p>
                <p class="font-bold text-${cat.color}-500">${probability}%</p>
            </div>
            <div class="h-2 w-full rounded-full bg-gray-200 dark:bg-gray-700">
                <div class="h-2 rounded-full bg-${cat.color}-500" style="width: ${probability}%;"></div>
            </div>
        `;
        grid.appendChild(card);
    });

    // Initialize Chart.js bar chart
    const ctx = chartCanvas.getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories.map(cat => cat.label),
            datasets: [{
                label: 'Probability (%)',
                data: categories.map(cat => (data[cat.key] * 100).toFixed(1)),
                backgroundColor: categories.map(cat => `rgba(${getColorRGBA(cat.color)}, 0.6)`),
                borderColor: categories.map(cat => `rgba(${getColorRGBA(cat.color)}, 1)`),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

function getColorRGBA(color) {
    const colors = {
        red: '220, 38, 38',
        orange: '249, 115, 22',
        purple: '147, 51, 234',
        yellow: '234, 179, 8',
        pink: '236, 72, 153'
    };
    return colors[color] || '156, 163, 175'; // default gray
}