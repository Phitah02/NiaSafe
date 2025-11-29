// Manage alerts - static implementation
document.addEventListener('DOMContentLoaded', function() {
    // Initialize alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Add dismiss functionality if needed
        const dismissBtn = alert.querySelector('.dismiss-btn');
        if (dismissBtn) {
            dismissBtn.addEventListener('click', () => {
                alert.style.display = 'none';
            });
        }
    });
});