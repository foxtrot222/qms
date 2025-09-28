// === Global Variables & Helpers ===
let isFirstTimeTestUser = true;
let etrTimerInterval;
let verifiedToken = '';

// === Page Navigation ===
const homePage = document.getElementById('homePage');
const organizationPage = document.getElementById('organizationPage');
const orgNavBtn = document.getElementById('orgNavBtn');
const orgNavBtnMobile = document.getElementById('orgNavBtnMobile');

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
        getOtpBtn.classList.add("hidden");
    } else {
        alert(data.error);
    }
});

// Step 2: Verify OTP
document.getElementById("checkStatusSubmitBtn").addEventListener("click", async () => {
    verifiedToken = document.getElementById("token").value.trim();
    const otp = document.getElementById("otp").value.trim();
    if (!otp) return alert("Please enter the OTP.");

    const btn = document.getElementById("checkStatusSubmitBtn");
    btn.textContent = "Verifying...";
    btn.disabled = true;

    try {
        const res = await fetch("/verify_otp", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ token: verifiedToken, otp })
        });

        if (!res.ok) {
            const errorText = await res.text();
            console.error("Error from server:", res.status, res.statusText, errorText);
            alert(`Error from server: ${res.statusText}`);
            btn.textContent = "Go to Status Page";
            btn.disabled = false;
            return;
        }

        const data = await res.json();
        if (data.success) {
            if (data.action === 'choose_type') {
                openChoiceModal();
            } else {
                btn.textContent = "OTP Verified! Redirecting...";
                setTimeout(() => {
                    window.location.href = '/status';
                }, 1000);
            }
        } else {
            alert(data.error);
            btn.textContent = "Go to Status Page";
            btn.disabled = false;
        }
    } catch (error) {
        console.error("Error during OTP verification fetch:", error);
        alert("A network error occurred during OTP verification. Please try again.");
        btn.textContent = "Go to Status Page";
        btn.disabled = false;
    }
});

// === Officer Login Modal Logic ===
const accessDashboardBtn = document.getElementById('accessDashboardBtn');
const officerLoginModal = document.getElementById('officerLoginModal');
const officerLoginModalContent = document.getElementById('officer-login-modal-content');
const closeOfficerLoginModalBtn = document.getElementById('closeOfficerLoginModalBtn');
const officerLoginForm = document.getElementById('officerLoginForm');
const officerLoginError = document.getElementById('officerLoginError');

if (accessDashboardBtn) {
    const openOfficerLoginModal = () => {
        if (!officerLoginModal) return;
        officerLoginModal.classList.remove('hidden');
        setTimeout(() => {
            officerLoginModal.style.opacity = '1';
            if (officerLoginModalContent) {
                officerLoginModalContent.classList.remove('scale-95', 'opacity-0');
            }
        }, 10);
    };

    const closeOfficerLoginModal = () => {
        if (!officerLoginModal) return;
        if (officerLoginModalContent) {
            officerLoginModalContent.classList.add('scale-95', 'opacity-0');
        }
        officerLoginModal.style.opacity = '0';
        setTimeout(() => {
            officerLoginModal.classList.add('hidden');
            if (officerLoginError) {
                officerLoginError.classList.add('hidden');
                officerLoginError.textContent = '';
            }
            if (officerLoginForm) {
                officerLoginForm.reset();
            }
        }, 300);
    };

    accessDashboardBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openOfficerLoginModal();
    });

    if (closeOfficerLoginModalBtn) {
        closeOfficerLoginModalBtn.addEventListener('click', (e) => {
            e.preventDefault();
            closeOfficerLoginModal();
        });
    }

    if (officerLoginModal) {
        officerLoginModal.addEventListener('click', (e) => {
            if (e.target === officerLoginModal) {
                closeOfficerLoginModal();
            }
        });
    }

    if (officerLoginForm) {
        officerLoginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitButton = e.target.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.textContent = 'Logging in...';
            submitButton.disabled = true;
            if (officerLoginError) {
                officerLoginError.classList.add('hidden');
            }

            const formData = new FormData(officerLoginForm);
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.success) {
                    window.location.href = data.redirect;
                } else {
                    if (officerLoginError) {
                        officerLoginError.textContent = data.error || 'An unknown error occurred.';
                        officerLoginError.classList.remove('hidden');
                    }
                    submitButton.textContent = originalButtonText;
                    submitButton.disabled = false;
                }
            } catch (error) {
                console.error('Login error:', error);
                if (officerLoginError) {
                    officerLoginError.textContent = 'An error occurred. Please try again.';
                    officerLoginError.classList.remove('hidden');
                }
                submitButton.textContent = originalButtonText;
                submitButton.disabled = false;
            }
        });
    }
}

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

