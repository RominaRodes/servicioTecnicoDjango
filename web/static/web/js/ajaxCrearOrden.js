const listarAccesorios = async (id_categoria) => {
    try {
        const response = await fetch(`crearorden/accesorios/${id_categoria}`);
        const data = await response.json();
        console.log(data);
        let opciones = `<option value="">------</option>`;
        if (data.message === 'Success') {
            data.accesorios.forEach((accesorio) => {
                opciones += `<option value=${accesorio.id}>${accesorio.nombre}</option>`;
            });
        } else {
            console.log('No existen accesorios...');
        }
        document.getElementById('id_accesorios').innerHTML = opciones;
    } catch (error) {
        console.log('Error al listar accesorios:', error);
        document.getElementById('id_accesorios').innerHTML = '<option value="">Error al cargar accesorios</option>';
    }
};

const listarModelos = async (id_subcategoria) => {
    try {
        const response = await fetch(`crearorden/modelos/${id_subcategoria}`);
        const data = await response.json();
        let opciones = `<option value="">------</option>`;
        if (data.message === 'Success') {
            data.modelos.forEach((modelo) => {
                opciones += `<option value="${modelo.id}">${modelo.nombre}</option>`;
            });
        } else {
            console.log('No existen modelos...');
        }
        attrmodelo.innerHTML = opciones;
    } catch (error) {
        console.log('Error al listar modelos:', error);
        attrmodelo.innerHTML = '<option value="">Error al cargar modelos</option>';
    }
};

const listarSubcategorias = async (id_categoria) => {
    try {
        const response = await fetch(`crearorden/subcategorias/${id_categoria}`);
        const data = await response.json();
        let opciones = `<option value="">------</option>`;
        if (data.message === 'Success') {
            data.subcategorias.forEach((subcategoria) => {
                opciones += `<option value="${subcategoria.id}">${subcategoria.nombre}</option>`;
            });
            attrsubcategoria.innerHTML = opciones;
            if (data.subcategorias.length > 0) {
                await listarModelos(data.subcategorias[0].id);
            } else {
                attrmodelo.innerHTML = '<option value="">No hay modelos disponibles</option>';
            }
            await listarAccesorios(id_categoria);
        } else {
            attrsubcategoria.innerHTML = '<option value="">No hay subcategorías disponibles</option>';
            attrmodelo.innerHTML = '<option value="">No hay modelos disponibles</option>';
            document.getElementById('id_accesorios').innerHTML = '<option value="">No hay accesorios disponibles</option>';
            console.log('No existen subcategorías...');
        }
    } catch (error) {
        console.log('Error al listar subcategorías:', error);
        attrsubcategoria.innerHTML = '<option value="">Error al cargar subcategorías</option>';
        attrmodelo.innerHTML = '<option value="">Error al cargar modelos</option>';
        document.getElementById('id_accesorios').innerHTML = '<option value="">Error al cargar accesorios</option>';
    }
};

const listarCategorias = async () => {
    try {
        const response = await fetch('crearorden/categorias');
        const data = await response.json();
        let opciones = `<option value="">------</option>`;
        if (data.message === 'Success') {
            data.categorias.forEach((categoria) => {
                opciones += `<option value="${categoria.id}">${categoria.nombre}</option>`;
            });
            attrcategoria.innerHTML = opciones;
            if (data.categorias.length > 0) {
                await listarSubcategorias(data.categorias[0].id);
            } else {
                attrsubcategoria.innerHTML = '<option value="">No hay subcategorías disponibles</option>';
                attrmodelo.innerHTML = '<option value="">No hay modelos disponibles</option>';
                document.getElementById('id_accesorios').innerHTML = '<option value="">No hay accesorios disponibles</option>';
            }
        } else {
            attrcategoria.innerHTML = '<option value="">No hay categorías disponibles</option>';
            attrsubcategoria.innerHTML = '<option value="">No hay subcategorías disponibles</option>';
            attrmodelo.innerHTML = '<option value="">No hay modelos disponibles</option>';
            document.getElementById('id_accesorios').innerHTML = '<option value="">No hay accesorios disponibles</option>';
            console.log('No existen categorías');
        }
    } catch (error) {
        console.log('Error al listar categorías:', error);
        attrcategoria.innerHTML = '<option value="">Error al cargar categorías</option>';
        attrsubcategoria.innerHTML = '<option value="">Error al cargar subcategorías</option>';
        attrmodelo.innerHTML = '<option value="">Error al cargar modelos</option>';
        document.getElementById('id_accesorios').innerHTML = '<option value="">Error al cargar accesorios</option>';
    }
};

const cargaInicial = async () => {
    await listarCategorias();

    attrcategoria.addEventListener('change', async (event) => {
        await listarSubcategorias(event.target.value);
        await listarAccesorios(event.target.value);
    });

    attrsubcategoria.addEventListener('change', async (event) => {
        await listarModelos(event.target.value);
    });
};

window.addEventListener('load', async () => {
    await cargaInicial();
});






