import { api } from '../api.js';

let etrTimerInterval;
let seconds = 0;
let servingNowTokenId = null;

const customerTimerEl = document.getElementById('customerTimer');
const nowServingToken = document.getElementById('nowServingToken');
const queueList = document.getElementById('queueList');
const completeServiceBtn = document.getElementById('completeServiceBtn');
const callNextBtn = document.getElementById('callNextBtn');
const customerCountEl = document.getElementById('customerCount');
const avgServiceTimeEl = document.getElementById('avgServiceTime');
const markLateBtn = document.getElementById("markLateBtn");

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
        const data = await api.getDashboardStats();
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
        const data = await api.getQueue();
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
            queueList.innerHTML = `<p class="text-red-500">Could not load queue: ${data.error}</p>`;
        }
    } catch (error) {
        console.error('Error loading queue:', error);
    }
}

function refreshDashboard() {
    loadQueue();
    loadDashboardStats();
}

function initTransferModal() {
    const transferBtn = document.getElementById('transferBtn');
    const transferModal = document.getElementById('transferModal');
    const closeTransferModalBtn = document.getElementById('closeTransferModalBtn');
    const transferServiceSelect = document.getElementById('transferService');
    const confirmTransferBtn = document.getElementById('confirmTransferBtn');
    const transferModalContent = document.getElementById('transfer-modal-content');

    if (!transferBtn) return;

    function closeTransferModal() {
        transferModalContent.classList.add('scale-95', 'opacity-0');
        transferModal.style.opacity = '0';
        setTimeout(() => transferModal.classList.add('hidden'), 300);
    }

    async function openTransferModal() {
        try {
            const data = await api.getTransferServices();
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
            alert('Could not open transfer modal.');
        }
    }

    transferBtn.addEventListener('click', openTransferModal);
    closeTransferModalBtn.addEventListener('click', closeTransferModal);
    transferModal.addEventListener('click', (e) => { if (e.target === transferModal) closeTransferModal(); });

    confirmTransferBtn.addEventListener('click', async () => {
        const destination_service_id = transferServiceSelect.value;
        if (!destination_service_id) return alert("Please select a service to transfer to.");

        try {
            const data = await api.transferCustomer(destination_service_id);
            if (data.success) {
                alert('Customer transferred successfully!');
                closeTransferModal();
                refreshDashboard();
            } else {
                alert(`Transfer failed: ${data.error}`);
            }
        } catch (error) {
            alert('An error occurred during the transfer.');
        }
    });
}

export function initDashboardPage() {
    if (!document.getElementById('dashboardPage')) return;

    completeServiceBtn.addEventListener('click', async () => {
        try {
            const data = await api.completeService(seconds);
            if (data.success) {
                stopCustomerTimer();
                refreshDashboard();
            } else {
                alert(`Failed to complete service: ${data.error}`);
            }
        } catch (error) {
            alert('An error occurred while completing the service.');
        }
    });

    callNextBtn.addEventListener('click', async () => {
        try {
            const data = await api.callNext();
            if (data.success) {
                refreshDashboard();
                startCustomerTimer();
            } else {
                alert(`Failed to call next customer: ${data.error}`);
            }
        } catch (error) {
            alert('An error occurred while calling the next customer.');
        }
    });

    markLateBtn.addEventListener("click", async () => {
        if (!servingNowTokenId) return alert("No active customer to mark late!");
        if (!confirm("Mark current customer as late?")) return;

        try {
            const data = await api.markLate(servingNowTokenId);
            if (data.success) {
                alert(`Customer marked late. New position: ${data.new_position}`);
                refreshDashboard();
            } else {
                alert(data.error || "Failed to mark late.");
            }
        } catch (err) {
            alert("Server error.");
        }
    });

    initTransferModal();
    refreshDashboard();
    startCustomerTimer();
}
