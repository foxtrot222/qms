/**
 * Handles click events for the role selection buttons.
 */
document.addEventListener('DOMContentLoaded', () => {
    const customerButton = document.getElementById('customer-btn');
    const serviceProviderButton = document.getElementById('provider-btn');
    const messageContainer = document.getElementById('message-container');

    if (customerButton && serviceProviderButton && messageContainer) {
        customerButton.addEventListener('click', () => {
            messageContainer.textContent = 'Welcome, Customer!';
        });

        serviceProviderButton.addEventListener('click', () => {
            messageContainer.textContent = 'Welcome, Service Provider!';
        });
    }
});