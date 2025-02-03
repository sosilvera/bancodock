import { renderMovimientosTabla } from './tablaMovimientos.js';
import { renderTarjetasTabla } from './tablaTarjetas.js';

const baseUrl = window.location.origin;
const apiUrl =  `${baseUrl}/elegion`;

// Load account balances
document.addEventListener('DOMContentLoaded', () => {
    const userId = localStorage.getItem('idCliente');
    console.log(userId)
    if (!userId) {
        alert('No se encontró un ID de cliente. Redirigiendo a la página de login.');
        window.location.href = '/elegion/login';
        return;
    }

    fetch(`${apiUrl}/getSaldo/${userId}`)
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
            localStorage.clear()
            window.location.href = `${apiUrl}`;
        })
        .catch(err => console.error('Error logging out:', err));
});


// Evento para el botón de movimientos
document.getElementById('movimientos-button').addEventListener('click', async () => {
    try {
        const userId = localStorage.getItem('idCliente')
        // Llamada al servicio de movimientos
        const response = await fetch(`${apiUrl}/getMovimientos/${userId}`);
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


// Evento para el botón de tarjetas
document.getElementById('tarjetas-button').addEventListener('click', async () => {
    try {
        const userId = localStorage.getItem('idCliente')
        // Llamada al servicio de movimientos
        const response = await fetch(`${apiUrl}/getTarjetas/${userId}`);
        if (!response.ok) {
            throw new Error('Error al obtener tarjetas');
        }

        const data = await response.json(); // Obtenemos la lista de tarjetas

        // Renderizar la tabla usando la función importada
        renderTarjetasTabla(data);
    } catch (error) {
        console.error('Error al obtener tarjetas:', error);
    }
});

document.getElementById('trans-button').addEventListener('click', async() => {
    try{
        window.location.href = `/elegion/transfer`;
    } catch (error) {
        console.error('Error: ', error);
    }
})