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
    const response = await fetch('/api/v1/places/', {
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

function checkAuthentication() {
  const token = getCookie('jwt');
  const loginLink = document.querySelector('.login-button');

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

function populatePriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  const prices = ['10', '50', '100', 'All'];
  
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
      <button class="details-button">View Details</button>
    `;
    
    placesList.appendChild(placeCard);
  });
}

  
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  populatePriceFilter();
  
  // Add event listener for price filter
  document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedPrice = event.target.value;
    filterPlaces(selectedPrice);
  });
});