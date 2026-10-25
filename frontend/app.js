const RESTAURANT_API = "";
const ORDER_API = "";
const menus = {
  1: {
    image: "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=1000&q=85",
    items: [
      { name: "Paneer Tikka Bowl", description: "Smoky paneer, rice & fresh herbs", price: 260 },
      { name: "Dal Makhani & Rice", description: "Slow-cooked comfort food", price: 240 },
      { name: "Masala Chai", description: "A warming cup of tea", price: 80 }
    ]
  },
  2: {
    image: "https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=1000&q=85",
    items: [
      { name: "Margherita Pizza", description: "Tomato, mozzarella & basil", price: 320 },
      { name: "Roasted Veg Pizza", description: "Seasonal vegetables & herbs", price: 380 },
      { name: "Garlic Bread", description: "Toasted, buttery & crisp", price: 150 }
    ]
  }
};

let cart = [];
let restaurants = [];

const restaurantList = document.getElementById("restaurant-list");
const cartPanel = document.getElementById("cart-panel");
const cartItems = document.getElementById("cart-items");
const cartCount = document.getElementById("cart-count");
const cartTotal = document.getElementById("cart-total");
const orderMessage = document.getElementById("order-message");


function renderRestaurants() {
  if (!restaurants.length) {
    restaurantList.innerHTML =
      "<p>No restaurants are available right now.</p>";
    return;
  }

  restaurantList.innerHTML = restaurants.map((restaurant) => {
    const menu = menus[restaurant.id];

    if (!menu) {
      return `
        <article class="restaurant-card">
          <div class="restaurant-content">
            <h3>${restaurant.name}</h3>
            <p>${restaurant.cuisine}</p>
          </div>
        </article>
      `;
    }

    return `
      <article class="restaurant-card">
        <img
          class="restaurant-image"
          src="${menu.image}"
          alt="${restaurant.name} food"
          loading="lazy"
        >

        <div class="restaurant-content">
          <div class="restaurant-topline">
            <h3>${restaurant.name}</h3>
            <span class="open-label">
              ${restaurant.available ? "● Available" : "Currently unavailable"}
            </span>
          </div>

          <p class="cuisine-label">${restaurant.cuisine} cuisine</p>

          <div class="menu-list">
            ${menu.items.map((item, index) => {
              const cartItem = cart.find(
                (entry) =>
                  entry.restaurantId === restaurant.id &&
                  entry.name === item.name
              );

              const quantity = cartItem ? cartItem.quantity : 0;

              return `
                <div class="menu-item">
                  <div>
                    <h4>${item.name}</h4>
                    <p>${item.description}</p>
                    <p>₹${item.price}</p>
                  </div>

                  ${
                    quantity === 0
                      ? `
                        <button
                          class="add-button"
                          data-action="add"
                          data-restaurant-id="${restaurant.id}"
                          data-item-index="${index}"
                          ${!restaurant.available ? "disabled" : ""}
                        >Add +</button>
                      `
                      : `
                        <div class="quantity-control">
                          <button
                            class="quantity-button"
                            data-action="decrease"
                            data-restaurant-id="${restaurant.id}"
                            data-item-index="${index}"
                            aria-label="Decrease ${item.name} quantity"
                          >−</button>

                          <span class="quantity-value">${quantity}</span>

                          <button
                            class="quantity-button"
                            data-action="increase"
                            data-restaurant-id="${restaurant.id}"
                            data-item-index="${index}"
                            aria-label="Increase ${item.name} quantity"
                          >+</button>
                        </div>
                      `
                  }
                </div>
              `;
            }).join("")}
          </div>
        </div>
      </article>
    `;
  }).join("");

  document.querySelectorAll("[data-action]").forEach((button) => {
    button.addEventListener("click", () => {
      const restaurantId = Number(button.dataset.restaurantId);
      const itemIndex = Number(button.dataset.itemIndex);
      const action = button.dataset.action;

      if (action === "add" || action === "increase") {
        addToCart(restaurantId, itemIndex);
      } else if (action === "decrease") {
        decreaseQuantity(restaurantId, itemIndex);
      }
    });
  });
}


