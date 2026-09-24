document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('equipoForm');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();


    const formData = {
      tipoDispositivo: document.getElementById('tipoDispositivo').value,
      numeroSerie: document.getElementById('numeroSerie').value,
      marca: document.getElementById('marca').value,
      modelo: document.getElementById('modelo').value,
      usuarioAsignado: document.getElementById('usuarioAsignado').value,
      ram: document.getElementById('ram').value,
      almacenamiento: document.getElementById('almacenamiento').value,
      procesador: document.getElementById('procesador').value,
      sistemaOperativo: document.getElementById('sistemaOperativo').value,
      tipoLicencia: document.getElementById('tipoLicencia').value,
      licenciaActiva: document.getElementById('licenciaActiva').checked
    };

    try {

      const response = await fetch('/api/equipo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const result = await response.json();

      if (response.ok) {
        alert('Equipo guardado exitosamente');
        console.log('Respuesta del servidor:', result);
      } else {
        alert('Error al guardar el equipo');
      }
    } catch (error) {
      console.error('Error de conexión:', error);
      alert('No se pudo conectar con el servidor en Python');
    }
  });
});