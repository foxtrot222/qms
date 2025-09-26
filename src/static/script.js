// === Global Variables & Helpers ===
let isFirstTimeTestUser = true;
let etrTimerInterval;

// === Page Navigation ===
const homePage = document.getElementById('homePage');
const organizationPage = document.getElementById('organizationPage');
const orgNavBtn = document.getElementById('orgNavBtn');
const orgNavBtnMobile = document.getElementById('orgNavBtnMobile');
const homeLinkStatusPage = document.getElementById('homeLinkStatusPage');

if (orgNavBtn) {
    orgNavBtn.addEventListener('click', (e) => { 
        e.preventDefault(); 
        if(homePage) homePage.classList.add('hidden');
        if(organizationPage) organizationPage.classList.remove('hidden');
    });
}
if (orgNavBtnMobile) {
    orgNavBtnMobile.addEventListener('click', (e) => { 
        e.preventDefault(); 
        if(homePage) homePage.classList.add('hidden');
        if(organizationPage) organizationPage.classList.remove('hidden');
        if(mobileMenu) mobileMenu.classList.add('hidden');
    });
}
if (homeLinkStatusPage) {
    homeLinkStatusPage.addEventListener('click', (e) => { 
        e.preventDefault();
        window.location.href = '/';
    });
}


// === Mobile Menu ===
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');
if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
}

// === Token Generation Modal Logic ===
const generateTokenBtn = document.getElementById('generateTokenBtn');
const tokenModal = document.getElementById('tokenModal');
const modalContent = document.getElementById('modal-content');
const closeModalBtn = document.getElementById('closeModalBtn');
const tokenForm = document.getElementById('tokenForm');
const notificationRadios = document.querySelectorAll('input[name="notification"]');
const smsInputContainer = document.getElementById('smsInputContainer');
const emailInputContainer = document.getElementById('emailInputContainer');

if (generateTokenBtn) {
    const openTokenModal = () => { tokenModal.classList.remove('hidden'); setTimeout(() => { tokenModal.style.opacity = '1'; modalContent.classList.remove('scale-95', 'opacity-0'); }, 10); };
    const closeTokenModal = () => { modalContent.classList.add('scale-95', 'opacity-0'); tokenModal.style.opacity = '0'; setTimeout(() => tokenModal.classList.add('hidden'), 300); };
    generateTokenBtn.addEventListener('click', (e) => { e.preventDefault(); openTokenModal(); });
    closeModalBtn.addEventListener('click', closeTokenModal);
    tokenModal.addEventListener('click', (e) => { if (e.target === tokenModal) closeTokenModal(); });
    notificationRadios.forEach(radio => { radio.addEventListener('change', (e) => { smsInputContainer.classList.toggle('hidden', e.target.value !== 'sms'); emailInputContainer.classList.toggle('hidden', e.target.value !== 'email'); }); });
    tokenForm.addEventListener('submit', (e) => { e.preventDefault(); const submitButton = e.target.querySelector('button[type="submit"]'); submitButton.textContent = 'Token Sent!'; submitButton.classList.replace('bg-blue-600', 'bg-green-500'); submitButton.classList.replace('hover:bg-blue-700', 'bg-green-500'); setTimeout(() => { closeTokenModal(); tokenForm.reset(); setTimeout(() => { submitButton.textContent = 'Generate Token'; submitButton.classList.replace('bg-green-500', 'bg-blue-600'); submitButton.classList.add('hover:bg-blue-700'); }, 500); }, 2000); });
}

// === Status Check Modal Logic ===
const checkStatusBtn = document.getElementById('checkStatusBtn');
const statusNavBtn = document.getElementById('statusNavBtn');
const statusNavBtnMobile = document.getElementById('statusNavBtnMobile');
const statusModal = document.getElementById('statusModal');
const statusModalContent = document.getElementById('status-modal-content');
const closeStatusModalBtn = document.getElementById('closeStatusModalBtn');
const statusForm = document.getElementById('statusForm');
const getOtpBtn = document.getElementById('getOtpBtn');
const otpInputContainer = document.getElementById('otpInputContainer');
const checkStatusSubmitBtn = document.getElementById('checkStatusSubmitBtn');

