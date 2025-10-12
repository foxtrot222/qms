import { api } from '../api.js';

function initSettingsSlider() {
    const latenessFactor = document.getElementById('lateness-factor');
    const latenessValue = document.getElementById('lateness-value');
    if (latenessFactor && latenessValue) {
        latenessFactor.addEventListener('input', () => {
            latenessValue.textContent = latenessFactor.value;
        });
    }
}

function initModal(buttonId, modalId, closeBtnId, modalContentId) {
    const openBtn = document.getElementById(buttonId);
    const modal = document.getElementById(modalId);
    const closeBtn = document.getElementById(closeBtnId);
    const content = document.getElementById(modalContentId);

    if (!openBtn || !modal || !closeBtn || !content) return;

    const open = () => {
        modal.classList.remove('hidden');
        setTimeout(() => {
            modal.style.opacity = '1';
            content.classList.remove('scale-95', 'opacity-0');
        }, 10);
    };

    const close = () => {
        content.classList.add('scale-95', 'opacity-0');
        modal.style.opacity = '0';
        setTimeout(() => modal.classList.add('hidden'), 300);
    };

    openBtn.addEventListener('click', open);
    closeBtn.addEventListener('click', close);
    modal.addEventListener('click', (e) => { if (e.target === modal) close(); });

    return { open, close };
}

function initEditUserModal() {
    const modal = initModal(null, 'editUserModal', 'closeEditUserModalBtn', 'edit-user-modal-content');
    if (!modal) return;

    document.querySelectorAll('.edit-user-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const userId = e.target.dataset.userId;
            try {
                const data = await api.getUserData(userId);
                if (data.success) {
                    document.getElementById('editUserId').value = data.user.id;
                    document.getElementById('editUserName').value = data.user.name;
                    document.getElementById('editOfficerID').value = data.user.officerID;
                    document.getElementById('editUserServiceId').value = data.user.service_id;
                    modal.open();
                } else {
                    alert(`Error: ${data.error}`);
                }
            } catch (error) {
                alert('An error occurred while fetching user data.');
            }
        });
    });
}

function initEditServiceModal() {
    const modal = initModal(null, 'editServiceModal', 'closeEditServiceModalBtn', 'edit-service-modal-content');
    if (!modal) return;

    document.querySelectorAll('.edit-service-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const serviceId = e.target.dataset.serviceId;
            try {
                const data = await api.getServiceData(serviceId);
                if (data.success) {
                    document.getElementById('editServiceId').value = data.service.id;
                    document.getElementById('editServiceName').value = data.service.name;
                    modal.open();
                } else {
                    alert(`Error: ${data.error}`);
                }
            } catch (error) {
                alert('An error occurred while fetching service data.');
            }
        });
    });
}

export function initAdminPage() {
    if (!document.querySelector('h1.text-blue-600')?.textContent.includes('QMS Admin')) return;

    initSettingsSlider();
    initModal('addUserBtn', 'addUserModal', 'closeAddUserModalBtn', 'add-user-modal-content');
    initModal('addServiceBtn', 'addServiceModal', 'closeAddServiceModalBtn', 'add-service-modal-content');
    initEditUserModal();
    initEditServiceModal();
}
