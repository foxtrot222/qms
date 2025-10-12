// Centralized API calls

async function fetchJSON(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Fetch error for ${url}:`, error);
        throw error;
    }
}

export const api = {
    getServices: () => fetchJSON('/get_services'),
    generateToken: (formData) => fetchJSON('/generate_token', { method: 'POST', body: formData }),
    requestOtp: (token) => fetchJSON('/request_otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
    }),
    verifyOtp: (token, otp) => fetchJSON('/verify_otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, otp })
    }),
    getAvailableSlots: () => fetchJSON('/get_available_slots'),
    joinWalkIn: (token) => fetchJSON('/join_walkin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
    }),
    bookAppointment: (token, slot_id) => fetchJSON('/book_appointment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, slot_id })
    }),
    getEstimatedWaitTime: (serviceId) => fetchJSON(`/estimated_wait_time?service_id=${serviceId}`),
    getStatusDetails: () => fetchJSON('/get_status_details'),
    cancelToken: () => fetchJSON('/cancel_token', { method: 'POST' }),
    checkIn: (latitude, longitude) => fetchJSON('/check_in', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude, longitude })
    }),
    officerLogin: (formData) => fetchJSON('/login', { method: 'POST', body: formData }),
    adminLogin: (formData) => fetchJSON('/adminlogin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(formData)
    }),
    getDashboardStats: () => fetchJSON('/get_dashboard_stats'),
    getQueue: () => fetchJSON('/get_queue'),
    completeService: (service_time) => fetchJSON('/complete_service', {
        method: 'POST',
        body: new URLSearchParams({ service_time })
    }),
    callNext: () => fetchJSON('/call_next', { method: 'POST' }),
    markLate: (token_id) => fetchJSON('/mark_late', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token_id })
    }),
    getTransferServices: () => fetchJSON('/get_transfer_services'),
    transferCustomer: (destination_service_id) => fetchJSON('/transfer_customer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ destination_service_id })
    }),
    getUserData: (userId) => fetchJSON(`/admin/users/${userId}/get`),
    getServiceData: (serviceId) => fetchJSON(`/admin/services/${serviceId}/get`),
};
