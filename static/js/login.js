const baseUrl = window.location.origin;
const apiUrl =  `${baseUrl}/elegion`;

document.getElementById('login-button').addEventListener('click', async () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        alert('Por favor completa ambos campos.');
        return;
    }

    const loginData = {
        user: username,
        passw: password
    };

    console.log('Ready to send to API:', loginData);

    try {
        const response = await fetch(`${apiUrl}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData),
        });

        userId = await response.json();
        console.log(userId)
        window.location.href = `/elegion/account?idCliente=${userId}`;
        
    } catch (error) {
        console.error('Error al realizar el inicio de sesión:', error);
    }

});

document.getElementById('toggle-password').addEventListener('click', function () {
    const passwordInput = document.getElementById('password');
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    this.textContent = type === 'password' ? '👁️' : '🙈';
});