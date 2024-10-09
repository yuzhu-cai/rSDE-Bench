/*
This file contains the JavaScript code for handling dynamic functionality
for the VolunteerMatch web application, including form validation and user interactions.
*/
// Function to validate login form
function validateLoginForm() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');
    if (username === '' || password === '') {
        errorMessage.textContent = 'Username and password cannot be empty.';
        return false;
    }
    errorMessage.textContent = '';
    return true;
}
// Function to validate application form
function validateApplicationForm() {
    const applicantName = document.getElementById('applicant-name').value;
    const applicantEmail = document.getElementById('applicant-email').value;
    const errorMessage = document.getElementById('error-message');
    if (applicantName === '' || applicantEmail === '') {
        errorMessage.textContent = 'Name and email cannot be empty.';
        return false;
    }
    if (!validateEmail(applicantEmail)) {
        errorMessage.textContent = 'Please enter a valid email address.';
        return false;
    }
    errorMessage.textContent = '';
    return true;
}
// Function to validate email format
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}
// Event listeners for forms
document.getElementById('login-form').addEventListener('submit', function(event) {
    if (!validateLoginForm()) {
        event.preventDefault();
    }
});
document.getElementById('apply-form').addEventListener('submit', function(event) {
    if (!validateApplicationForm()) {
        event.preventDefault();
    }
});