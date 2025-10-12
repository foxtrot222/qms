import { api } from '../api.js';

function initCancelToken() {
    const cancelTokenBtn = document.getElementById('cancelTokenBtn');
    if (!cancelTokenBtn) return;

    cancelTokenBtn.addEventListener('click', async () => {
        if (confirm("Are you sure you want to cancel your token? This action cannot be undone.")) {
            try {
                const data = await api.cancelToken();
                if (data.success) {
                    alert("Your token has been cancelled.");
                    window.location.href = '/';
                } else {
                    alert(`Error: ${data.error}`);
                }
            } catch (error) {
                alert('An error occurred while cancelling the token.');
            }
        }
    });
}

function initCheckIn() {
    const checkInBtn = document.getElementById('checkInBtn');
    if (!checkInBtn) return;

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
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            api.checkIn(latitude, longitude)
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

function initMapModal() {
    const viewMapBtn = document.getElementById('viewMapBtn');
    const mapModal = document.getElementById('mapModal');
    const closeMapModalBtn = document.getElementById('closeMapModalBtn');
    const mapModalContent = document.getElementById('map-modal-content');

    if (!viewMapBtn) return;

    const openMap = () => {
        if (mapModal) {
            mapModal.classList.remove('hidden');
            setTimeout(() => {
                mapModal.style.opacity = '1';
                if (mapModalContent) mapModalContent.classList.remove('scale-95', 'opacity-0');
            }, 10);
        }
    };

    const closeMap = () => {
        if (mapModal) {
            if (mapModalContent) mapModalContent.classList.add('scale-95', 'opacity-0');
            mapModal.style.opacity = '0';
            setTimeout(() => mapModal.classList.add('hidden'), 300);
        }
    };

    viewMapBtn.addEventListener('click', openMap);
    if (closeMapModalBtn) closeMapModalBtn.addEventListener('click', closeMap);
    if (mapModal) mapModal.addEventListener('click', (e) => { if (e.target === mapModal) closeMap(); });
}

async function loadStatusDetails() {
    try {
        const data = await api.getStatusDetails();
        if (!data.success || !data.details) {
            console.error('Failed to load status details:', data.error || 'Unknown error');
            return;
        }

        const details = data.details;
        document.getElementById('statusName').textContent = details.name || 'N/A';
        document.getElementById('statusContact').textContent = details.contact || 'N/A';
        document.getElementById('statusService').textContent = details.service || 'N/A';
        document.getElementById('statusPosition').textContent = details.position ?? 'N/A';

        if (details.etr_seconds) {
            let etrSeconds = details.etr_seconds;
            const timerInterval = setInterval(() => {
                if (etrSeconds <= 0) {
                    document.getElementById("etrMessage").textContent = "It's your turn!";
                    clearInterval(timerInterval);
                    return;
                }
                etrSeconds--;
                const hours = Math.floor(etrSeconds / 3600).toString().padStart(2, "0");
                const minutes = Math.floor((etrSeconds % 3600) / 60).toString().padStart(2, "0");
                const seconds = (etrSeconds % 60).toString().padStart(2, "0");
                document.getElementById("etrTimer").textContent = `${hours}:${minutes}:${seconds}`;
            }, 1000);
        } else if (details.type === 'appointment' && details.time_slot) {
            document.getElementById("etrMessage").textContent = `Your appointment is at ${details.time_slot}.`;
            document.getElementById("etrTimer").textContent = details.time_slot;
        } else {
            document.getElementById("etrMessage").textContent = "No ETR available.";
        }
    } catch (error) {
        console.error('Error fetching status details:', error);
    }
}

export function initStatusPage() {
    if (!document.getElementById('statusPage')) return;

    loadStatusDetails();
    initCancelToken();
    initCheckIn();
    initMapModal();
}
