document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const message = urlParams.get('message');
    if (message) {
      const messageDiv = document.getElementById('message');
      if (messageDiv) {
        messageDiv.textContent = decodeURIComponent(message);
      }
    }
  });