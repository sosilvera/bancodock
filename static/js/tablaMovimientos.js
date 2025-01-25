/**
 * Genera una tabla con los movimientos y la inserta en el contenedor.
 * @param {Array} movimientos - Lista de movimientos [{fecha, descripcion, monto}].
 */
export function renderMovimientosTabla(movimientos) {
    // Crear la tabla
    const table = document.createElement('table');
    table.classList.add('movements-table'); // Clase para estilos
    table.innerHTML = `
        <thead>
            <tr>
                <th>Id</th>
                <th>Tipo</th>
                <th>Descripción</th>
                <th>Monto</th>
            </tr>
        </thead>
        <tbody>
            ${movimientos.map(mov => `
                <tr>
                    <td>${mov.id}</td>
                    <td>${mov.tipo}</td>
                    <td>${mov.descripcion}</td>
                    <td>${mov.monto}</td>
                </tr>
            `).join('')}
        </tbody>
    `;

    // Insertar la tabla en el contenedor
    const container = document.querySelector('.home-container');
    let tableContainer = document.querySelector('#table-container');

    if (!tableContainer) {
        tableContainer = document.createElement('div');
        tableContainer.id = 'table-container'; // Contenedor único para la tabla
        container.appendChild(tableContainer);
    }

    tableContainer.innerHTML = ''; // Limpiar cualquier tabla previa
    tableContainer.appendChild(table);

    // Centrar la pantalla en la tabla
    tableContainer.scrollIntoView({ behavior: 'smooth' });
}
