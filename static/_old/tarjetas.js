const apiUrl = "http://127.0.0.1:3100/elegion"; 

async function getDetalles() {
    try {
        const response = await fetch(`${apiUrl}/getSaldo/${userId}`);
        const data = await response.json();
        document.getElementById("saldoPesos").textContent = data.saldoPesos;
    } catch (error) {
        console.error("Error al obtener el saldo:", error);
    }
}