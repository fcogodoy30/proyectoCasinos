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

  blocks.forEach(block => {
    const selectedButton = block.querySelector('.button.selected');
    if (!selectedButton) {
      allSelected = false;
    }
  });

  if (allSelected) {
    alert("Formulario enviado con éxito.");
    // Aquí puedes agregar la lógica para enviar el formulario
  } else {
    alert("Por favor, selecciona una opción en todos los bloques.");
  }
}