if (checkStatusBtn) {
    const openStatusModal = () => { statusModal.classList.remove('hidden'); setTimeout(() => { statusModal.style.opacity = '1'; statusModalContent.classList.remove('scale-95', 'opacity-0'); }, 10); };
    const closeStatusModal = () => { statusModalContent.classList.add('scale-95', 'opacity-0'); statusModal.style.opacity = '0'; setTimeout(() => { statusModal.classList.add('hidden'); otpInputContainer.classList.add('hidden'); checkStatusSubmitBtn.classList.add('hidden'); getOtpBtn.classList.remove('hidden'); statusForm.reset(); }, 300); };
    checkStatusBtn.addEventListener('click', (e) => { e.preventDefault(); openStatusModal(); });
    statusNavBtn.addEventListener('click', (e) => { e.preventDefault(); openStatusModal(); });
    statusNavBtnMobile.addEventListener('click', (e) => { e.preventDefault(); openStatusModal(); mobileMenu.classList.add('hidden'); });
    closeStatusModalBtn.addEventListener('click', closeStatusModal);
    statusModal.addEventListener('click', (e) => { if (e.target === statusModal) closeStatusModal(); });
    getOtpBtn.addEventListener('click', (e) => { e.preventDefault(); otpInputContainer.classList.remove('hidden'); checkStatusSubmitBtn.classList.remove('hidden'); getOtpBtn.classList.add('hidden'); });
}

// === Officer Login Modal Logic ===
const accessDashboardBtn = document.getElementById('accessDashboardBtn');
const officerLoginModal = document.getElementById('officerLoginModal');
const officerLoginModalContent = document.getElementById('officer-login-modal-content');
const closeOfficerLoginModalBtn = document.getElementById('closeOfficerLoginModalBtn');
const officerLoginForm = document.getElementById('officerLoginForm');
const officerLoginError = document.querySelector('#officerLoginError');

if (accessDashboardBtn) {
    const openModal = () => { 
        officerLoginModal.classList.remove('hidden'); 
        setTimeout(() => { 
            officerLoginModal.style.opacity = '1'; 
            officerLoginModalContent.classList.remove('scale-95', 'opacity-0'); 
        }, 10); 
    };
    const closeModal = () => { 
        officerLoginModalContent.classList.add('scale-95', 'opacity-0'); 
        officerLoginModal.style.opacity = '0'; 
        setTimeout(() => officerLoginModal.classList.add('hidden'), 300); 
    };

    accessDashboardBtn.addEventListener('click', e => { e.preventDefault(); openModal(); });
    closeOfficerLoginModalBtn.addEventListener('click', closeModal);
    officerLoginModal.addEventListener('click', e => { if (e.target === officerLoginModal) closeModal(); });

    officerLoginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        officerLoginError.classList.add('hidden');

        const officerId = document.getElementById('officerId').value.trim();
        const officerPassword = document.getElementById('officerPassword').value;
        const submitBtn = officerLoginForm.querySelector('button[type="submit"]');

        if (!officerId || !officerPassword) {
            officerLoginError.textContent = "Provide both ID and password.";
            officerLoginError.classList.remove('hidden');
            return;
        }

        submitBtn.textContent = "Logging in...";

        try {
            const formData = new FormData();
            formData.append('officerId', officerId);
            formData.append('officerPassword', officerPassword);

            const response = await fetch('/login', { method: 'POST', body: formData });
            const data = await response.json();

            if (data.success) {
                // Store officer info in sessionStorage
                sessionStorage.setItem('officerName', data.officerName);
                sessionStorage.setItem('officerId', officerId); // store ID for dashboard

                // Redirect to dashboard
                window.location.href = data.redirect;
            } 
            else {
                officerLoginError.textContent = data.error;
                officerLoginError.classList.remove('hidden');
                submitBtn.textContent = "Login";
            }

        } catch (err) {
            officerLoginError.textContent = "Login failed. Try again.";
            officerLoginError.classList.remove('hidden');
            submitBtn.textContent = "Login";
            console.error(err);
        }
    });

}





