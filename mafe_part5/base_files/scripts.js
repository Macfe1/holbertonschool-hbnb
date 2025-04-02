// Main process
document.addEventListener('DOMContentLoaded', () => {

  checkAuthentication();

  const priceFilter = document.getElementById("price-filter");
  if (priceFilter) {
    populatePriceFilter();
  } else {
    console.warn("⚠️ No se encontró #price-filter en esta página.");
  }

  // Modal in index.html
  const modal = document.getElementById('loginModal');

  if (modal) {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.querySelector('.close');

    // Open modal
    if (openModalButton) {
      openModalButton.addEventListener('click', () => {
        modal.style.display = 'flex';
      });
    }

    // Close the modal with the "X"
    if (closeModalButton) {
      closeModalButton.addEventListener('click', () => {
        modal.style.display = 'none';
      });
    }

    // Close the modal if there's a click out of it
    window.addEventListener('click', (event) => {
      if (event.target === modal) {
        modal.style.display = 'none';
      }
    });
  } else {
    console.warn("⚠️ There is no modal in the page. Skip the modal logic");
  }

  // Login
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      // email and password input
      const emailValue = document.getElementById('email').value;
      const passwordValue = document.getElementById('password').value;
      const response = await loginUser(emailValue, passwordValue);
      console.log(response);
    });
  }

  // Add event listener for price filter
  if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
      const selectedPrice = event.target.value;
      filterPlaces(selectedPrice);
    });
  } else {
    console.warn("⚠️ No se encontró #price-filter en esta página.");
  }

  // Add event listener to send the place_id in the Add a Review button 
  const placeId = getPlaceIdFromURL();
  const addReviewSection = document.getElementById('add-review-button-place');
  if (addReviewSection) {
    addReviewSection.addEventListener('click', () => {
      window.location.href = `add_review.html?id=${placeId}`;
    });
  } else {
    console.warn("The addReviewSection is not present in this page");
  }

  // Review Form
  console.log("Buscando reviewForm...");
  const reviewForm = document.getElementById('review-form');
  console.log("🟢 reviewForm:", reviewForm);
  if (reviewForm) {
    const token = getCookie('token');
    console.log('Token:', token);
    let placeId;
    
    try {
      placeId = getPlaceIdFromURL();
      console.log("placeId: ", placeId);

      // Add place title to the review form
      fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(place => {
        const formTitle = document.querySelector('#review-form h2');
        formTitle.textContent = `Add Review for ${place.title}`;
      })
      .catch(error => console.error('Error fetching place title:', error));
      
    } catch (error) {
      console.error('Error getting place ID:', error);
      return;
    }

    // Submit the review
    const submitButton = document.querySelector('#review-form button[type="submit"]');    
    console.log("Submit button", document.querySelector('#review-form button[type="submit"]'));
    if (submitButton) {
      submitButton.addEventListener('click', async (event) => {
        event.preventDefault();
        console.log("✅ DOM completamente cargado");
        console.log("Submit button clicked!");

        const reviewText = document.getElementById('review').value;
        const rating = parseInt(document.getElementById('rating').value);
        console.log("review_text", document.getElementById('review').value)


        if (!rating || !reviewText.trim()) {
          alert('Please fill in all fields');
          return;
        }

        let userIdToken;
        try {
          userIdToken = getUserIdFromToken(token);
        } catch (error) {
          return;
        }
        console.log("🔍 Token obtenido: 😁", token);
        console.log("userIdToken:😁", userIdToken)

        if (!userIdToken) {
          console.error("User ID not found in token");
          alert("Authentication error. Please log in again.");
          return;
        }

        console.log("Token in REVIEW:", token);
        console.log("placeId:", placeId);

        try {
          const reviewData = {
            text: reviewText.trim(),
            rating: rating,
            place_id: placeId,
            user_id: userIdToken
          };

          await submitReview(reviewData, token);
          
          // Clear the form
          document.getElementById('review').value = '';
          document.getElementById('rating').value = '';
        
          // Show success message and redirect
          alert('Review submitted successfully!');
          window.location.href = `place.html?id=${placeId}`;
        } catch (error) {
          console.error('Review submission error:', error);

          if (error.message.includes('already reviewed')) {
            alert('You have already submitted a review for this place');
          } else if (error.message.includes('own place')) {
            alert('You cannot review your own place');
          } else {
            alert('Failed to submit review: ' + error.message);
          }
        }
      });
    }
  }
});


// Check user authentication:
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.querySelector('.login-button');
  const logOutButton = document.querySelector('.log-out-button');
  const addReviewSection = document.getElementById('add-review-button-place');
  const reviewForm = document.getElementById('review-form');
  const modal = document.getElementById('loginModal');

  if (!token) {
    console.log("TOKEN IN CHECKOUT:", token)
    if (loginLink) loginLink.style.display = 'block';
    if (logOutButton) logOutButton.style.display = 'none';
    if (addReviewSection) addReviewSection.style.display = 'none';
    if (reviewForm) {
      alert("You should have an account to add a review");
      return; // Stop execution after redirect
    }
  } else {
    if (loginLink) loginLink.style.display = 'none';
    if (logOutButton) logOutButton.style.display = 'block';
    if (addReviewSection) addReviewSection.style.display = 'block';
    if (modal) {
      modal.style.display = 'none';
    }

    // Only try to fetch place details if we're on a place detail page
    let placeId = getPlaceIdFromURL();
    if (!placeId) {
      console.warn("No placeId found, skipping fetch.");
    } else if (window.location.pathname.includes("place.html")) {
      fetchPlaceDetails(token, placeId);
      fetchPlaceReviews(token, placeId);
    }
  }

  // Fetch places regardless of authentication status
  fetchPlaces();
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

