
// Espera 5 segundos y luego cierra la alerta
setTimeout(function() {
  var alertElement = document.getElementById('customxD');
  var alert = new mdb.Alert(alertElement);
  alert.dispose();  // Cierra la alerta
}, 5000); //


// SPINNER DE CARGA DE LOGIN
$(document).ready(function() {
    $('#loginForm').on('submit', function() {
      $('#loadingSpinner').show(); // Mostrar el spinner
    });
  });