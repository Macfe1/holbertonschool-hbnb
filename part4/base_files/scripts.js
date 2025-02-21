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

/* function to extract the place_id
function getPlaceIdFromURL() {
  const URLparameters =  new URLSearchParams(window.location.search)
  console.log(URLparameters)
  const place_id = URLparameters.get('place_id')
  console.log(place_id)
}
*/
/*Check user authentication:*/
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.querySelector('.login-button');
  //const addReviewSection = document.getElementById('add-review');

  if (!token) {
    loginLink.style.display = 'block';
    //addReviewSection.style.display = 'none';
  } else {
    loginLink.style.display = 'none';
    fetchPlaces(token);
    //addReviewSection.style.display = 'block';
    // Store the token for later use
    //fetchPlaceDetails(token, placeId);
  }
}

function getCookie(name) {
  const cookies = document.cookie.split(';');

  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split('=');

    if (cookieName === name) {
      return cookieValue;
    }
  }
  return null;
}

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    displayPlaces(data);
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function populatePriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  const prices = ['All', '10', '50', '100'];
  
  prices.forEach(price => {
    const option = document.createElement('option');
    option.value = price;
    option.textContent = price === 'All' ? 'All' : `$${price}`;
    priceFilter.appendChild(option);
  });
}

function filterPlaces(maxPrice) {
  const placeCards = document.querySelectorAll('.place-card');
  
  placeCards.forEach(card => {
    const priceElement = card.querySelector('strong');
    const price = parseFloat(priceElement.textContent.replace('$', ''));
    
    if (maxPrice === 'All' || price <= parseFloat(maxPrice)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';
  
  places.forEach(place => {
    const placeCard = document.createElement('article');
    placeCard.className = 'place-card';
    
    placeCard.innerHTML = `
      <h3>${place.title}</h3>
      <p>Location: ${place.latitude}, ${place.longitude}</p>
      <p>Price: <strong>$${place.price}</strong></p>
      <button class="details-button">View Details</button>
    `;
    
    placesList.appendChild(placeCard);
  });
}

  
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

  checkAuthentication();
  populatePriceFilter();
  
  // Add event listener for price filter
  document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedPrice = event.target.value;
    filterPlaces(selectedPrice);
  });
});
