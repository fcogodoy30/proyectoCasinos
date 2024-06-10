function selectOption(button) {
  const buttons = button.parentNode.querySelectorAll('.button');
  buttons.forEach(btn => {
    btn.classList.remove('selected');
  });
  button.classList.add('selected');
}

function validateSelection() {
  const blocks = document.querySelectorAll('.block');
  let allSelected = true;
  const selections = [];

  blocks.forEach(block => {
    const selectedButton = block.querySelector('.button.selected');
    if (!selectedButton) {
      allSelected = false;
    } else {
      const selectedValue = selectedButton.value;
      const fechaServicio = selectedButton.getAttribute('data-fecha');
      selections.push({
        fecha_servicio: fechaServicio,
        opcion_id: selectedValue
      });
    }
  });

  if (allSelected) {
    alert("Formulario enviado con éxito.");

    // Enviar los datos seleccionados al servidor usando fetch (AJAX)
    fetch('/guardar_selecciones/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') // Añade el token CSRF si estás usando Django
      },
      body: JSON.stringify(selections)
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        console.log('Success:', data);
        // Aquí puedes manejar la respuesta del servidor
      } else {
        console.error('Error:', data);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });

  } else {
    alert("Por favor, selecciona una opción en todos los bloques.");
  }
}

// Función auxiliar para obtener el token CSRF (si usas Django)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
