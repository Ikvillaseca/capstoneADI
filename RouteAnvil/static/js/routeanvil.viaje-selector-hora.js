document.addEventListener('DOMContentLoaded', function() {
    // ===== VALIDACIÓN DE HORA EN FORMATO 24H =====
    const inputHora = document.getElementById('id_hora');
    
    if (inputHora) {
        // Formatear mientras el usuario escribe
        inputHora.addEventListener('input', function(e) {
            let valor = e.target.value.replace(/[^\d:]/g, ''); // Solo números y :
            
            // Auto-agregar : después de 2 dígitos
            if (valor.length === 2 && !valor.includes(':')) {
                valor += ':';
            }
            
            // Limitar a 5 caracteres (HH:MM)
            if (valor.length > 5) {
                valor = valor.substring(0, 5);
            }
            
            e.target.value = valor;
        });
        
        // Validar al salir del campo
        inputHora.addEventListener('blur', function(e) {
            const valor = e.target.value;
            
            if (valor) {
                const regex = /^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$/;
                
                if (!regex.test(valor)) {
                    e.target.classList.add('is-invalid');
                    
                    // Mostrar error
                    let errorDiv = e.target.parentElement.querySelector('.invalid-feedback');
                    if (!errorDiv) {
                        errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback d-block';
                        e.target.parentElement.appendChild(errorDiv);
                    }
                    errorDiv.textContent = 'Formato inválido. Use HH:MM (00:00 - 23:59)';
                } else {
                    e.target.classList.remove('is-invalid');
                    const errorDiv = e.target.parentElement.querySelector('.invalid-feedback');
                    if (errorDiv) errorDiv.remove();
                    
                    // Auto-completar con ceros
                    const partes = valor.split(':');
                    const horas = partes[0].padStart(2, '0');
                    const minutos = partes[1];
                    e.target.value = `${horas}:${minutos}`;
                }
            }
        });
        
        // Sugerencias de hora comunes
        inputHora.addEventListener('focus', function(e) {
            if (!e.target.value) {
                // Sugerir hora actual redondeada
                const ahora = new Date();
                const horas = String(ahora.getHours()).padStart(2, '0');
                const minutos = String(Math.round(ahora.getMinutes() / 15) * 15).padStart(2, '0');
                e.target.placeholder = `Ej: ${horas}:${minutos}`;
            }
        });
    }

    // ===== HACER CARDS CLICKEABLES =====
    document.querySelectorAll('.tipo-viaje-card, .tipo-hora-card').forEach(card => {
        card.addEventListener('click', function() {
            const radio = this.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
                actualizarTextoTipoHora();
            }
        });
    });

    // ===== ACTUALIZAR TEXTOS DINÁMICOS =====
    const radiosViaje = document.querySelectorAll('input[name="tipo_viaje"]');
    radiosViaje.forEach(radio => {
        radio.addEventListener('change', actualizarTextoTipoHora);
    });

    function actualizarTextoTipoHora() {
        const tipoViaje = document.querySelector('input[name="tipo_viaje"]:checked');
        const textoInicio = document.getElementById('texto-inicio');
        const textoFin = document.getElementById('texto-fin');
        
        if (textoInicio && textoFin && tipoViaje) {
            if (tipoViaje.value === 'IDA') {
                textoInicio.textContent = 'Hora en que se inicia a recoger pasajeros en sus paraderos';
                textoFin.textContent = 'Hora en que todos deben llegar al punto de encuentro';
            } else if (tipoViaje.value === 'VUELTA') {
                textoInicio.textContent = 'Hora en que se inicia a partir del punto de encuentro';
                textoFin.textContent = 'Hora en que todos deben llegar a sus paraderos';
            }
        }
    }

    // Inicializar textos
    actualizarTextoTipoHora();

    // ===== VALIDACIÓN DEL FORMULARIO =====
    const formulario = document.getElementById('formHorario');
    if (formulario) {
        formulario.addEventListener('submit', function(e) {
            const fecha = document.querySelector('input[name="fecha"]').value;
            const hora = document.getElementById('id_hora').value;
            const tipoViaje = document.querySelector('input[name="tipo_viaje"]:checked');
            const tipoHora = document.querySelector('input[name="tipo_hora_deseada"]:checked');

            // Validar hora formato 24h
            const regexHora = /^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$/;
            
            if (!hora || !regexHora.test(hora)) {
                e.preventDefault();
                alert('Por favor ingrese una hora válida en formato 24h (HH:MM)');
                document.getElementById('id_hora').focus();
                return false;
            }

            if (!fecha || !tipoViaje || !tipoHora) {
                e.preventDefault();
                alert('Por favor complete todos los campos requeridos');
                return false;
            }
        });
    }
    
    // ===== ESTABLECER FECHA MÍNIMA (HOY) =====
    const inputFecha = document.querySelector('input[name="fecha"]');
    if (inputFecha) {
        const hoy = new Date().toISOString().split('T')[0];
        inputFecha.setAttribute('min', hoy);
    }
});