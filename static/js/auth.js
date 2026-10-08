document.querySelectorAll('[data-password-toggle]').forEach((button) => {
    const passwordInput = document.getElementById(button.getAttribute('aria-controls'));
    const icon = button.querySelector('i');

    if (!passwordInput || !icon) {
        return;
    }

    button.addEventListener('click', () => {
        const isVisible = passwordInput.type === 'text';
        passwordInput.type = isVisible ? 'password' : 'text';
        button.setAttribute('aria-pressed', String(!isVisible));
        button.setAttribute('aria-label', isVisible ? 'Show password' : 'Hide password');
        button.title = isVisible ? 'Show password' : 'Hide password';
        icon.classList.toggle('fa-eye', isVisible);
        icon.classList.toggle('fa-eye-slash', !isVisible);
    });
});
