// === Global Variables & Helpers ===
let isFirstTimeTestUser = true;
let etrTimerInterval;
let verifiedToken = '';
let verifiedServiceId = null;

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
if (generateTokenBtn) {
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
const statusModal = document.getElementById('statusModal');
if (statusModal) {
    const checkStatusBtn = document.getElementById('checkStatusBtn');
    const statusNavBtn = document.getElementById('statusNavBtn');
    const statusNavBtnMobile = document.getElementById('statusNavBtnMobile');
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

    getOtpBtn.addEventListener("click", async () => {
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

    checkStatusSubmitBtn.addEventListener("click", async () => {
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
                    verifiedServiceId = data.service_id;
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
}

// === Officer Login Modal Logic ===
const accessDashboardBtn = document.getElementById('accessDashboardBtn');
if (accessDashboardBtn) {
    const officerLoginModal = document.getElementById('officerLoginModal');
    const officerLoginModalContent = document.getElementById('officer-login-modal-content');
    const closeOfficerLoginModalBtn = document.getElementById('closeOfficerLoginModalBtn');
    const officerLoginForm = document.getElementById('officerLoginForm');
    const officerLoginError = document.getElementById('officerLoginError');

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

// === Admin Login ===
document.addEventListener("DOMContentLoaded", () => {
    const adminLoginBtn = document.getElementById("adminLoginBtn");
    const adminLoginModal = document.getElementById("adminLoginModal");
    const closeAdminLoginModalBtn = document.getElementById("closeAdminLoginModalBtn");
    const modalContent = document.getElementById("admin-login-modal-content");
    const adminLoginForm = document.getElementById("adminLoginForm");
    const adminLoginError = document.getElementById("adminLoginError");

    // Show modal
    adminLoginBtn.addEventListener("click", (e) => {
        e.preventDefault();
        adminLoginModal.classList.remove("hidden");
        setTimeout(() => {
            modalContent.classList.remove("scale-95", "opacity-0");
            modalContent.classList.add("scale-100", "opacity-100");
        }, 10);
    });

    // Close modal
    const closeModal = () => {
        modalContent.classList.add("scale-95", "opacity-0");
        setTimeout(() => {
            adminLoginModal.classList.add("hidden");
        }, 200);
    };

    closeAdminLoginModalBtn.addEventListener("click", closeModal);

    // Close when clicking outside modal content
    adminLoginModal.addEventListener("click", (e) => {
        if (e.target === adminLoginModal) closeModal();
    });

    // Handle form submit (AJAX)
    adminLoginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(adminLoginForm);
        const adminId = formData.get("adminId");
        const adminPassword = formData.get("adminPassword");

        adminLoginError.textContent = "";
        adminLoginError.classList.add("hidden");

        try {
            const response = await fetch("/adminlogin", {
                method: "POST",
                body: new URLSearchParams({
                    adminID: adminId,
                    adminPassword: adminPassword
                }),
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });

            const data = await response.json();

            if (data.success) {
                // Redirect to admin dashboard
                window.location.href = data.redirect;
            } else {
                // Show error
                adminLoginError.textContent = data.error || "Login failed.";
                adminLoginError.classList.remove("hidden");
            }
        } catch (err) {
            adminLoginError.textContent = "Network error. Please try again.";
            adminLoginError.classList.remove("hidden");
        }
    });
});


// === Dashboard Page Logic ===
const dashboardPage = document.getElementById('dashboardPage');
if (dashboardPage) {
    const customerTimerEl = document.getElementById('customerTimer');
    const nowServingToken = document.getElementById('nowServingToken');
    const queueList = document.getElementById('queueList');
    const completeServiceBtn = document.getElementById('completeServiceBtn');
    const callNextBtn = document.getElementById('callNextBtn');
    const customerCountEl = document.getElementById('customerCount');
    const avgServiceTimeEl = document.getElementById('avgServiceTime');
    let seconds = 0;
    let servingNowTokenId = null;

    function stopCustomerTimer() {
        if (etrTimerInterval) clearInterval(etrTimerInterval);
    }

    function startCustomerTimer() {
        stopCustomerTimer();
        seconds = 0;
        if (customerTimerEl) customerTimerEl.textContent = '00:00';
        etrTimerInterval = setInterval(() => {
            seconds++;
            const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
            const secs = (seconds % 60).toString().padStart(2, '0');
            if (customerTimerEl) customerTimerEl.textContent = `${mins}:${secs}`;
        }, 1000);
    }

    async function loadDashboardStats() {
        try {
            const response = await fetch('/get_dashboard_stats');
            const data = await response.json();
            if (data.success) {
                customerCountEl.textContent = data.stats.customer_count;
                avgServiceTimeEl.textContent = data.stats.avg_time;
            } else {
                console.error('Failed to load stats:', data.error);
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    async function loadQueue() {
        try {
            const response = await fetch('/get_queue');
            const data = await response.json();
            if (data.success) {
                queueList.innerHTML = '';
                const servingNow = data.queue.find(customer => customer.position === 0);
                if (servingNow) {
                    nowServingToken.textContent = servingNow.token_value;
                    servingNowTokenId = servingNow.token_id;
                } else {
                    nowServingToken.textContent = '---';
                    servingNowTokenId = null;
                }
                const inQueue = data.queue.filter(customer => customer.position > 0);
                if (inQueue.length === 0) {
                    queueList.innerHTML = '<p class="text-gray-500">Queue is empty.</p>';
                }
                inQueue.forEach(customer => {
                    const itemHTML = `
                        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between bg-white p-3 rounded-md shadow-sm border gap-3">
                            <div class="flex items-center gap-4">
                                <span class="text-xl font-bold text-gray-600 bg-gray-100 px-3 py-1 rounded-md">${customer.token_value}</span>
                                <div>
                                    <p class="font-semibold text-gray-800">${customer.customer_name}</p>
                                    <p class="text-sm text-gray-500">Contact ID: ${customer.customer_email}</p>
                                </div>
                            </div>
                             <div class="flex items-center gap-2 w-full sm:w-auto">
                                <span class="text-xs font-bold text-gray-600 bg-gray-200 px-2 py-1 rounded-full w-24 text-center">IN LINE</span>
                             </div>
                        </div>
                    `;
                    queueList.insertAdjacentHTML('beforeend', itemHTML);
                });
            } else {
                console.error('Failed to load queue:', data.error);
                queueList.innerHTML = '<p class="text-red-500">Could not load queue.</p>';
            }
        } catch (error) {
            console.error('Error loading queue:', error);
        }
    }

    function refreshDashboard() {
        loadQueue();
        loadDashboardStats();
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
                    stopCustomerTimer();
                    refreshDashboard();
                } else {
                    alert(`Failed to complete service: ${data.error}`);
                }
            } catch (error) {
                console.error('Error completing service:', error);
                alert('An error occurred while completing the service.');
            }
        });
    }

    if (callNextBtn) {
        callNextBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/call_next', {
                    method: 'POST'
                });
                const data = await response.json();
                if (data.success) {
                    refreshDashboard();
                    startCustomerTimer();
                } else {
                    alert(`Failed to call next customer: ${data.error}`);
                }
            } catch (error) {
                console.error('Error calling next customer:', error);
                alert('An error occurred while calling the next customer.');
            }
        });
    }

    const markLateBtn = document.getElementById("markLateBtn");
    if (markLateBtn) {
        markLateBtn.addEventListener("click", async () => {
            if (!servingNowTokenId) {
                alert("No active customer to mark late!");
                return;
            }

            if (!confirm("Mark current customer as late?")) return;

            try {
                const res = await fetch("/mark_late", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ token_id: servingNowTokenId })
                });

                const data = await res.json();

                if (data.success) {
                    alert(`Customer marked late. New position: ${data.new_position}`);
                    refreshDashboard();
                } else {
                    alert(data.error || "Failed to mark late.");
                }
            } catch (err) {
                console.error(err);
                alert("Server error.");
            }
        });
    }

    // Transfer Modal Logic (already implemented)
    const transferBtn = document.getElementById('transferBtn');
    const transferModal = document.getElementById('transferModal');
    const closeTransferModalBtn = document.getElementById('closeTransferModalBtn');
    const transferServiceSelect = document.getElementById('transferService');
    const confirmTransferBtn = document.getElementById('confirmTransferBtn');
    const transferModalContent = document.getElementById('transfer-modal-content');

    function closeTransferModal() {
        transferModalContent.classList.add('scale-95', 'opacity-0');
        transferModal.style.opacity = '0';
        setTimeout(() => transferModal.classList.add('hidden'), 300);
    }

    async function openTransferModal() {
        try {
            const response = await fetch('/get_transfer_services');
            const data = await response.json();
            if (data.success) {
                transferServiceSelect.innerHTML = '';
                if (data.services.length > 0) {
                    data.services.forEach(service => {
                        const option = document.createElement('option');
                        option.value = service.id;
                        option.textContent = service.name;
                        transferServiceSelect.appendChild(option);
                    });
                    transferModal.classList.remove('hidden');
                    setTimeout(() => {
                        transferModal.style.opacity = '1';
                        transferModalContent.classList.remove('scale-95', 'opacity-0');
                    }, 10);
                } else {
                    alert("No other services available to transfer to.");
                }
            } else {
                alert(`Error fetching services: ${data.error}`);
            }
        } catch (error) {
            console.error('Error opening transfer modal:', error);
            alert('Could not open transfer modal.');
        }
    }

    if (transferBtn) {
        transferBtn.addEventListener('click', openTransferModal);
    }
    if (closeTransferModalBtn) {
        closeTransferModalBtn.addEventListener('click', closeTransferModal);
    }
    if (transferModal) {
        transferModal.addEventListener('click', (e) => { if (e.target === transferModal) closeTransferModal(); });
    }
    if (confirmTransferBtn) {
        confirmTransferBtn.addEventListener('click', async () => {
            const destination_service_id = transferServiceSelect.value;
            if (!destination_service_id) {
                alert("Please select a service to transfer to.");
                return;
            }

            try {
                const response = await fetch('/transfer_customer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ destination_service_id })
                });
                const data = await response.json();
                if (data.success) {
                    alert('Customer transferred successfully!');
                    closeTransferModal();
                    refreshDashboard();
                } else {
                    alert(`Transfer failed: ${data.error}`);
                }
            } catch (error) {
                console.error('Error transferring customer:', error);
                alert('An error occurred during the transfer.');
            }
        });
    }

    // Initial Load
    refreshDashboard();
    startCustomerTimer();
}


