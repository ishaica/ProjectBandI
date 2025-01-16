document.addEventListener('DOMContentLoaded', () =>
{
    let togglePasswordButton = document.getElementById('toggle_password');
    const password_input = document.getElementById('password');
    togglePasswordButton.addEventListener('click', () =>
    {
        password_input.type = password_input.type === 'password' ? 'text' : 'password';
    });
});