function addToCart(restaurantId, itemIndex) {
  if (cart.length && cart[0].restaurantId !== restaurantId) {
    alert("Your bag contains food from another restaurant. Place that order first, or remove those items.");
    return;
  }

  const menu = menus[restaurantId];
  const item = menu.items[itemIndex];
  const existing = cart.find((entry) => entry.name === item.name);

  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({
      ...item,
      restaurantId,
      quantity: 1
    });
  }

  orderMessage.textContent = "";
  renderCart();
  renderRestaurants();
}


function decreaseQuantity(restaurantId, itemIndex) {
  const item = menus[restaurantId].items[itemIndex];

  const cartItem = cart.find(
    (entry) =>
      entry.restaurantId === restaurantId &&
      entry.name === item.name
  );

  if (!cartItem) return;

  cartItem.quantity -= 1;

  if (cartItem.quantity <= 0) {
    cart = cart.filter((entry) => entry !== cartItem);
  }

  renderCart();
  renderRestaurants();
}


function renderCart() {
  const count = cart.reduce((sum, item) => sum + item.quantity, 0);
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  cartCount.textContent = count;
  cartTotal.textContent = `Total: ₹${total}`;

  if (!cart.length) {
    cartItems.innerHTML = "<p>Your bag is empty. Let's fix that.</p>";
  } else {
    cartItems.innerHTML = cart.map((item, index) => `
      <div class="cart-line">
        <div>
          <p>${item.name} × ${item.quantity}</p>
          <small>₹${item.price * item.quantity}</small>
        </div>
        <button class="remove-button" data-index="${index}" aria-label="Remove ${item.name}">×</button>
      </div>
    `).join("");
  }

  cartItems.querySelectorAll(".remove-button").forEach((button) => {
    button.addEventListener("click", () => {
      cart.splice(Number(button.dataset.index), 1);
      renderCart();
    });
  });
}

document.getElementById("cart-toggle").addEventListener("click", () => {
  cartPanel.hidden = !cartPanel.hidden;
});

document.getElementById("cart-close").addEventListener("click", () => {
  cartPanel.hidden = true;
});

document.getElementById("theme-toggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
  localStorage.setItem(
    "gather-theme",
    document.body.classList.contains("dark") ? "dark" : "light"
  );
});

if (localStorage.getItem("gather-theme") === "dark") {
  document.body.classList.add("dark");
}

