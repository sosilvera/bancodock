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

    try {
        const response = await fetch(`${apiUrl}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData),
        });

        data = await response.json();
        console.log(data)
        // Generar un hash del JSON (Base64)
        const jsonString = JSON.stringify(data);
        const hash = btoa(jsonString); // Codifica en Base64
        console.log(hash)
        // Redirigir a /account con el hash
        window.location.href = `/elegion/account?idCliente=${hash}`;
        
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