// Replace login.js content with:
document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('login');
  const attemptsEl = document.getElementById('attempts');
  const countDisplay = document.getElementById('count-display');
  const errorDiv = document.getElementById('login-error');
  
  let failedAttempts = 0;

  loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const formData = new FormData(loginForm);
      const data = Object.fromEntries(formData.entries());
      
      fetch('/processlogin', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
          if (data.status === 'success') {
              window.location.href = '/home';
          } else {
              failedAttempts++;
              attemptsEl.style.display = 'block';
              countDisplay.textContent = failedAttempts;
              errorDiv.textContent = data.error || 'Login failed';
          }
      })
      .catch(error => {
          console.error('Error:', error);
          errorDiv.textContent = 'An unexpected error occurred';
      });
  });
});