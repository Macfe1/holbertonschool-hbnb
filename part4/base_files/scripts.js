document.addEventListener('DOMContentLoaded', () => {
  /*Login */ 
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      /*email and password input*/
      const emailValue = document.getElementById('email').value
      const passwordValue = document.getElementById('password').value
      const response = await loginUser(emailValue, passwordValue)
      console.log(response);
    });
  }
});
/* function to login user */
async function loginUser(email, password) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
    return data;
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

/* function to extract the place_id*/
function getPlaceIdFromURL() {
  const URLparameters =  new URLSearchParams(window.location.search)
  console.log(URLparameters)
  const place_id = URLparameters.get('place_id')
  console.log(place_id)
}
/*Check user authentication:*/
function checkAuthentication() {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
      addReviewSection.style.display = 'none';
  } else {
      addReviewSection.style.display = 'block';
      // Store the token for later use
      fetchPlaceDetails(token, placeId);
  }
}

function getCookie(name) {
  // Function to get a cookie value by its name
  // Your code here
}