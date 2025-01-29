document.addEventListener('DOMContentLoaded', () => {
    const transferForm = document.getElementById('transfer-form');

    transferForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const currency = document.getElementById('currency').value;
        const amount = document.getElementById('amount').value;
        const alias = document.getElementById('alias').value;

        const userId = localStorage.getItem('idCliente');

        try {
            const response = await fetch(`${apiUrl}/transferir`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId,
                    currency,
                    amount,
                    alias
                })
            });

            if (!response.ok) {
                throw new Error('Error al realizar la transferencia');
            }

            const result = await response.json();
            alert('Transferencia realizada con éxito');
            // Redirigir o actualizar la página según sea necesario
        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un error al realizar la transferencia');
        }
    });
});