// === Choice Modal Logic ===
async function openChoiceModal() {
    const appointmentModal = document.getElementById('appointmentModal');
    const appointmentModalContent = document.getElementById('appointment-modal-content');
    const appointmentSlotSelect = document.getElementById('appointmentSlot');
    const bookAppointmentBtn = document.getElementById('bookAppointmentBtn');

    closeStatusModal();
    updateEstimatedWaitTime(verifiedServiceId);
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

const appointmentModal = document.getElementById('appointmentModal');
if (appointmentModal) {
    const joinWalkInBtn = document.getElementById('joinWalkInBtn');
    const bookAppointmentBtn = document.getElementById('bookAppointmentBtn');
    const appointmentSlotSelect = document.getElementById('appointmentSlot');

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

// === Estimated Waiting Time of new customer in walk-in line ===
async function updateEstimatedWaitTime(service_id) {
    try {
        const response = await fetch(`/estimated_wait_time?service_id=${service_id}`);
        const data = await response.json();

        if (data.success) {
            const waitElem = document.getElementById('estimatedWaitTime');
            const timeStr = data.estimated_wait_time || "00:00:00";

            // Convert "HH:MM:SS" -> total minutes
            const [hours, minutes, seconds] = timeStr.split(':').map(Number);
            const totalMinutes = hours * 60 + minutes + Math.round(seconds / 60);

            if (waitElem) {
                if (totalMinutes > 0) {
                    waitElem.textContent = `~${totalMinutes} Mins`;
                } else {
                    waitElem.textContent = 'No Wait';
                }
            }
        } else {
            console.error("Error fetching wait time:", data.error);
        }
    } catch (error) {
        console.error("Error fetching wait time:", error);
    }
}



// === Status Page Logic ===
const statusPage = document.getElementById('statusPage');
if (statusPage) {
    async function loadStatusDetails() {
        try {
            const response = await fetch('/get_status_details');
            const data = await response.json();

            if (data.success && data.details) {
                const details = data.details;

                // Populate customer details
                document.getElementById('statusName').textContent = details.name || 'N/A';
                document.getElementById('statusContact').textContent = details.contact || 'N/A';
                document.getElementById('statusService').textContent = details.service || 'N/A';
                document.getElementById('statusPosition').textContent = details.position ?? 'N/A';

                // Handle ETR countdown
                if (details.etr_seconds) {
                    let etrSeconds = details.etr_seconds;

                    function updateETR() {
                        let hours = Math.floor(etrSeconds / 3600);
                        let minutes = Math.floor((etrSeconds % 3600) / 60);
                        let seconds = etrSeconds % 60;

                        document.getElementById("etrTimer").textContent =
                            `${hours.toString().padStart(2, "0")}:` +
                            `${minutes.toString().padStart(2, "0")}:` +
                            `${seconds.toString().padStart(2, "0")}`;

                        if (etrSeconds <= 0) {
                            document.getElementById("etrMessage").textContent = "It's your turn!";
                            clearInterval(timerInterval);
                        }

                        etrSeconds--;
                    }

                    updateETR(); // run once immediately
                    let timerInterval = setInterval(updateETR, 1000);
                } else {
                    document.getElementById("etrMessage").textContent = "No ETR available.";
                }

                // Optional: show extra info if you want
                if (details.type !== 'appointment' && details.ETR) {
                    console.log(`Estimated Time Remaining: ${details.ETR}`);
                } else if (details.type === 'appointment' && details.time_slot) {
                    console.log(`Appointment Time: ${details.time_slot}`);
                    document.getElementById("etrMessage").textContent = `Your appointment is at ${details.time_slot}.`;
                    document.getElementById("etrTimer").textContent = details.time_slot;
                }

            } else {
                console.error('Failed to load status details:', data.error || 'Unknown error');
            }
        } catch (error) {
            console.error('Error fetching status details:', error);
        }
    }

    // Run when page is ready
    document.addEventListener('DOMContentLoaded', loadStatusDetails);

    // === Cancel Token ===
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

    // === Check-in Logic ===
    const checkInBtn = document.getElementById('checkInBtn');
    if (checkInBtn) {
        checkInBtn.addEventListener('click', () => {
            checkInBtn.disabled = true;
            checkInBtn.textContent = 'Checking in...';

            if (!navigator.geolocation) {
                alert('Geolocation is not supported by your browser.');
                checkInBtn.disabled = false;
                checkInBtn.textContent = 'Check-in Now';
                return;
            }

            function success(position) {
                const latitude  = position.coords.latitude;
                const longitude = position.coords.longitude;

                fetch('/check_in', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ latitude, longitude })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        checkInBtn.textContent = 'Checked-in Successfully!';
                        checkInBtn.classList.replace('bg-green-500', 'bg-green-600');
                        checkInBtn.classList.remove('hover:bg-green-600');
                    } else {
                        alert(`Check-in failed: ${data.error}`);
                        checkInBtn.disabled = false;
                        checkInBtn.textContent = 'Check-in Now';
                    }
                })
                .catch(err => {
                    console.error('Check-in error:', err);
                    alert('An error occurred during check-in.');
                    checkInBtn.disabled = false;
                    checkInBtn.textContent = 'Check-in Now';
                });
            }

            function error() {
                alert('Unable to retrieve your location.');
                checkInBtn.disabled = false;
                checkInBtn.textContent = 'Check-in Now';
            }

            navigator.geolocation.getCurrentPosition(success, error);
        });
    }

    // === Map Modal ===
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
}

