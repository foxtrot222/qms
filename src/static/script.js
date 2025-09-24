let serviceTime = 0;
let serviceInterval;
let currentToken = 38;

// Show interface by role
function showInterface(role, event) {
  document.querySelectorAll('.interface').forEach(i => i.classList.remove('active'));
  document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('active'));

  document.getElementById(role + '-interface').classList.add('active');
  event.target.classList.add('active');
}

// Call next customer
function callNext() {
  currentToken++;
  document.getElementById('current-token').textContent = 'A' + String(currentToken).padStart(3, '0');
  resetServiceTimer();

  // Update active queue visually
  const queue = document.getElementById('active-queue');
  const items = queue.querySelectorAll('.queue-item');
  items[0].remove(); // remove current
  const newToken = currentToken + 4;
  const newItem = document.createElement('div');
  newItem.className = 'queue-item';
  newItem.innerHTML = `<span><strong>A${String(newToken).padStart(3,'0')}</strong> - New Customer (Walk-in)</span><span>Waiting</span>`;
  queue.appendChild(newItem);
}

// Mark customer no-show
function markNoShow() {
  alert('Customer marked as no-show. Moving to next customer.');
  callNext();
}

// Complete service
function completeService() {
  alert('Service completed successfully!');
  resetServiceTimer();
  callNext();
}

// Timer controls
function resetServiceTimer() {
  serviceTime = 0;
  clearInterval(serviceInterval);
  startServiceTimer();
}
function startServiceTimer() {
  serviceInterval = setInterval(() => {
    serviceTime++;
    const minutes = Math.floor(serviceTime / 60);
    const seconds = serviceTime % 60;
    document.getElementById('service-timer').textContent =
      String(minutes).padStart(2,'0') + ':' + String(seconds).padStart(2,'0');
  }, 1000);
}

// Appointment form validation
document.getElementById('appointment-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const service = document.getElementById('service-type').value;
  const time = document.getElementById('appointment-time').value;

  if (!email || !service || !time) {
    alert('Please fill all fields!');
    return;
  }
  alert(`Appointment booked!\nService: ${service}\nTime: ${time}`);
  this.reset();
});

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
  startServiceTimer();
});
