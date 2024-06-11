function validarRut(rut) {
    // Remover puntos y guiones
    rut = rut.replace(/\./g, "").replace(/-/g, "").toUpperCase();
    
    // Validar formato básico
    if (!/^\d{7,8}[0-9K]$/.test(rut)) {
        return false;
    }
  
    let cuerpo = rut.slice(0, -1);
    let dv = rut.slice(-1);
  
    let suma = 0;
    let multiplo = 2;
  
    for (let i = cuerpo.length - 1; i >= 0; i--) {
        suma += parseInt(cuerpo.charAt(i)) * multiplo;
        multiplo = multiplo === 7 ? 2 : multiplo + 1;
    }
  
    let resto = suma % 11;
    let dvCalculado = resto === 1 ? 'K' : (11 - resto).toString();
    dvCalculado = resto === 0 ? '0' : dvCalculado;
  
    return dv === dvCalculado;
  }
  
  function formatearRut(rut) {
    // Remover puntos y guiones
    rut = rut.replace(/\./g, "").replace(/-/g, "");
    // Agregar puntos y guión
    return rut.replace(/^(\d{1,2})(\d{3})(\d{3})([0-9K])$/, "$1.$2.$3-$4");
  }
  
  function validarRutInput() {
    const rutInput = document.getElementById('id_rut');
    const rutValue = rutInput.value;
  
    // Formatear el RUT y actualizar el valor del input
    const rutFormateado = formatearRut(rutValue);
    rutInput.value = rutFormateado;
  
    if (validarRut(rutFormateado)) {
        rutInput.setCustomValidity('');
        rutInput.style.borderColor = 'green';
    } else {
        rutInput.setCustomValidity('RUT inválido');
        rutInput.style.borderColor = 'red';
    }
  }
  
  document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('id_rut');
    rutInput.addEventListener('input', validarRutInput);
  });