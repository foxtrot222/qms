import { api } from './api.js';
import { initMobileMenu, initLogoutButtons } from './ui.js';
import { initTokenModal } from './components/tokenModal.js';
import { initStatusModal } from './components/statusModal.js';
import { initChoiceModal } from './components/choiceModal.js';
import { initStatusPage } from './pages/statusPage.js';
import { initDashboardPage } from './pages/dashboardPage.js';
import { initAdminPage } from './pages/adminPage.js';
import { initOrganizationPage } from './pages/organizationPage.js';


document.addEventListener('DOMContentLoaded', () => {
    // Initialize components that are on every page
    initMobileMenu();
    initLogoutButtons();

    // Initialize components for the main/home page
    if (document.getElementById('homePage')) {
        initTokenModal(api);
        initStatusModal(api);
        initChoiceModal(api);
    }

    // Initialize page-specific logic
    initStatusPage(api);
    initDashboardPage(api);
    initAdminPage(api);
    initOrganizationPage(api);
});