// === Officer Dashboard Logic ===
const customerTimerEl = document.getElementById('customerTimer');
const callNextBtn = document.getElementById('callNextBtn');
const customerCountEl = document.getElementById('customerCount');
if (customerTimerEl) {
    let timerInterval; let seconds = 0;
    function formatTime(sec) { const minutes = Math.floor(sec / 60).toString().padStart(2, '0'); const secondsValue = (sec % 60).toString().padStart(2, '0'); return `${minutes}:${secondsValue}`; }
    function startCustomerTimer() { if (timerInterval) clearInterval(timerInterval); seconds = 0; customerTimerEl.textContent = formatTime(seconds); timerInterval = setInterval(() => { seconds++; customerTimerEl.textContent = formatTime(seconds); }, 1000); }
    startCustomerTimer();
    callNextBtn.addEventListener('click', () => { const nowServing = document.getElementById('nowServingToken'); const queueList = document.getElementById('queueList'); const nextCustomer = queueList.querySelector('li'); if (nextCustomer) { nowServing.textContent = nextCustomer.querySelector('span:first-child').textContent; nextCustomer.remove(); customerCountEl.textContent = queueList.children.length; } else { nowServing.textContent = "---"; customerCountEl.textContent = 0; } startCustomerTimer(); });
}


// === Appointment/Walk-in Modal Logic ===
const appointmentModal = document.getElementById('appointmentModal');
const appointmentModalContent = document.getElementById('appointment-modal-content');
const joinWalkInBtn = document.getElementById('joinWalkInBtn');
const bookAppointmentBtn = document.getElementById('bookAppointmentBtn');

if (appointmentModal) {
    const openAppointmentModal = () => { appointmentModal.classList.remove('hidden'); setTimeout(() => { appointmentModal.style.opacity = '1'; appointmentModalContent.classList.remove('scale-95', 'opacity-0'); }, 10); };
    const closeAppointmentModal = () => { appointmentModalContent.classList.add('scale-95', 'opacity-0'); appointmentModal.style.opacity = '0'; setTimeout(() => appointmentModal.classList.add('hidden'), 300); };
    joinWalkInBtn.addEventListener('click', () => { closeAppointmentModal(); setTimeout(() => { window.location.href = '/status'; }, 350); });
    bookAppointmentBtn.addEventListener('click', () => {
        closeAppointmentModal();
        setTimeout(() => {
            window.location.href = '/status';
        }, 350);
    });
}


// === Status Page Logic ===
const etrTimerEl = document.getElementById('etrTimer');
const etrMessageEl = document.getElementById('etrMessage');
const checkInBtn = document.getElementById('checkInBtn');
const viewMapBtn = document.getElementById('viewMapBtn');

if (etrTimerEl) {
    function formatTime(sec) { const minutes = Math.floor(sec / 60).toString().padStart(2, '0'); const secondsValue = (sec % 60).toString().padStart(2, '0'); return `${minutes}:${secondsValue}`; }
    function startETRTimer(duration) {
        let timer = duration; if (etrTimerInterval) clearInterval(etrTimerInterval);
        etrTimerEl.textContent = formatTime(timer); // Initialize display
        etrTimerInterval = setInterval(() => {
            etrTimerEl.textContent = formatTime(timer);
            if (--timer < 0) { clearInterval(etrTimerInterval); etrTimerEl.textContent = "00:00"; etrMessageEl.textContent = "It's your turn!"; }
        }, 1000);
    }
    checkInBtn.addEventListener('click', () => { checkInBtn.textContent = 'Checked-in Successfully!'; checkInBtn.classList.replace('bg-green-500', 'bg-green-600'); checkInBtn.disabled = true; });
    
    // Dummy data for demonstration
    const data = { name: 'John Doe', contact: '909******', service: 'General Inquiry', position: '3rd in line', etr: 15 * 60 };
    document.getElementById('statusName').textContent = data.name; 
    document.getElementById('statusContact').textContent = data.contact; 
    document.getElementById('statusService').textContent = data.service; 
    document.getElementById('statusPosition').textContent = data.position;
    startETRTimer(data.etr);
}


