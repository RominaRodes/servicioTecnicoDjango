document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.nav-link');
    const tableBodies = document.querySelectorAll('.tabla-ordenes-body'); // Selecciona por clase

    tabs.forEach(tab => {
        tab.addEventListener('click', function (event) {
            event.preventDefault();
            const estado = this.getAttribute('data-estado');

            tabs.forEach(tab => tab.classList.remove('active'));
            this.classList.add('active');

            let url;
            if (estado === 'todas') {
                url = '/web/get_todas_las_ordenes';
            } else {
                url = `/web/get_ordenes_por_estado/${estado}`;
            }

            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.message === 'Success') {
                        tableBodies.forEach(tableBody => {
                            tableBody.innerHTML = '';
                            if (data.ordenes.length > 0) {
                                data.ordenes.forEach(ordenInfo => {
                                    const row = document.createElement('tr');
                                    row.innerHTML = `
                                        <td><a href="${urls.detalle_orden}${ordenInfo.orden.id}">${ordenInfo.orden.id}</a></td>
                                        <td>${new Date(ordenInfo.orden.fecha_ingreso).toLocaleDateString()}</td>
                                        <td>
                                            <a href="${urls.detalle_cliente}${ordenInfo.orden.cliente.id}">
                                                ${ordenInfo.orden.cliente.nombre} 
                                                ${ordenInfo.orden.cliente.empresa ? `<br>${ordenInfo.orden.cliente.razon_social}` : ''}
                                            </a>
                                        </td>
                                        <td>${ordenInfo.orden.maquina.categoria}</td>
                                        <td>${ordenInfo.orden.maquina.subcategoria}</td>
                                        <td>${ordenInfo.orden.maquina.modelo}</td>
                                        <td>${ordenInfo.orden.maquina.serie}</td>
                                        <td>${ordenInfo.accesorios.map(acc => acc.nombre).join(', ')}</td>
                                        <td>${ordenInfo.orden.garantia ? 'Sí' : 'No'}</td>
                                        <td>${new Date(ordenInfo.fecha_ultimo_estado).toLocaleDateString()}</td>
                                        <td>
                                            <span class="badge ${ordenInfo.ultimo_estado}">
                                                ${ordenInfo.ultimo_estado.charAt(0).toUpperCase() + ordenInfo.ultimo_estado.slice(1)}
                                            </span>
                                        </td>
                                        <td>${getBotones(ordenInfo)}</td>
                                        <td>${ordenInfo.ultimo_estado !== 'ingresada' && ordenInfo.presupuesto_id ? `<a href="${urls.detalle_presupuesto}${ordenInfo.presupuesto_id}">Ver P</a>` : ''}</td>
                                    `;
                                    tableBody.appendChild(row);
                                });
                            } else {
                                tableBody.innerHTML = `<tr><td colspan="13">No hay ordenes ${estado}</td></tr>`;
                            }
                        });
                    } else {
                        tableBodies.forEach(tableBody => {
                            tableBody.innerHTML = `<tr><td colspan="13">${data.message}</td></tr>`;
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    tableBodies.forEach(tableBody => {
                        tableBody.innerHTML = `<tr><td colspan="13">Error cargando las órdenes. Por favor, inténtalo de nuevo.</td></tr>`;
                    });
                });
        });
    });

    function getBotones(ordenInfo) {
        let botones = '';
        const id = ordenInfo.orden.id;
        const presupuesto_uuid = ordenInfo.presupuesto_uuid;
        const clienteNombre = ordenInfo.orden.cliente.empresa ? `${ordenInfo.orden.cliente.razon_social} - ${ordenInfo.orden.cliente.nombre} ${ordenInfo.orden.cliente.apellido}` : `${ordenInfo.orden.cliente.nombre} ${ordenInfo.orden.cliente.apellido}`;

        // Eliminar cualquier barra adicional al final de las URLs base
        const aceptarPresupuestoUrl = urls.aceptar_presupuesto.replace(/\/$/, '');
        const rechazarPresupuestoUrl = urls.rechazar_presupuesto.replace(/\/$/, '');

        switch (ordenInfo.ultimo_estado) {
            case 'ingresada':
                botones = `<a href="${urls.presupuestar_orden}${id}"><button class="btn btn-tbl presupuestar">Presupuestar</button></a>`;
                break;
            case 'presupuestada':
                if (presupuesto_uuid) {
                    botones = `
                        <a href="#" data-bs-toggle="modal" data-bs-target="#staticBackdrop" data-presupuesto-url="${aceptarPresupuestoUrl}/${presupuesto_uuid}" data-cliente-nombre="${clienteNombre}" data-orden-id="${id}" data-action="aceptar"><i class="fa-solid fa-circle-check aceptada"></i></a>
                        <a "#" data-bs-toggle="modal" data-bs-target="#staticBackdrop" data-presupuesto-url="${rechazarPresupuestoUrl}/${presupuesto_uuid}" data-cliente-nombre="${clienteNombre}" data-orden-id="${id}" data-action="rechazar"><i class="fa-regular fa-circle-xmark rechazada"></i></a>
                    `;
                    console.log(botones);
                }
                break;
            case 'aceptada':
                botones = `<a href="${urls.reparar_orden}${id}"><button class="btn btn-tbl reparada">Reparar</button></a>`;
                break;
            case 'reparada':
            case 'rechazada':
                botones = `<a href="${urls.entregar_orden}${id}"><button class="btn btn-tbl entregada">Para entregar</button></a>`;
                break;
        }

        return botones;
    }
});
