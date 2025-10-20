function inicializar() {
    // Envolver en try-catch para evitar errores de JS que bloqueen funcionalidad
    try {
        setupPasajeroFilters();
        setupItemClickeable();
    } catch (error) {
        console.error("Error al inicializar:", error);
    }
}

// Función para configurar los filtros de pasajeros por empresa
function setupPasajeroFilters() {
    // Seleccionar todos los botones de filtro de empresa
    const empresaFilters = document.querySelectorAll('.empresa-filter');
    
    if (!empresaFilters || empresaFilters.length === 0) {
        console.warn("No se encontraron filtros de empresa");
        return;
    }
    
    // Agregar el evento click a cada botón
    empresaFilters.forEach(button => {
        button.addEventListener('click', function(e) {
            // Prevenir comportamiento predeterminado de botones
            e.preventDefault();
        
            // Quitar la clase active de todos los botones
            empresaFilters.forEach(btn => btn.classList.remove('active'));
    
            // Agregar la clase active al botón clickeado
            this.classList.add('active');
            const empresaSeleccionada = this.dataset.empresa || 'todos';
            
            // Obtener todos los items de pasajeros
            const pasajeros = document.querySelectorAll('.pasajero-item');
            
            // Contar elementos visibles para a lo mejor agregar un contador
            let elementosVisibles = 0;
            
            // Filtrar los pasajeros según la empresa seleccionada
            pasajeros.forEach(pasajero => {
                if (empresaSeleccionada === 'todos') {
                    // Si es "todos", mostrar todos los pasajeros
                    pasajero.style.display = 'block';
                    elementosVisibles++;
                } else {
                    // Comparar con la empresa del pasajero usando dataset
                    const empresaPasajero = pasajero.dataset.empresa || '';
                    if (empresaPasajero === empresaSeleccionada) {
                        pasajero.style.display = 'block';
                        elementosVisibles++;
                    } else {
                        pasajero.style.display = 'none';
                    }
                }
            });
            
            // Caso en el que no hay pasajeros para la empresa
            if (elementosVisibles === 0) {
                console.log("No hay pasajeros para esta empresa");
            }
        });
    });
}

function setupItemClickeable() {
    // Lista de todos los pasajero-item
    const pasajeroItems = document.querySelectorAll('.pasajero-item');
    
    // Hacerlos clickeables
    pasajeroItems.forEach(item => {
        item.addEventListener('click', function(event) {
            // Buscar el checkbox
            const checkbox = this.querySelector('input[type="checkbox"]');
            const label = this.querySelector('label[class="form-check-label pasajero-label"]');
            const small = this.querySelector('small[class="text-muted"]');
            
            // No activar si se clickeo la caja o sino se hace doble
            if (event.target !== checkbox) {
                checkbox.checked = !checkbox.checked;
                //Arreglo para permitir clickear el texto
                if (event.target == label || event.target == small) {
                    checkbox.checked = !checkbox.checked;        
                }
            }
        });
    });
}

// Añadir función para seleccionar/deseleccionar todos los pasajeros visibles
function selectAllVisible(checked) {
    try {
        const pasajeros = document.querySelectorAll('.pasajero-item');
        //let contadorActualizados = 0;
        
        pasajeros.forEach(pasajero => {
            // Verificar si el elemento está visible
            const esVisible = window.getComputedStyle(pasajero).display !== 'none';
            if (esVisible) {
                const checkbox = pasajero.querySelector('input[type="checkbox"]');
                if (checkbox && !checkbox.disabled) {
                    checkbox.checked = checked;
                    //contadorActualizados++;
                }
            }
        });
        //console.log(`${checked ? 'Seleccionados' : 'Deseleccionados'} ${contadorActualizados} pasajeros visibles`);
    } catch (error) {
        console.error("Error al seleccionar/deseleccionar pasajeros:", error);
        return 0;
    }
}
