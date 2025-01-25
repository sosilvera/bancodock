import { renderMovimientosTabla } from './tablaMovimientos.js';

const baseUrl = window.location.origin;
const apiUrl =  `${baseUrl}/elegion`;
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

    const jsonString = atob(idCliente);
    const userData = JSON.parse(jsonString);

    // Guardar idCliente en localStorage
    localStorage.setItem('idCliente', userData.userId);
    fetch(`${apiUrl}/getSaldo/${userData.userId}`)
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


// Evento para el botón de movimientos
document.getElementById('movimientos-button').addEventListener('click', async () => {
    try {
        const userId = localStorage.getItem('idCliente')
        // Llamada al servicio de movimientos
        const response = await fetch(`${apiUrl}/getMovimientos/${userId}`); // Reemplaza '1' con el userId si es dinámico
        if (!response.ok) {
            throw new Error('Error al obtener movimientos');
        }

        const data = await response.json(); // Obtenemos la lista de movimientos
        const movimientos = data.listaMovimientos;

        // Renderizar la tabla usando la función importada
        renderMovimientosTabla(movimientos);
    } catch (error) {
        console.error('Error al obtener movimientos:', error);
    }
});