const logregBox = document.querySelector('.logreg-box');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');

registerLink.addEventListener('click', (e) => {
    e.preventDefault(); // Prevents the page from jumping
    logregBox.classList.add('active');
});

loginLink.addEventListener('click', (e) => {
    e.preventDefault();
    logregBox.classList.remove('active');
});

