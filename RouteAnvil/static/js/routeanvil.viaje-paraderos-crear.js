function inicializar_mapa(api_embed) {
    // Obtener todos los datos necesarios
    const API_KEY = api_embed;
    const direccionInput = document.getElementById('id_direccion');
    const mapIframe = document.getElementById('mapIframe');
    const mapPlaceholder = document.getElementById('mapPlaceholder');
    const updateMapBtn = document.getElementById('updateMapBtn');

    function actualizarMapa() {
        // Construir URL del iframe
        const direccion = direccionInput.value.trim();
        const direccionCodificada = encodeURIComponent(direccion);
        const mapUrl = `https://www.google.com/maps/embed/v1/place?key=${API_KEY}&q=${direccionCodificada}`;
        
        // Actualizar src del iframe
        mapIframe.src = mapUrl;
    }

    // Event listener para el botón "Actualizar Mapa"
    updateMapBtn.addEventListener('click', function(e) {
        if(direccionInput.value.trim()) {
            e.preventDefault();
            actualizarMapa();
        }
    });

    // Event listener para detectar Enter en el input de dirección
    direccionInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' & direccionInput.value.trim()) {
            e.preventDefault();
            actualizarMapa();
        }
    });

    // Actualizar mapa automaticamente cuando se clickea afuera
    direccionInput.addEventListener('blur', function() {
        if (direccionInput.value.trim()) {
            actualizarMapa();
        }
    });

    // Si hay texto inicial
    window.addEventListener('DOMContentLoaded', function() {
        if (direccionInput.value.trim()) {
            actualizarMapa();
        }
    });

}
