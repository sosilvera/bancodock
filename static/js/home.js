const apiUrl = `http://localhost:3100/elegion`;
// Parse URL query parameters
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Load account balances
document.addEventListener('DOMContentLoaded', () => {
    const idCliente = getQueryParam('idCliente');
    if (!idCliente) {
        alert('No se encontró un ID de cliente. Redirigiendo a la página de login.');
        window.location.href = '/elegion/login';
        return;
    }

    // Guardar idCliente en localStorage
    localStorage.setItem('idCliente', idCliente);
    console.log(idCliente)
    fetch(`${apiUrl}/getSaldo/${idCliente}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('saldo-pesos').textContent = `$ ${data.saldoPesos}`;
            document.getElementById('saldo-dolar').textContent = `USD ${data.saldoDolar}`;
        })
        .catch(err => console.error('Error fetching balances:', err));
});

// Navigate to different routes
function navigateTo(route) {
    window.location.href = route;
}

// Handle logout
document.getElementById('logout-button').addEventListener('click', () => {
    fetch('/api/logout', { method: 'POST' })
        .then(() => {
            window.location.href = `${apiUrl}`;
        })
        .catch(err => console.error('Error logging out:', err));
});