// === Choice Modal Logic ===
const appointmentModal = document.getElementById('appointmentModal');
const appointmentModalContent = document.getElementById('appointment-modal-content');
const appointmentSlotSelect = document.getElementById('appointmentSlot');
const joinWalkInBtn = document.getElementById('joinWalkInBtn');
const bookAppointmentBtn = document.getElementById('bookAppointmentBtn');

async function openChoiceModal() {
    closeStatusModal();

    try {
        const response = await fetch('/get_available_slots');
        const data = await response.json();
        if (data.success) {
            appointmentSlotSelect.innerHTML = '';
            if (data.slots.length > 0) {
                bookAppointmentBtn.disabled = false;
                data.slots.forEach(slot => {
                    const option = document.createElement('option');
                    option.value = slot.id;
                    option.textContent = slot.time_slot;
                    appointmentSlotSelect.appendChild(option);
                });
            } else {
                const option = document.createElement('option');
                option.textContent = "No slots available";
                option.disabled = true;
                appointmentSlotSelect.appendChild(option);
                bookAppointmentBtn.disabled = true;
            }
        }
    } catch (error) {
        console.error('Error fetching slots:', error);
    }

    appointmentModal.classList.remove('hidden');
    setTimeout(() => {
        appointmentModal.style.opacity = '1';
        if(appointmentModalContent) {
            appointmentModalContent.classList.remove('scale-95', 'opacity-0');
        }
    }, 10);
}

if(joinWalkInBtn) {
    joinWalkInBtn.addEventListener('click', async () => {
        const res = await fetch('/join_walkin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: verifiedToken })
        });
        const data = await res.json();
        if (data.success) {
            window.location.href = '/status';
        } else {
            alert(data.error);
        }
    });
}

if(bookAppointmentBtn) {
    bookAppointmentBtn.addEventListener('click', async () => {
        const slot_id = appointmentSlotSelect.value;
        if (!slot_id || appointmentSlotSelect.options[appointmentSlotSelect.selectedIndex].disabled) {
            alert("Please select an available time slot.");
            return;
        }
        const res = await fetch('/book_appointment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: verifiedToken, slot_id })
        });
        const data = await res.json();
        if (data.success) {
            window.location.href = '/status';
        } else {
            alert(data.error);
        }
    });
}

// === Status Page Logic ===
const cancelTokenBtn = document.getElementById('cancelTokenBtn');
if (cancelTokenBtn) {
    cancelTokenBtn.addEventListener('click', async () => {
        if (confirm("Are you sure you want to cancel your token? This action cannot be undone.")) {
            try {
                const res = await fetch('/cancel_token', { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    alert("Your token has been cancelled.");
                    window.location.href = '/';
                } else {
                    alert(`Error: ${data.error}`);
                }
            } catch (error) {
                console.error('Error cancelling token:', error);
                alert('An error occurred while cancelling the token.');
            }
        }
    });
}

const viewMapBtn = document.getElementById('viewMapBtn');
const mapModal = document.getElementById('mapModal');
const closeMapModalBtn = document.getElementById('closeMapModalBtn');
const mapModalContent = document.getElementById('map-modal-content');

if (viewMapBtn) {
    viewMapBtn.addEventListener('click', () => {
        if (mapModal) {
            mapModal.classList.remove('hidden');
            setTimeout(() => {
                mapModal.style.opacity = '1';
                if (mapModalContent) {
                    mapModalContent.classList.remove('scale-95', 'opacity-0');
                }
            }, 10);
        }
    });
}

function closeMap() {
    if (mapModal) {
        if (mapModalContent) {
            mapModalContent.classList.add('scale-95', 'opacity-0');
        }
        mapModal.style.opacity = '0';
        setTimeout(() => mapModal.classList.add('hidden'), 300);
    }
}

if (closeMapModalBtn) {
    closeMapModalBtn.addEventListener('click', closeMap);
}

if (mapModal) {
    mapModal.addEventListener('click', (e) => {
        if (e.target === mapModal) {
            closeMap();
        }
    });
}