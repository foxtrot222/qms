export function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

export function initLogoutButtons() {
    const userLogoutBtn = document.getElementById('userLogoutBtn');
    if (userLogoutBtn) {
        userLogoutBtn.addEventListener('click', () => {
            window.location.href = '/user/logout';
        });
    }

    const orgLogoutBtn = document.getElementById('orgLogoutBtn');
    if (orgLogoutBtn) {
        orgLogoutBtn.addEventListener('click', () => {
            window.location.href = '/org/logout';
        });
    }
    
    const adminLogoutBtn = document.getElementById('adminLogoutBtn');
    if(adminLogoutBtn) {
        adminLogoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = '/admin/logout';
        });
    }
}