// === Logout ===
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
const latenessFactor = document.getElementById('lateness-factor');
const latenessValue = document.getElementById('lateness-value');
latenessFactor.addEventListener('input', () => {
  latenessValue.textContent = latenessFactor.value;
});

const addUserBtn = document.getElementById('addUserBtn');
const addUserModal = document.getElementById('addUserModal');
const closeAddUserModalBtn = document.getElementById('closeAddUserModalBtn');
const addUserModalContent = document.getElementById('add-user-modal-content');

if (addUserBtn) {
    addUserBtn.addEventListener('click', () => {
        addUserModal.classList.remove('hidden');
        setTimeout(() => {
            addUserModal.style.opacity = '1';
            addUserModalContent.classList.remove('scale-95', 'opacity-0');
        }, 10);
    });
}

if (closeAddUserModalBtn) {
    closeAddUserModalBtn.addEventListener('click', () => {
        addUserModalContent.classList.add('scale-95', 'opacity-0');
        addUserModal.style.opacity = '0';
        setTimeout(() => addUserModal.classList.add('hidden'), 300);
    });
}

if (addUserModal) {
    addUserModal.addEventListener('click', (e) => {
        if (e.target === addUserModal) {
            addUserModalContent.classList.add('scale-95', 'opacity-0');
            addUserModal.style.opacity = '0';
            setTimeout(() => addUserModal.classList.add('hidden'), 300);
        }
    });
}