// const listarAccesorios = async (id_categoria) => {
//     try {
//         const response = await fetch(`crearorden/accesorios/${id_categoria}`);
//         const data = await response.json();
//         console.log(data);
//         if (data.message === 'Success') {
//             let opciones = ``;
//             data.accesorios.forEach((accesorio) => {
//                 opciones +=
//                     `<option value=${accesorio.id} >${accesorio.nombre}</option>`
//             });
//             document.getElementById('id_accesorios').innerHTML = opciones;
//         } else {
//             document.getElementById('id_accesorios').innerHTML = '<p>No hay accesorios disponibles</p>';
//             console.log('No existen accesorios...');
//         }
//     } catch (error) {
//         console.log('Error al listar accesorios:', error);
//         document.getElementById('id_accesorios').innerHTML = '<p>Error al cargar accesorios</p>';
//     }
// };



// const listarModelos = async (id_subcategoria) => {
//     try {
//         const response = await fetch(`crearorden/modelos/${id_subcategoria}`);
//         const data = await response.json();
//         if (data.message === 'Success') {
//             let opciones = ``;
//             data.modelos.forEach((modelo) => {
//                 opciones += `<option value="${modelo.id}">${modelo.nombre}</option>`;
//             });
//             attrmodelo.innerHTML = opciones;
//         } else {
//             attrmodelo.innerHTML = '<option value="">No hay modelos disponibles</option>';
//             console.log('No existen modelos...');
//         }
//     } catch (error) {
//         console.log('Error al listar modelos:', error);
//         attrmodelo.innerHTML = '<option value="">Error al cargar modelos</option>';
//     }
// };

// const listarSubcategorias = async (id_categoria) => {
//     try {
//         const response = await fetch(`crearorden/subcategorias/${id_categoria}`);
//         const data = await response.json();
//         if (data.message === 'Success') {
//             let opciones = ``;
//             data.subcategorias.forEach((subcategoria) => {
//                 opciones += `<option value="${subcategoria.id}">${subcategoria.nombre}</option>`;
//             });
//             attrsubcategoria.innerHTML = opciones;
//             // Listar modelos de la primera subcategoría
//             if (data.subcategorias.length > 0) {
//                 await listarModelos(data.subcategorias[0].id);
//             } else {
//                 attrmodelo.innerHTML = '<option value="">No hay modelos disponibles</option>';
//             }
//             // Listar accesorios de la categoría seleccionada
//             await listarAccesorios(id_categoria);
//         } else {
//             attrsubcategoria.innerHTML = '<option value="">No hay subcategorías disponibles</option>';
//             attrmodelo.innerHTML = '<option value="">No hay modelos disponibles</option>';
//             document.getElementById('id_accesorios').innerHTML = '<p>No hay accesorios disponibles</p>';
//             console.log('No existen subcategorías...');
//         }
//     } catch (error) {
//         console.log('Error al listar subcategorías:', error);
//         attrsubcategoria.innerHTML = '<option value="">Error al cargar subcategorías</option>';
//         attrmodelo.innerHTML = '<option value="">Error al cargar modelos</option>';
//         document.getElementById('id_accesorios').innerHTML = '<p>Error al cargar accesorios</p>';
//     }
// };

// const listarCategorias = async () => {
//     try {
//         const response = await fetch('crearorden/categorias');
//         const data = await response.json();
//         if (data.message === 'Success') {
//             let opciones = ``;
//             data.categorias.forEach((categoria) => {
//                 opciones += `<option value="${categoria.id}">${categoria.nombre}</option>`;
//             });
//             attrcategoria.innerHTML = opciones;
//             // Listar subcategorías y modelos de la primera categoría
//             if (data.categorias.length > 0) {
//                 await listarSubcategorias(data.categorias[0].id);
//             } else {
//                 attrsubcategoria.innerHTML = '<option value="">No hay subcategorías disponibles</option>';
//                 attrmodelo.innerHTML = '<option value="">No hay modelos disponibles</option>';
//                 document.getElementById('attraccesorios').innerHTML = '<p>No hay accesorios disponibles</p>';
//             }
//         } else {
//             attrcategoria.innerHTML = '<option value="">No hay categorías disponibles</option>';
//             attrsubcategoria.innerHTML = '<option value="">No hay subcategorías disponibles</option>';
//             attrmodelo.innerHTML = '<option value="">No hay modelos disponibles</option>';
//             document.getElementById('id_accesorios').innerHTML = '<p>No hay accesorios disponibles</p>';
//             console.log('No existen categorías');
//         }
//     } catch (error) {
//         console.log('Error al listar categorías:', error);
//         attrcategoria.innerHTML = '<option value="">Error al cargar categorías</option>';
//         attrsubcategoria.innerHTML = '<option value="">Error al cargar subcategorías</option>';
//         attrmodelo.innerHTML = '<option value="">Error al cargar modelos</option>';
//         document.getElementById('id_accesorios').innerHTML = '<p>Error al cargar accesorios</p>';
//     }
// };
// const cargaInicial = async () => {
//     await listarCategorias();

//     attrcategoria.addEventListener('change', async (event) => {
//         await listarSubcategorias(event.target.value);
//         await listarAccesorios(event.target.value); // Listar accesorios al cambiar la categoría
//     });

//     attrsubcategoria.addEventListener('change', async (event) => {
//         await listarModelos(event.target.value);
//     });
// };

// window.addEventListener('load', async () => {
//     await cargaInicial();
// });