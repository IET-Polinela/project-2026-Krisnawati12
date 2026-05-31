// Menginisialisasi event listener form login secara global saat aplikasi SPA pertama kali dimuat
document.addEventListener('DOMContentLoaded', () => {
    if (typeof setupLoginForm === 'function') {
        setupLoginForm();
    }
});