document.getElementById("place-order").addEventListener("click", async () => {
  if (!cart.length) {
    orderMessage.textContent = "Add something delicious to your bag first.";
    return;
  }

  const button = document.getElementById("place-order");
  button.disabled = true;
  button.textContent = "Placing order...";
  orderMessage.textContent = "";

  const restaurantId = cart[0].restaurantId;
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const itemSummary = cart
    .map((item) => `${item.name} x${item.quantity}`)
    .join(", ");

  try {
    const response = await fetch(`${ORDER_API}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        restaurant_id: restaurantId,
        customer: "Guest",
        item: itemSummary,
        price: total
      })
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.detail || "The order could not be placed.");
    }

    orderMessage.textContent =
      `Order #${result.id} placed! Delivery status: ${result.delivery?.status || "Pending"}.`;

    cart = [];
    renderCart();
  } catch (error) {
    orderMessage.textContent =
      `Couldn't place the order: ${error.message}. Check that the services are running.`;
  } finally {
    button.disabled = false;
    button.textContent = "Place your order";
  }
});

async function loadRestaurants() {
  try {
    const response = await fetch(`${RESTAURANT_API}/restaurants`);

    if (!response.ok) {
      throw new Error("Restaurant service returned an error.");
    }

    restaurants = await response.json();
    renderRestaurants();
  } catch (error) {
    restaurantList.innerHTML = `
      <p>We couldn't reach the restaurant service.
      Make sure Docker Compose is running, then refresh this page.</p>
    `;
    console.error(error);
  }
}

renderCart();
loadRestaurants();

async function loadOrders() {
  const ordersList = document.getElementById("orders-list");
  const refreshButton = document.getElementById("refresh-orders");

  ordersList.innerHTML =
    '<p class="loading-message">Loading your orders...</p>';

  try {
    const response = await fetch(`${ORDER_API}/orders`);

    if (!response.ok) {
      throw new Error("Could not fetch orders.");
    }

    const orders = await response.json();

    if (orders.length === 0) {
      ordersList.innerHTML = `
        <p class="loading-message">
          No orders yet. Find something delicious on the menu!
        </p>
      `;
      return;
    }

    
    ordersList.innerHTML = orders.slice().reverse().map((order) => {
    const deliveryStatus = order.delivery?.status || "Pending";
    const currentStatus = deliveryStatus.toLowerCase();

    const statusSteps = [
        "Placed",
        "Preparing",
        "Out for Delivery",
        "Delivered"
    ];

    const currentStep = currentStatus.includes("delivered")
        ? 3
        : currentStatus.includes("out for delivery")
        ? 2
        : currentStatus.includes("preparing")
            ? 1
            : 0;

    return `
        <article class="order-card" data-order-id="${order.id}">
        <div class="order-card-heading">
            <div>
            <p class="eyebrow">ORDER #${order.id}</p>
            <h3>${order.item}</h3>
            </div>
            <span class="order-status">${order.status}</span>
        </div>

        <p class="order-detail">Restaurant ID: ${order.restaurant_id}</p>
        <p class="order-detail">Customer: ${order.customer}</p>
        <p class="order-detail">Delivery status: <span class="delivery-status-text">${deliveryStatus}</span></p>

        <div class="delivery-progress" data-progress>
            ${statusSteps.map((step, index) => `
            <div class="progress-step ${index <= currentStep ? "completed" : ""}">
                <span class="progress-dot">${index < currentStep ? "✓" : index + 1}</span>
                <span class="progress-label">${step}</span>
            </div>
            `).join("")}
        </div>
        </article>
    `;
    }).join("");


  } catch (error) {
    ordersList.innerHTML = `
      <p class="loading-message">
        Couldn't load orders. Check that Docker is running and try again.
      </p>
    `;
    console.error("Order loading error:", error);
  } finally {
    refreshButton.disabled = false;
  }
}

document.getElementById("refresh-orders")
  .addEventListener("click", loadOrders);

loadOrders();

setInterval(refreshOrderStatuses, 5000);

async function refreshOrderStatuses() {
  try {
    const response = await fetch(`${ORDER_API}/orders`);

    if (!response.ok) return;

    const orders = await response.json();

    orders.forEach((order) => {
      const card = document.querySelector(
        `.order-card[data-order-id="${order.id}"]`
      );

      if (!card) return;

      const deliveryStatus = order.delivery?.status || "Pending";
      const statusText = card.querySelector(".delivery-status-text");
      const progress = card.querySelector("[data-progress]");

      const statusSteps = [
        "Placed",
        "Preparing",
        "Out for Delivery",
        "Delivered"
      ];

      const normalizedStatus = deliveryStatus.toLowerCase();

      const currentStep = normalizedStatus.includes("delivered")
        ? 3
        : normalizedStatus.includes("out for delivery")
          ? 2
          : normalizedStatus.includes("preparing")
            ? 1
            : 0;

      // Update the status text only if it changed.
      if (statusText && statusText.textContent !== deliveryStatus) {
        statusText.textContent = deliveryStatus;
      }

      // Update the progress markers without rebuilding the order card.
      if (progress) {
        progress.querySelectorAll(".progress-step").forEach((step, index) => {
          step.classList.toggle("completed", index <= currentStep);

          const dot = step.querySelector(".progress-dot");
          if (dot) {
            dot.textContent = index < currentStep ? "✓" : index + 1;
          }
        });
      }
    });
  } catch (error) {
    console.error("Status refresh failed:", error);
  }
}