// === Map Modal Logic ===
const mapModal = document.getElementById('mapModal');
const mapModalContent = document.getElementById('map-modal-content');
const closeMapModalBtn = document.getElementById('closeMapModalBtn');
if (viewMapBtn) {
    const openMapModal = () => { mapModal.classList.remove('hidden'); setTimeout(() => { mapModal.style.opacity = '1'; mapModalContent.classList.remove('scale-95', 'opacity-0'); }, 10); };
    const closeMapModal = () => { mapModalContent.classList.add('scale-95', 'opacity-0'); mapModal.style.opacity = '0'; setTimeout(() => mapModal.classList.add('hidden'), 300); };
    viewMapBtn.addEventListener('click', openMapModal);
    closeMapModalBtn.addEventListener('click', closeMapModal);
    mapModal.addEventListener('click', (e) => { if (e.target === mapModal) closeMapModal(); });
}

// === Main Form Submission Logic ===
if (statusForm) {
    statusForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const tokenInput = document.getElementById('token').value;
        const otpInput = document.getElementById('otp').value;

        if (tokenInput.toLowerCase() === 'test' && otpInput === '0') {
            if (isFirstTimeTestUser) {
                isFirstTimeTestUser = false;
                const closeStatusModal = () => { statusModalContent.classList.add('scale-95', 'opacity-0'); statusModal.style.opacity = '0'; setTimeout(() => { statusModal.classList.add('hidden'); otpInputContainer.classList.add('hidden'); checkStatusSubmitBtn.classList.add('hidden'); getOtpBtn.classList.remove('hidden'); statusForm.reset(); }, 300); };
                const openAppointmentModal = () => { appointmentModal.classList.remove('hidden'); setTimeout(() => { appointmentModal.style.opacity = '1'; appointmentModalContent.classList.remove('scale-95', 'opacity-0'); }, 10); };
                closeStatusModal();
                setTimeout(openAppointmentModal, 350);
            } else {
                const closeStatusModal = () => { statusModalContent.classList.add('scale-95', 'opacity-0'); statusModal.style.opacity = '0'; setTimeout(() => { statusModal.classList.add('hidden'); otpInputContainer.classList.add('hidden'); checkStatusSubmitBtn.classList.add('hidden'); getOtpBtn.classList.remove('hidden'); statusForm.reset(); }, 300); };
                closeStatusModal();
                setTimeout(() => {
                    window.location.href = '/status';
                }, 350);
            }
            return;
        }
        
        // This is a simulation, so we don't use a real alert.
        // In a real app, you would handle this with a message on the modal.
        const submitBtn = document.getElementById('checkStatusSubmitBtn');
        submitBtn.textContent = 'Verifying...';
        setTimeout(() => {
             console.log("Invalid Token/OTP (simulation)");
             // You could show an error message here.
             submitBtn.textContent = 'Go to Status Page';
             // For now, we'll just close it.
             const closeStatusModal = () => { statusModalContent.classList.add('scale-95', 'opacity-0'); statusModal.style.opacity = '0'; setTimeout(() => { statusModal.classList.add('hidden'); otpInputContainer.classList.add('hidden'); checkStatusSubmitBtn.classList.add('hidden'); getOtpBtn.classList.remove('hidden'); statusForm.reset(); }, 300); };
             closeStatusModal();
        }, 1500);
    });
}

// Auto-open officer login modal if there is a flash message
document.addEventListener("DOMContentLoaded", function() {
    const flashMsgDiv = document.querySelector('#officerLoginModal .text-red-600');
    if (flashMsgDiv && flashMsgDiv.textContent.trim() !== "") {
        const modal = document.getElementById("officerLoginModal");
        const modalContent = document.getElementById("officer-login-modal-content");

        modal.classList.remove("hidden");
        modalContent.classList.remove("scale-95", "opacity-0");
        modalContent.classList.add("scale-100", "opacity-100");
    }
});

// Update Officer Name on Dashboard after login
document.addEventListener("DOMContentLoaded", () => {
    const officerNameEl = document.getElementById('officerName');
    const officerName = sessionStorage.getItem('officerName'); // fetched from login
    const officerId = sessionStorage.getItem('officerId'); // optional: store ID too

    if (officerNameEl && officerName) {
        officerNameEl.textContent = `${officerName} (ID: ${officerId || ''})`;
    }
});
