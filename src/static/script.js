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
const serviceSelect = document.getElementById('service');

async function loadServices() {
    try {
        const response = await fetch('/get_services');
        const data = await response.json();
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

if (generateTokenBtn) {
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
    generateTokenBtn.addEventListener('click', (e) => { e.preventDefault(); openTokenModal(); });
    closeModalBtn.addEventListener('click', closeTokenModal);
    tokenModal.addEventListener('click', (e) => { if (e.target === tokenModal) closeTokenModal(); });

    tokenForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitButton = e.target.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.textContent = 'Generating...';
        submitButton.disabled = true;

        const formData = new FormData(tokenForm);
        try {
            const response = await fetch('/generate_token', { method: 'POST', body: formData });
            const data = await response.json();
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
            console.error('Error generating token:', error);
            alert('An error occurred while generating the token.');
            submitButton.textContent = originalButtonText;
            submitButton.disabled = false;
        }
    });
}

// === Status Check Modal Logic (Token → OTP → Verify) ===
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

function openStatusModal() {
    statusModal.classList.remove('hidden');
    setTimeout(() => {
        statusModal.style.opacity = '1';
        statusModalContent.classList.remove('scale-95', 'opacity-0');
        statusModalContent.classList.add('scale-100', 'opacity-100');
    }, 10);
}

function closeStatusModal() {
    statusModalContent.classList.add('scale-95', 'opacity-0');
    statusModalContent.classList.remove('scale-100', 'opacity-100');
    statusModal.style.opacity = '0';
    setTimeout(() => {
        statusModal.classList.add('hidden');
        otpInputContainer.classList.add('hidden');
        checkStatusSubmitBtn.classList.add('hidden');
        getOtpBtn.classList.remove('hidden');
        statusForm.reset();
    }, 300);
}

[checkStatusBtn, statusNavBtn, statusNavBtnMobile].forEach(btn => { if (btn) btn.addEventListener('click', (e) => { e.preventDefault(); openStatusModal(); }); });
closeStatusModalBtn.addEventListener('click', closeStatusModal);
statusModal.addEventListener('click', e => { if (e.target === statusModal) closeStatusModal(); });

// Step 1: Request OTP
document.getElementById("getOtpBtn").addEventListener("click", async () => {
    const token = document.getElementById("token").value.trim();
    if (!token) return alert("Please enter your token.");

    const res = await fetch("/request_otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token })
    });

const data = await res.json();
    if (data.success) {
        alert(data.message);
        document.getElementById("otpInputContainer").classList.remove("hidden");
        document.getElementById("checkStatusSubmitBtn").classList.remove("hidden");
        getOtpBtn.disabled = true; // prevent immediate resending
    } else {
        alert(data.error);
    }
});

// Step 2: Verify OTP
document.getElementById("checkStatusSubmitBtn").addEventListener("click", async () => {
    const token = document.getElementById("token").value.trim();
    const otp = document.getElementById("otp").value.trim();
    if (!otp) return alert("Please enter the OTP.");

    const btn = document.getElementById("checkStatusSubmitBtn");
    btn.textContent = "Verifying...";
    btn.disabled = true;

    const res = await fetch("/verify_otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, otp })
    });

    const data = await res.json();
    if (data.success) {
        btn.textContent = "OTP Verified! Redirecting...";
        // ✅ Pass token as query param
        setTimeout(() => {
            window.location.href = `/status?token=${token}`;
        }, 1000);
    } else {
        alert(data.error);
        btn.textContent = "Go to Status Page";
        btn.disabled = false;
    }
});


const completeServiceBtn = document.getElementById('completeServiceBtn');

let seconds = 0;

function startCustomerTimer() {
    if (etrTimerInterval) clearInterval(etrTimerInterval);
    seconds = 0;
    if (customerTimerEl) customerTimerEl.textContent = '00:00';
    etrTimerInterval = setInterval(() => {
        seconds++;
        const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
        const secs = (seconds % 60).toString().padStart(2, '0');
        if (customerTimerEl) customerTimerEl.textContent = `${mins}:${secs}`;
    }, 1000);
}

if (completeServiceBtn) {
    completeServiceBtn.addEventListener('click', async () => {
        try {
            const formData = new FormData();
            formData.append('service_time', seconds);

            const response = await fetch('/complete_service', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.success) {
                loadQueue(); // Refresh the queue
                startCustomerTimer(); // Restart the timer
            } else {
                console.error('Failed to complete service:', data.error);
                alert('Failed to complete service.');
            }
        } catch (error) {
            console.error('Error completing service:', error);
            alert('An error occurred while completing the service.');
        }
    });
}

const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        window.location.href = '/logout';
    });
}

// === Officer Dashboard Logic ===
const customerTimerEl = document.getElementById('customerTimer');
const callNextBtn = document.getElementById('callNextBtn');
const customerCountEl = document.getElementById('customerCount');
const nowServingToken = document.getElementById('nowServingToken');
const queueList = document.getElementById('queueList');

async function loadQueue() {
    try {
        const response = await fetch('/get_queue');
        const data = await response.json();

        if (data.success) {
            queueList.innerHTML = ''; // Clear existing list

            const servingNow = data.queue.find(customer => customer.position === 0);
            if (servingNow) {
                nowServingToken.textContent = servingNow.token_value;
            } else {
                nowServingToken.textContent = '---';
            }

            const inQueue = data.queue.filter(customer => customer.position > 0);
            inQueue.forEach(customer => {
                const li = document.createElement('li');
                li.className = 'flex justify-between items-center bg-white p-2 rounded-md shadow-sm border border-gray-200';

                const tokenSpan = document.createElement('span');
                tokenSpan.className = 'font-medium text-gray-700';
                tokenSpan.textContent = customer.token_value;

                const statusSpan = document.createElement('span');
                statusSpan.className = 'text-xs font-bold text-gray-600 bg-gray-200 px-2 py-1 rounded-full';
                statusSpan.textContent = 'IN LINE';

                li.appendChild(tokenSpan);
                li.appendChild(statusSpan);
                queueList.appendChild(li);
            });

            if(customerCountEl) customerCountEl.textContent = inQueue.length;

        } else {
            console.error('Failed to load queue:', data.error);
        }
    } catch (error) {
        console.error('Error loading queue:', error);
    }
}

