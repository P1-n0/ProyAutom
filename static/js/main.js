/**
 * Lógica Frontend para el Sistema de Gestión de Activos
 */
document.addEventListener('DOMContentLoaded', () => {

  const form = document.getElementById('equipoForm');
  const btnLimpiar = document.getElementById('btnLimpiar');
  const btnGuardar = document.getElementById('btnGuardar');
  const toastElement = document.getElementById('liveToast');
  
  // Si no está el formulario en la vista actual, detiene la ejecución
  if (!form) return;

  const toast = new bootstrap.Toast(toastElement);

  // MANEJO DEL ENVÍO DEL FORMULARIO VIA AJAX/FETCH
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validaciones de Bootstrap
    if (!form.checkValidity()) {
      e.stopPropagation();
      form.classList.add('was-validated');
      return;
    }

    const originalText = btnGuardar.innerHTML;
    btnGuardar.disabled = true;
    btnGuardar.innerHTML = `<span class="spinner-border spinner-border-sm"></span> Guardando...`;

    // Recopilar datos del formulario
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
      // Petición a la API de Flask (Ruta relativa automática)
      const response = await fetch('/api/equipo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const resData = await response.json();

      if (response.ok) {
        document.getElementById('toastMessage').textContent = resData.message || "Activo registrado con éxito.";
        toast.show();
        form.reset();
        form.classList.remove('was-validated');
      } else {
        alert("Error al registrar: " + resData.message);
      }
    } catch (error) {
      console.error("Error de conexión:", error);
      alert("Error de conexión con el servidor Flask.");
    } finally {
      btnGuardar.disabled = false;
      btnGuardar.innerHTML = originalText;
    }
  });

  // Botón Limpiar
  if (btnLimpiar) {
    btnLimpiar.addEventListener('click', () => {
      form.reset();
      form.classList.remove('was-validated');
    });
  }
});