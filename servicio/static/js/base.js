function updateTime() {
    const timeElement = document.getElementById('time');
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const dateString = now.toLocaleDateString();
    timeElement.innerText = `Fecha y hora: ${dateString} ${timeString}`;
}

// Llamar a la función cada segundo para actualizar la hora
setInterval(updateTime, 1000);



// Get the login modal and the link to open it
var modal = document.getElementById("loginModal");
var loginLink = document.getElementById("loginLink");

// When the user clicks the link, open the modal
loginLink.onclick = function() {
  modal.style.display = "block";
};

// When the user clicks on the close button, close the modal
var closeBtn = document.getElementsByClassName("close")[0];
closeBtn.onclick = function() {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};



