const baseUrl = window.location.origin;
const apiUrl =  `${baseUrl}/elegion`;

document.addEventListener('DOMContentLoaded', () => {
    const transferForm = document.getElementById('transfer-form');
    const successModal = document.getElementById('success-modal')

    transferForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const currency = document.getElementById('currency').value;
        const amount = document.getElementById('amount').value;
        const alias = document.getElementById('alias').value;

        const userId = localStorage.getItem('idCliente');

        try {
            const response = await fetch(`${apiUrl}/doPayment/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "idUsuario": userId,
                    "moneda": currency,
                    "monto": amount,
                    "alias": alias,
                    "formaPago": "Debito"
                })
            });

            if (!response.ok) {
                throw new Error('Error al realizar la transferencia');
            }

            const result = await response.json();
            if(result["result"] == "OK"){
                // Mostrar el modal de éxito
                successModal.style.display = 'flex';

                // Esperar 10 segundos y luego redirigir
                setTimeout(() => {
                    window.location.href = `${apiUrl}/account`;
                }, 5000); // 10 segundos
            }else{
                alert(result["result"])
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un error al realizar la transferencia');
        }
    });
});

document.querySelector('.menu-icon').addEventListener('click', () =>{
    window.location.href = `${apiUrl}/account`;
})

// Handle logout
document.getElementById('logout-button').addEventListener('click', () => {
    fetch('/api/logout', { method: 'POST' })
        .then(() => {
            localStorage.clear()
            window.location.href = `${apiUrl}`;
        })
        .catch(err => console.error('Error logging out:', err));
});