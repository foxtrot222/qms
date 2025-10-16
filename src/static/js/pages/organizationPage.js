import { api } from '../api.js';

function initLoginModal(buttonId, modalId, closeBtnId, contentId, formId, errorId, loginFn) {
    const openBtn = document.getElementById(buttonId);
    const modal = document.getElementById(modalId);
    const closeBtn = document.getElementById(closeBtnId);
    const content = document.getElementById(contentId);
    const form = document.getElementById(formId);
    const errorEl = document.getElementById(errorId);

    if (!openBtn || !modal || !closeBtn || !content || !form || !errorEl) return;

    const open = (e) => {
        e.preventDefault(); // stop <a> from navigating away

        // Force cancel any pending navigation (in case href points to a real route)
        if (openBtn.tagName === 'a') openBtn.setAttribute('href', '#');

        // Now show the modal
        modal.classList.remove('hidden');
        requestAnimationFrame(() => {
            modal.style.opacity = '1';
            content.classList.remove('scale-95', 'opacity-0');
        });
    };

    const close = () => {
        content.classList.add('scale-95', 'opacity-0');
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.classList.add('hidden');
            errorEl.classList.add('hidden');
            errorEl.textContent = '';
            form.reset();
        }, 300);
    };

    openBtn.addEventListener('click', open);
    closeBtn.addEventListener('click', (e) => { e.preventDefault(); close(); });
    modal.addEventListener('click', (e) => { if (e.target === modal) close(); });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitButton = e.target.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.textContent = 'Logging in...';
        submitButton.disabled = true;
        errorEl.classList.add('hidden');

        const formData = new FormData(form);
        try {
            const data = await loginFn(formData);
            if (data.success) {
                window.location.href = data.redirect;
            } else {
                errorEl.textContent = data.error || 'An unknown error occurred.';
                errorEl.classList.remove('hidden');
                submitButton.textContent = originalButtonText;
                submitButton.disabled = false;
            }
        } catch (error) {
            errorEl.textContent = 'An error occurred. Please try again.';
            errorEl.classList.remove('hidden');
            submitButton.textContent = originalButtonText;
            submitButton.disabled = false;
        }
    });
}

export function initOrganizationPage() {
    if (!document.getElementById('organizationPage')) return;

    initLoginModal(
        'accessDashboardBtn',
        'officerLoginModal',
        'closeOfficerLoginModalBtn',
        'officer-login-modal-content',
        'officerLoginForm',
        'officerLoginError',
        api.officerLogin
    );

    initLoginModal(
        'adminLoginBtn',
        'adminLoginModal',
        'closeAdminLoginModalBtn',
        'admin-login-modal-content',
        'adminLoginForm',
        'adminLoginError',
        (formData) => {
            const plainFormData = Object.fromEntries(formData.entries());
            const body = {
                adminID: plainFormData.adminId,
                adminPassword: plainFormData.adminPassword
            };
            return api.adminLogin(body);
        }
    );
}

// Auto-initialize when loaded directly (not through main.js)
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initOrganizationPage);
} else {
    initOrganizationPage();
}