const addServiceBtn = document.getElementById('addServiceBtn');
const addServiceModal = document.getElementById('addServiceModal');
const closeAddServiceModalBtn = document.getElementById('closeAddServiceModalBtn');
const addServiceModalContent = document.getElementById('add-service-modal-content');

if (addServiceBtn) {
    addServiceBtn.addEventListener('click', () => {
        addServiceModal.classList.remove('hidden');
        setTimeout(() => {
            addServiceModal.style.opacity = '1';
            addServiceModalContent.classList.remove('scale-95', 'opacity-0');
        }, 10);
    });
}

if (closeAddServiceModalBtn) {
    closeAddServiceModalBtn.addEventListener('click', () => {
        addServiceModalContent.classList.add('scale-95', 'opacity-0');
        addServiceModal.style.opacity = '0';
        setTimeout(() => addServiceModal.classList.add('hidden'), 300);
    });
}

if (addServiceModal) {
    addServiceModal.addEventListener('click', (e) => {
        if (e.target === addServiceModal) {
            addServiceModalContent.classList.add('scale-95', 'opacity-0');
            addServiceModal.style.opacity = '0';
            setTimeout(() => addServiceModal.classList.add('hidden'), 300);
        }
    });
}

// Edit User Modal Logic
const editUserModal = document.getElementById('editUserModal');
const closeEditUserModalBtn = document.getElementById('closeEditUserModalBtn');
const editUserModalContent = document.getElementById('edit-user-modal-content');
const editUserForm = document.getElementById('editUserForm');

