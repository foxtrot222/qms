import { api } from '../api.js';

export function initTokenModal() {
    const generateTokenBtn = document.getElementById('generateTokenBtn');
    if (!generateTokenBtn) return;

    const tokenModal = document.getElementById('tokenModal');
    const modalContent = document.getElementById('modal-content');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const tokenForm = document.getElementById('tokenForm');
    const emailOption = document.getElementById('emailOption');
    const consumerIdOption = document.getElementById('consumerIdOption');
    const emailInputContainer = document.getElementById('emailInputContainer');
    const consumerIdInputContainer = document.getElementById('consumerIdInputContainer');
    const serviceSelect = document.getElementById('service');

    if (emailOption && consumerIdOption) {
        emailOption.addEventListener('change', () => {
            emailInputContainer.classList.remove('hidden');
            consumerIdInputContainer.classList.add('hidden');
            document.getElementById('emailAddress').required = true;
            document.getElementById('consumerId').required = false;
        });

        consumerIdOption.addEventListener('change', () => {
            consumerIdInputContainer.classList.remove('hidden');
            emailInputContainer.classList.add('hidden');
            document.getElementById('consumerId').required = true;
            document.getElementById('emailAddress').required = false;
        });
    }

    async function loadServices() {
        try {
            const data = await api.getServices();
            if (data.success) {
                serviceSelect.innerHTML = '';
                data.services.forEach(service => {
                    const option = document.createElement('option');
                    option.value = service.id;
                    option.textContent = service.name;
                    serviceSelect.appendChild(option);
                });
            } else {
                console.error('Failed to load services:', data.error);
            }
        } catch (error) {
            console.error('Error loading services:', error);
        }
    }

    const openTokenModal = () => {
        tokenModal.classList.remove('hidden');
        setTimeout(() => {
            tokenModal.style.opacity = '1';
            modalContent.classList.remove('scale-95', 'opacity-0');
        }, 10);
        loadServices();
    };

    const closeTokenModal = () => {
        modalContent.classList.add('scale-95', 'opacity-0');
        tokenModal.style.opacity = '0';
        setTimeout(() => tokenModal.classList.add('hidden'), 300);
    };

    generateTokenBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openTokenModal();
    });

    closeModalBtn.addEventListener('click', closeTokenModal);
    tokenModal.addEventListener('click', (e) => {
        if (e.target === tokenModal) closeTokenModal();
    });

    tokenForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitButton = e.target.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.textContent = 'Generating...';
        submitButton.disabled = true;

        const formData = new FormData(tokenForm);
        try {
            const data = await api.generateToken(formData);
            if (data.success) {
                submitButton.textContent = `Your Token: ${data.token}`;
                submitButton.classList.replace('bg-blue-600', 'bg-green-500');
                submitButton.classList.replace('hover:bg-blue-700', 'bg-green-500');
                setTimeout(() => {
                    closeTokenModal();
                    tokenForm.reset();
                    submitButton.textContent = originalButtonText;
                    submitButton.classList.replace('bg-green-500', 'bg-blue-600');
                    submitButton.classList.add('hover:bg-blue-700');
                    submitButton.disabled = false;
                }, 5000);
            } else {
                alert(`Error: ${data.error}`);
                submitButton.textContent = originalButtonText;
                submitButton.disabled = false;
            }
        } catch (error) {
            alert('An error occurred while generating the token.');
            submitButton.textContent = originalButtonText;
            submitButton.disabled = false;
        }
    });
}
