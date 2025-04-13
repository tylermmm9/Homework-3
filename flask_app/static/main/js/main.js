const feedbackForm = document.getElementById('feedback');
const toggleButton = document.getElementById('buttonFeedback');
const loginButton = document.getElementById('login');

toggleButton.addEventListener('click', () => {
  if (feedbackForm.style.display === 'none') {
    feedbackForm.style.display = 'block';
  } else {
    feedbackForm.style.display = 'none';
  }
});
 
 function toggle_visibility() {
    var e = document.getElementById('feedback-main');
    if(e.style.display == 'block')
       e.style.display = 'none';
    else
       e.style.display = 'block';
 }