function openEditUserModal() {
    editUserModal.classList.remove('hidden');
    setTimeout(() => {
        editUserModal.style.opacity = '1';
        editUserModalContent.classList.remove('scale-95', 'opacity-0');
    }, 10);
}

function closeEditUserModal() {
    editUserModalContent.classList.add('scale-95', 'opacity-0');
    editUserModal.style.opacity = '0';
    setTimeout(() => editUserModal.classList.add('hidden'), 300);
}

if (closeEditUserModalBtn) {
    closeEditUserModalBtn.addEventListener('click', closeEditUserModal);
}
if (editUserModal) {
    editUserModal.addEventListener('click', (e) => {
        if (e.target === editUserModal) {
            closeEditUserModal();
        }
    });
}

// Event delegation for Edit User buttons
const editUserButtons = document.querySelectorAll('.edit-user-btn');
console.log('Found Edit User buttons:', editUserButtons.length);
editUserButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
        e.preventDefault();
        console.log('Edit User button clicked.');
        const userId = e.target.dataset.userId; // Extract user_id from data-user-id
        console.log('User ID:', userId);
        try {
            console.log(`Fetching user data for ID: ${userId}`);
            const response = await fetch(`/admin/users/${userId}/get`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.success) {
                console.log('User data fetched successfully:', data.user);
                document.getElementById('editUserId').value = data.user.id;
                document.getElementById('editUserName').value = data.user.name;
                document.getElementById('editOfficerID').value = data.user.officerID;
                document.getElementById('editUserServiceId').value = data.user.service_id;
                openEditUserModal();
                console.log('Edit User modal opened.');
            } else {
                alert(`Error: ${data.error}`);
                console.error('Error from server:', data.error);
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
            alert('An error occurred while fetching user data.');
        }
    });
});

// Edit Service Modal Logic
const editServiceModal = document.getElementById('editServiceModal');
const closeEditServiceModalBtn = document.getElementById('closeEditServiceModalBtn');
const editServiceModalContent = document.getElementById('edit-service-modal-content');
const editServiceForm = document.getElementById('editServiceForm');

function openEditServiceModal() {
    editServiceModal.classList.remove('hidden');
    setTimeout(() => {
        editServiceModal.style.opacity = '1';
        editServiceModalContent.classList.remove('scale-95', 'opacity-0');
    }, 10);
    console.log('Edit Service modal opened.');
}

function closeEditServiceModal() {
    editServiceModalContent.classList.add('scale-95', 'opacity-0');
    editServiceModal.style.opacity = '0';
    setTimeout(() => editServiceModal.classList.add('hidden'), 300);
    console.log('Edit Service modal closed.');
}

if (closeEditServiceModalBtn) {
    closeEditServiceModalBtn.addEventListener('click', closeEditServiceModal);
}
if (editServiceModal) {
    editServiceModal.addEventListener('click', (e) => {
        if (e.target === editServiceModal) {
            closeEditServiceModal();
        }
    });
}

// Event delegation for Edit Service buttons
const editServiceButtons = document.querySelectorAll('.edit-service-btn');
console.log('Found Edit Service buttons:', editServiceButtons.length);
editServiceButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
        e.preventDefault();
        console.log('Edit Service button clicked.');
        const serviceId = e.target.dataset.serviceId; // Extract service_id from data-service-id
        console.log('Service ID:', serviceId);
        try {
            console.log(`Fetching service data for ID: ${serviceId}`);
            const response = await fetch(`/admin/services/${serviceId}/get`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.success) {
                console.log('Service data fetched successfully:', data.service);
                document.getElementById('editServiceId').value = data.service.id;
                document.getElementById('editServiceName').value = data.service.name;
                openEditServiceModal();
                console.log('Edit Service modal opened.');
            } else {
                alert(`Error: ${data.error}`);
                console.error('Error from server:', data.error);
            }
        } catch (error) {
            console.error('Error fetching service data:', error);
            alert('An error occurred while fetching service data.');
        }
    });
});