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

// function to extract the place_id//
function getPlaceIdFromURL() {
  const parts = window.location.pathname.split('/');

  const placeIndex = parts.indexOf('places') + 1;

  //If places doesn't exists return -1
  if (parts.indexOf('places') === -1) {
    throw new Error("Error: No place_id found in the URL");
  }
  
  if (placeIndex <= 0 || placeIndex >= parts.length) {  
    throw new Error("Error: No place_id found in the URL");
  }
  return parts[placeIndex];
}

// Get cookie function
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

//Get place details function
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}: ${response.statusText}`); 
    }
    const data = await response.json();
    displayPlaceDetails(data)
  } catch (error) {
    console.error('Error fetching place details:', error)
    alert('Failed to retrieve place details: ' + error.message);
  }
}

//Organize de place details in the HTML//
function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');

  const title = document.createElement("h2");
  title.textContent = place.title;

  const divPlaceInfo = document.createElement("div");
  divPlaceInfo.classList.add("place-info");

  const description = document.createElement("p");
  description.textContent = place.description;

  const mainDetails = document.createElement("ul");

  const longitude = document.createElement("li");
  longitude.textContent = ` Longitude: ${place.longitude}`;

  const latitude = document.createElement("li");

  latitude.textContent = `Latitude: ${place.latitude}`;
  const price = document.createElement("li");

  price.textContent = `Price: $${place.price}`;

  placeDetails.replaceChildren()//To clear the previous Place

  placeDetails.appendChild(title);
  placeDetails.appendChild(divPlaceInfo);
  divPlaceInfo.appendChild(description);
  divPlaceInfo.appendChild(mainDetails);
  mainDetails.appendChild(longitude);
  mainDetails.appendChild(latitude);
  mainDetails.appendChild(price);

  const reviews = document.getElementById('review-list');
  reviews.replaceChildren();

  if (!place.reviews || !place.reviews.length){
    console.log('No reviews found for this place.');
    const noReviews = document.createElement("p");
    noReviews.textContent = "No reviews available.";
    reviews.appendChild(noReviews);
    return; // Getting out of the function to avoiding the forEach
}

  place.reviews.forEach(review => {

    const reviewCard = document.createElement("article");
    reviewCard.classList.add("review-card")

    const user = document.createElement("span");
    user.classList.add("review-username")
    user.textContent = review.user_id;

    // rating between 1 - 5
    const ratingValue = Math.min(5, Math.max(1, review.rating || 1)); 

    const rating = document.createElement("span");
    rating.classList.add("review-rating")
    rating.innerHTML = "⭐".repeat(ratingValue);

    const reviewComment = document.createElement("p");
    reviewComment.textContent = review.text;

    reviews.appendChild(reviewCard);
    reviewCard.appendChild(user);
    reviewCard.appendChild(rating);
    reviewCard.appendChild(reviewComment);
  });
}

/*Check user authentication:*/
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.querySelector('.login-button');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
    loginLink.style.display = 'block';
    addReviewSection.style.display = 'none';
  } else {
    loginLink.style.display = 'none';
    addReviewSection.style.display = 'block';
    fetchPlaces(token);
    placeId = getPlaceIdFromURL()
    fetchPlaceDetails(token, placeId);
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
