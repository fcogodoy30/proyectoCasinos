$(document).ready(function() {
    // Initialize DataTable
    $('#menu-table').DataTable({
        "paging": true,
        "searching": true,
        "ordering": true,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.11.3/i18n/es_es.json"  // Localization for Spanish
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const switchCheckboxes = document.querySelectorAll('.switch-activo');
    switchCheckboxes.forEach(function(checkbox) {
      checkbox.addEventListener('change', function() {
        const usuarioId = this.getAttribute('data-usuario');
        const isChecked = this.checked;
  
        fetch('/cambiar_estado_usuario/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token }}'  // Asegúrate de tener el token CSRF disponible en tu plantilla
          },
          body: new URLSearchParams({
            usuario_id: usuarioId,
            activo: isChecked ? '1' : '0'
          }),
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            console.log('Estado cambiado exitosamente');
            location.reload();
          } else {
            console.error('Error al cambiar el estado');
          }
        })
        .catch(error => {
          console.error('Error de red:', error);
        });
      });
    });
  });



  $(document).ready(function() {
    $('.btn-edit').click(function() {
        const userId = $(this).data('id');
        
        // Obtener los datos del usuario y llenar el formulario
        $.ajax({
            url: '/usuarios/editar/' + userId + '/',
            type: 'GET',
            success: function(response) {
                $('#usuario_id').val(response.usuario.id);
                $('#id_username').val(response.usuario.rut);
                $('#tipousuario').val(response.usuario.tipo_usuario_id);
                $('#id_first_name').val(response.usuario.nombre);
                $('#id_last_name').val(response.usuario.apellido);
                $('#editUserModal').modal('show');
            }
        });
    });

    $('#saveChanges').click(function() {
        const userId = $('#usuario_id').val();
        const data = $('#editUserForm').serialize();

        $.ajax({
            url: '/usuarios/editar/' + userId + '/',
            type: 'POST',
            data: data,
            success: function(response) {
                if (response.status === 'success') {
                    location.reload(); // Recargar la página después de guardar los cambios
                } else {
                    alert('Hubo un error al actualizar el usuario.');
                }
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
  var password1Input = document.getElementById('id_password1');
  var password2Input = document.getElementById('id_password2');
  var mensajeError = document.getElementById('mensaje-error');
  var passwordPattern = /^[0-9]{4}$/;

  password2Input.addEventListener('blur', function() {
      var password1 = password1Input.value;
      var password2 = password2Input.value;

      if (password1 === '' && password2 === '') {
          // Ambos campos están vacíos, no hacemos nada
          mensajeError.textContent = '';
          return;
      }

      if (!passwordPattern.test(password2)) {
          mensajeError.textContent = 'La contraseña debe ser un número de 4 dígitos';
          password1Input.value = '';
          password2Input.value = '';
          password1Input.focus();
      } else if (password1 !== password2) {
          mensajeError.textContent = 'Las contraseñas no coinciden';
          password2Input.value = '';
          password2Input.focus();
      } else {
          mensajeError.textContent = '';
      }
  });
});