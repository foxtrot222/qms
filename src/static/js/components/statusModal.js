import { api } from '../api.js';
import { openChoiceModal } from './choiceModal.js';

let statusModal, statusModalContent, closeStatusModalBtn;

function openStatusModal() {
    statusModal.classList.remove('hidden');
    setTimeout(() => {
        statusModal.style.opacity = '1';
        statusModalContent.classList.remove('scale-95', 'opacity-0');
        statusModalContent.classList.add('scale-100', 'opacity-100');
    }, 10);
}

function closeStatusModal() {
    const statusForm = document.getElementById('statusForm');
    const otpInputContainer = document.getElementById('otpInputContainer');
    const checkStatusSubmitBtn = document.getElementById('checkStatusSubmitBtn');
    const getOtpBtn = document.getElementById('getOtpBtn');

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

export function initStatusModal() {
    statusModal = document.getElementById('statusModal');
    if (!statusModal) return;

    const checkStatusBtn = document.getElementById('checkStatusBtn');
    const statusNavBtn = document.getElementById('statusNavBtn');
    const statusNavBtnMobile = document.getElementById('statusNavBtnMobile');
    statusModalContent = document.getElementById('status-modal-content');
    closeStatusModalBtn = document.getElementById('closeStatusModalBtn');
    const statusForm = document.getElementById('statusForm');
    const getOtpBtn = document.getElementById('getOtpBtn');
    const checkStatusSubmitBtn = document.getElementById('checkStatusSubmitBtn');

    [checkStatusBtn, statusNavBtn, statusNavBtnMobile].forEach(btn => {
        if (btn) btn.addEventListener('click', (e) => { e.preventDefault(); openStatusModal(); });
    });
    closeStatusModalBtn.addEventListener('click', closeStatusModal);
    statusModal.addEventListener('click', e => { if (e.target === statusModal) closeStatusModal(); });

    getOtpBtn.addEventListener("click", async () => {
        const token = document.getElementById("token").value.trim();
        if (!token) return alert("Please enter your token.");

        try {
            const data = await api.requestOtp(token);
            if (data.success) {
                alert(data.message);
                document.getElementById("otpInputContainer").classList.remove("hidden");
                document.getElementById("checkStatusSubmitBtn").classList.remove("hidden");
                getOtpBtn.classList.add("hidden");
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert('An error occurred while requesting OTP.');
        }
    });

    checkStatusSubmitBtn.addEventListener("click", async () => {
        const verifiedToken = document.getElementById("token").value.trim();
        const otp = document.getElementById("otp").value.trim();
        if (!otp) return alert("Please enter the OTP.");

        const btn = document.getElementById("checkStatusSubmitBtn");
        btn.textContent = "Verifying...";
        btn.disabled = true;

        try {
            const data = await api.verifyOtp(verifiedToken, otp);
            if (data.success) {
                if (data.action === 'choose_type') {
                    closeStatusModal();
                    openChoiceModal(verifiedToken, data.service_id);
                } else {
                    btn.textContent = "OTP Verified! Redirecting...";
                    setTimeout(() => {
                        window.location.href = '/status';
                    }, 1000);
                }
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert("A network error occurred during OTP verification. Please try again.");
        } finally {
            btn.textContent = "Go to Status Page";
            btn.disabled = false;
        }
    });
}
