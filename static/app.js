// Cambia la URL por la ruta real de tu API
const apiUrl = "http://127.0.0.1:3100/elegion"; 
userId = 1

// Nueva función para realizar el inicio de sesión
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${apiUrl}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'user': username, 'passw': password }),
        });

        userId = await response.json();

        if (userId > 0) {
            // Si el inicio de sesión es exitoso, oculta el formulario y muestra el contenido
            document.getElementById('loginForm').style.display = 'none';
            document.querySelector('.saldo-container').style.display = 'flex';
            document.getElementById('botonera').style.display = 'flex';
            // Llama a la función getSaldo con el userId
            getSaldo(userId);
        } else {
            // Si el inicio de sesión falla, muestra un mensaje o realiza alguna acción
            alert('Inicio de sesión fallido. Verifica tu usuario y contraseña.');
        }
    } catch (error) {
        console.error('Error al realizar el inicio de sesión:', error);
    }
}

// Función para obtener el saldo desde la API
async function getSaldo() {
    try {
        const response = await fetch(`${apiUrl}/getSaldo/${userId}`);
        const data = await response.json();
        document.getElementById("saldoPesos").textContent = data.saldoPesos;
        document.getElementById("saldoDolar").textContent = data.saldoDolar;
    } catch (error) {
        console.error("Error al obtener el saldo:", error);
    }
}

// Funciones para llamar a las API de detalles de movimientos, tarjetas y préstamos
async function getMovimientos() {
    try {
        const response = await fetch(`${apiUrl}/getMovimientos/${userId}`);
        const data = await response.json();
        // Llama a la función para crear la tabla
        createTableMovimientos(data.listaMovimientos);
    } catch (error) {
        console.error("Error al obtener detalles de movimientos:", error);
    }
}

async function getTarjetas() {
    try {
        const response = await fetch(`${apiUrl}/getTarjetas/${userId}`);
        const data = await response.json();
        createTarjetasRectangles(data);
    } catch (error) {
        console.error("Error al obtener tarjetas:", error);
    }
}

async function getPrestamos() {
    try {
        const response = await fetch(`${apiUrl}/getPrestamosActivos/${userId}`);
        const data = await response.json();
        createPrestamosTable(data);
    } catch (error) {
        console.error("Error al obtener préstamos:", error);
    }
}

// Función para mostrar el resultado en el contenedor
function mostrarResultado(resultado) {
    document.getElementById("resultContainer").textContent = resultado;
}

// Función para crear la tabla
function createTableMovimientos(data) {
    // Encuentra el contenedor donde se mostrará la tabla
    const resultContainer = document.getElementById('resultContainer');

    // Crea una tabla y agrega clases de Bootstrap para el estilo
    const table = document.createElement('table');
    table.classList.add('table', 'table-bordered', 'table-striped');

    // Crea la cabecera de la tabla
    const thead = document.createElement('thead');
    const headRow = document.createElement('tr');
    ['ID', 'Tipo', 'Descripción', 'Monto'].forEach((headerText) => {
        const th = document.createElement('th');
        th.textContent = headerText;
        headRow.appendChild(th);
    });
    thead.appendChild(headRow);
    table.appendChild(thead);

    // Crea el cuerpo de la tabla
    const tbody = document.createElement('tbody');
    data.forEach((movimiento) => {
        const row = document.createElement('tr');
        ['id', 'tipo', 'descripcion', 'monto'].forEach((key) => {
            const cell = document.createElement('td');
            cell.textContent = movimiento[key];
            row.appendChild(cell);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    // Limpia el contenedor y agrega la nueva tabla
    resultContainer.innerHTML = '';
    resultContainer.appendChild(table);
}

// Función para crear la tabla de préstamos activos
// Función para crear la tabla de préstamos activos
function createPrestamosTable(data) {
    // Encuentra el contenedor donde se mostrará la tabla
    const resultContainer = document.getElementById('resultContainer');

    // Verifica si data es un array
    if (!Array.isArray(data)) {
        resultContainer.innerHTML = data;
        return;
    }

    // Crea una tabla y agrega clases de Bootstrap para el estilo
    const table = document.createElement('table');
    table.classList.add('table', 'table-bordered', 'table-striped');

    // Crea la cabecera de la tabla
    const thead = document.createElement('thead');
    const headRow = document.createElement('tr');
    ['Monto Solicitado', 'Monto Próxima Cuota', 'Cuota Actual', 'Cantidad Cuotas', 'Vencimiento Próxima Cuota', 'Tipo de Préstamo'].forEach((headerText) => {
        const th = document.createElement('th');
        th.textContent = headerText;
        headRow.appendChild(th);
    });
    thead.appendChild(headRow);
    table.appendChild(thead);

    // Crea el cuerpo de la tabla
    const tbody = document.createElement('tbody');
    data.forEach((prestamo) => {
        const row = document.createElement('tr');
        ['MontoSolicitado', 'MontoProximaCuota', 'cuotaActual', 'CantidadCuotas', 'VencimientoProximaCuota', 'DescripcionTipoPrestamo'].forEach((key) => {
            const cell = document.createElement('td');
            cell.textContent = prestamo[key];
            row.appendChild(cell);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    // Limpia el contenedor y agrega la nueva tabla
    resultContainer.innerHTML = '';
    resultContainer.appendChild(table);
}

// Función para crear los rectángulos de las tarjetas
function createTarjetasRectangles(data) {
    // Encuentra el contenedor donde se mostrarán las tarjetas
    const resultContainer = document.getElementById('resultContainer');

    // Verifica si data es un array y tiene elementos
    if (!Array.isArray(data) || data.length === 0) {
        resultContainer.innerHTML = 'No hay tarjetas disponibles.';
        return;
    }

    // Crea un contenedor div para las tarjetas
    const tarjetasContainer = document.createElement('div');

    // Itera sobre cada tarjeta y crea un rectángulo para cada una
    data.forEach((tarjeta) => {
        // Crea un elemento div para representar visualmente la tarjeta
        const tarjetaDiv = document.createElement('div');
        tarjetaDiv.classList.add('tarjeta'); // Agrega una clase para aplicar estilos

        // Agrega el número de la tarjeta y el tipo
        tarjetaDiv.innerHTML = `<p>${'****' + tarjeta.numero}</p><p>${tarjeta.tipo}</p>`;

        // Agrega un evento de clic al div para redirigir a la página de detalles
        tarjetaDiv.addEventListener('click', function () {
            // Redirecciona a la página de detalles (ajusta la URL según tus necesidades)
            window.location.href = `/detalles_tarjeta/${tarjeta.id}`;
        });

        // Agrega el rectángulo de la tarjeta al contenedor
        tarjetasContainer.appendChild(tarjetaDiv);
    });

    // Limpia el contenedor y agrega los nuevos rectángulos de tarjetas
    resultContainer.innerHTML = '';
    resultContainer.appendChild(tarjetasContainer);
}

// Llamar a la función getSaldo al cargar la página
getSaldo();
