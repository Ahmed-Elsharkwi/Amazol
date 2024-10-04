async function get_main_page() {
    window.location.href = "http://localhost:3000/";

}

function renderCartItems() {
    const cartItemsContainer = document.getElementById("cart-items");
    cartItemsContainer.innerHTML = "";
    let total_price = 0
    const keys = Object.keys(localStorage)
    for (let key in keys){
        let item = JSON.parse(localStorage.getItem(keys[key]))
        const cartItemElement = document.createElement("div");

        cartItemElement.classList.add("cart-item");
        cartItemElement.innerHTML = `
            <div class="cart-item-info">
                <img src="${item.photo_url}" alt="${item.name}" class="click_me" onclick="get_product_info('${item.name}')">
                <div class="cart-item-details">
                    <h3 class="click_me" onclick="get_product_info('${item.name}')">${item.name}</h3>
                    <p>Price: $${item.price.toFixed(2)}</p>
                    <select class="quantity-select" data-id="${item.id}">
                        ${generateQuantityOptions(item.quantity, item.amount)}
                    </select>
                    <p>Quantity: <span class="quantity-value">${item.quantity}</span></p>
                </div>
            </div>
            <div class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</div>
            <button class="delete-btn" data-id="${item.id}">Delete</button>
        `;
        total_price += item.price * item.quantity
        cartItemsContainer.appendChild(cartItemElement);
    };

    updateTotalPrice(total_price);
    addEventListeners();
}

async function get_product_info(name) {
    window.location.href = `http://localhost:3000/product_info?product_name= ${name} `    
}

function generateQuantityOptions(currentQuantity, maxQuantity) {
    let options = '';
    for (let i = 1; i <= maxQuantity; i++) {
        options += `<option value="${i}" ${i === currentQuantity ? 'selected' : ''}>${i}</option>`;
    }
    return options;
}

function updateTotalPrice(total_price) {
    document.getElementById("total-price").textContent = total_price.toFixed(2);
}

function addEventListeners() {
    const quantitySelects = document.querySelectorAll(".quantity-select");
    const deleteButtons = document.querySelectorAll(".delete-btn");

    quantitySelects.forEach(select => {
        select.addEventListener("change", (e) => {
            const itemId = e.target.dataset.id;
            console.log(itemId)
            const newQuantity = parseInt(e.target.value);
            const item = JSON.parse(localStorage.getItem(itemId))
            if (newQuantity  > item.amount){
                alert(`the maximum limit is ${item.amount}`)
            }
            else{
                item.quantity = newQuantity;
                localStorage.setItem(itemId, JSON.stringify(item))
                e.target.nextElementSibling.querySelector(".quantity-value").textContent = newQuantity;
            }
            renderCartItems()
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            const itemId = e.target.dataset.id;
            console.log(localStorage.getItem(itemId))
            localStorage.removeItem(itemId)
            renderCartItems();
        });
    });
}

renderCartItems();