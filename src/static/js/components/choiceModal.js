import { api } from '../api.js';

let verifiedToken = ''; // This will be set by statusModal
let verifiedServiceId = null; // This will be set by statusModal

async function updateEstimatedWaitTime(service_id) {
    try {
        const data = await api.getEstimatedWaitTime(service_id);
        const waitElem = document.getElementById('estimatedWaitTime');
        if (!waitElem) return;

        if (data.success) {
            const timeStr = data.estimated_wait_time || "00:00:00";
            const [hours, minutes, seconds] = timeStr.split(':').map(Number);
            const totalMinutes = hours * 60 + minutes + Math.round(seconds / 60);

            if (totalMinutes > 0) {
                waitElem.textContent = `~${totalMinutes} Mins`;
            } else {
                waitElem.textContent = 'No Wait';
            }
        } else {
            console.error("Error fetching wait time:", data.error);
            waitElem.textContent = 'N/A';
        }
    } catch (error) {
        console.error("Error fetching wait time:", error);
    }
}

export async function openChoiceModal(token, serviceId) {
    verifiedToken = token;
    verifiedServiceId = serviceId;

    const appointmentModal = document.getElementById('appointmentModal');
    const appointmentModalContent = document.getElementById('appointment-modal-content');
    const appointmentSlotSelect = document.getElementById('appointmentSlot');
    const bookAppointmentBtn = document.getElementById('bookAppointmentBtn');

    if (!appointmentModal) return;

    updateEstimatedWaitTime(verifiedServiceId);

    try {
        const data = await api.getAvailableSlots();
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
        if (appointmentModalContent) {
            appointmentModalContent.classList.remove('scale-95', 'opacity-0');
        }
    }, 10);
}

export function initChoiceModal() {
    const appointmentModal = document.getElementById('appointmentModal');
    if (!appointmentModal) return;

    const joinWalkInBtn = document.getElementById('joinWalkInBtn');
    const bookAppointmentBtn = document.getElementById('bookAppointmentBtn');
    const appointmentSlotSelect = document.getElementById('appointmentSlot');

    joinWalkInBtn.addEventListener('click', async () => {
        try {
            const data = await api.joinWalkIn(verifiedToken);
            if (data.success) {
                window.location.href = '/status';
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert('An error occurred while joining the queue.');
        }
    });

    bookAppointmentBtn.addEventListener('click', async () => {
        const slot_id = appointmentSlotSelect.value;
        if (!slot_id || appointmentSlotSelect.options[appointmentSlotSelect.selectedIndex].disabled) {
            alert("Please select an available time slot.");
            return;
        }
        try {
            const data = await api.bookAppointment(verifiedToken, slot_id);
            if (data.success) {
                window.location.href = '/status';
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert('An error occurred while booking the appointment.');
        }
    });
}
