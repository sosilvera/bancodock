/**
 * Genera una tabla con las tarjetas y la inserta en el contenedor.
 * @param {Array} tarjetas - Lista de tarjetas [{tipo, numero}].
 */
export function renderTarjetasTabla(tarjetas) {
    // Crear la tabla
    const table = document.createElement('table');
    table.classList.add('tarjetas-table'); // Clase para estilos
    table.innerHTML = `
        <thead>
            <tr>
                <th>Tipo</th>
                <th>Numero</th>
                <th>Monto Periodo actual</th>
            </tr>
        </thead>
        <tbody>
            ${tarjetas.map(t => `
                <tr>
                    <td>${t.tipo}</td>
                    <td>${t.numero}</td>
                    <td></td>
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