// function to extract the place_id
function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  const placeId = urlParams.get('id');
  
  if (!placeId) {
    console.warn("Error: No place_id found in the URL");
  }
  
  return placeId;
}

// Get place details function
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
    // alert('Failed to retrieve place details: ' + error.message);
  }
}

// Get the Review with a place_id
async function fetchPlaceReviews(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
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

    // Verify if the response have an array of reviews
    if (!Array.isArray(data)) {
      console.warn('Unexpected response format:', data);
      return [];
    }

    // Call displayPlaceReviews to update UI
    displayPlaceReviews(data);

  } catch (error) {
    console.error('Error fetching place reviews:', error);
    return []; // Return an empty array if there is an error
  }
}

// Get Places
async function fetchPlaces() {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Places data:', data);
    displayPlaces(data);
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

// Fill the price filter
function populatePriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  
  if (!priceFilter) {
    console.warn("⚠️ No se encontró #price-filter en esta página. Omitiendo populatePriceFilter().");
    return;
  }

  const prices = ['All', '100.00', '200.00', '500.00'];

  prices.forEach(price => {
    const option = document.createElement('option');
    option.classList.add("filter_text")
    option.value = price;
    option.textContent = price === 'All' ? 'All' : `$${price}`;
    priceFilter.appendChild(option);
  });
}

// function to login user
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
    // Save token in cookies
    document.cookie = `token=${data.access_token}; path=/`;
    //Close modal
    const modal = document.getElementById('loginModal');
    if (modal) {
      modal.style.display = 'none';
    }
    window.location.href = 'index.html';
    return data;
  } else {
    alert('Login failed: ' + response.statusText);
  }
}


// Organize de place details in the HTML (without reviews)
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
}

// Obtains the place reviews and organize them in the HTML
function displayPlaceReviews(reviews) {
  const reviewsContainer = document.getElementById('review-list');
  reviewsContainer.replaceChildren();

  if (!reviewsContainer) {
    console.warn("⚠️ No se encontró #reviews en esta página. Omitiendo displayPlaceReviews.");
    return;
  }

  if (!reviews.length) {
    const noReviews = document.createElement("p");
    noReviews.textContent = "No reviews, be the first person to leave a review if you have visited this place";
    reviewsContainer.appendChild(noReviews);      
    return;
  }

  reviews.forEach(review => {

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

    reviewCard.appendChild(user);
    reviewCard.appendChild(rating);
    reviewCard.appendChild(reviewComment);
    reviewsContainer.appendChild(reviewCard);
  });
}

// Filter the places
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
// Display places in the Index.html
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');

  if (!placesList) {
    console.warn("⚠️ No se encontró #places-list en esta página. Omitiendo displayPlaces.");
    return;
  }

  placesList.innerHTML = '';

  places.forEach(place => {
    const placeCard = document.createElement('article');
    placeCard.className = 'place-card';

    placeCard.innerHTML = `
  
      <img src="https://picsum.photos/300/200?random=${place.id}" alt="${place.title}" class="imageCardIndex">
      <h3>${place.title}</h3>
      <div class="placeCardDetails">
        <p>Location: ${place.latitude}, ${place.longitude}</p>
        <p>Price: <strong>$${place.price}</strong></p>
      </div>
      <button class="details-button" data-place-id="${place.id}">View Details</button>
    `;

    // Add click handler for the details button
    const detailsButton = placeCard.querySelector('.details-button');
    detailsButton.addEventListener('click', () => {
      window.location.href = `place.html?id=${place.id}`;
    });

    placesList.appendChild(placeCard);
  });
}

// Add this new function to handle review submission
async function submitReview(reviewData, token) {

  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(reviewData)
    });

    let data;
    try {
      data = await response.json();  
    } catch {
      throw new Error("Unexpected response from server");
    }

    if (!response.ok) {
      if (data.error === 'You have already reviewed this place') {
        throw new Error('You have already submitted a review for this place');
      } else if (data.error === 'You cannot review your own place') {
        throw new Error('You cannot review your own place');
      } else {
        throw new Error(data.error || 'Failed to submit review');
      }
    }

    return data;
  } catch (error) {
    throw error;
  }
}

// Decode the JWT
function getUserIdFromToken(token){
  try{
    const decoded = jwt_decode(token);
    console.log("🔍 Token decodificado:", decoded);
    return decoded.sub || null;
  } catch (error) {
    console.error("❌ Error decoding token:", error);
    return null;
  }
} 
