let cartItems = 0;

function get_user_orders(){
    alert("orders are here")
}
function updateCartCount() {
    document.getElementById('cartCount').textContent = cartItems;
}

function addToCart(product_info) {

    let product = JSON.parse(localStorage.getItem(product_info.id));
    if (product == null) {
        product_info['quantity'] = 1
        localStorage.setItem(product_info.id, JSON.stringify(product_info))
    }
    else {
        if (product.quantity + 1 > product.amount) {
            alert("The limit is exceeded")
            return null
        }
        else {
            product.quantity = product.quantity + 1
            localStorage.setItem(product.id, JSON.stringify(product))
        }
    }
    cartItems++;
    updateCartCount();
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.id = product.id;
    card.innerHTML = `
        <img src="${product.photo_url}" alt="${product.name}" class="product-image" id="click_me" onclick="get_product_info('${product.name}')">
        <div class="product-info">
            <h2 class="product-title" id="click_me" onclick="get_product_info('${product.name}')">${product.name}</h2>
            <p class="product-price" id="click_me" onclick="get_product_info('${product.name}')">${product.price}</p>
            <button class="btn btn-primary add-to-cart" onclick='addToCart(${JSON.stringify(product)})'>Add to Cart</button>
        </div>
    `;
    return card;
}

function get_cart_items(){
    let counter = 0
    for (key in localStorage) {
        product = JSON.parse(localStorage.getItem(key))
        if (product != null) {
            counter += product.quantity
        } 
    }
    if (counter != cartItems){
        cartItems = counter
        updateCartCount()
    }
}
async function renderProducts(page_number) {
    const productGrid = document.getElementById('productGrid');
    const word = document.getElementById('searchInput').value
    
    get_cart_items()
    if (word == '') {
        try {
            const response = await fetch(`http://localhost:5000/products_data/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            });
            if (response.ok){
                const data = await response.json();

                for (const product in data) {
                        productGrid.appendChild(createProductCard(data[product]));

                    }
            }

        } 
        catch (error) {
            alert(error)
        }
    }
else {
    pages = document.getElementById('pages_number')

    let send_data = {}
    if (page_number != null && pages != null) {
        send_data['page'] = page_number
        send_data['pages'] = pages.textContent
        productGrid.innerHTML = ''
        container_2 = document.getElementById('container_2')
        container_2.innerHTML = ''
    }
    try {
            const response = await fetch(`http://localhost:5000/products_data/${word}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(send_data),
            });
            if (response.ok){                      
                const data = await response.json();

                for (const product in data) {
                        if (product != 'page' && product != 'pages'){
                            productGrid.appendChild(createProductCard(data[product]));
                        }
                    }
                    if (data['pages'] != undefined) {
                        let div_buttons = document.createElement('div');
                        div_buttons.className = 'pages'
                        let botton_id = ''

                        for (let page_number = 1; page_number <= data['pages']; page_number++) {
                            // Create a button for each page number
                            let div_buttons = document.createElement('div');
                            div_buttons.className = 'pages_buttons'

                            if (page_number == data['pages']) {
                                button_id = 'pages_number'
                            }
                            else {
                                button_id = 'page_number'
                            }

                            div_buttons.innerHTML = `
                                <button class='page_button' id=${button_id} onclick='renderProducts(${page_number})'>${page_number}</button>
                            `
                            container_2.appendChild(div_buttons);

                        }

                        // Append the rectangle div to the body or any other container
                    }

            }
            else {
                message = await response.json()
                alert(message)
            }

        } 
        catch (error) {
            alert(error)
        }

}
}

function search() {
    let search_query = document.getElementById('searchInput').value
    if (search_query != ''){
        window.location.href = `http://localhost:3000?search_query=${search_query}`;
    }
    else {
        get_main_page()
    }
}

async function get_main_page() {
    window.location.href = "http://localhost:3000/";

}
function sign_in_user() {
    window.location.href = "http://localhost:3000/login?type=user&next_page=/";
}

function get_user_info(name) {
    alert(`welcome mr ${name}`)
    //window.location.href = "http://localhost:3000/user_info";
}



function get_seller_info() {
    window.location.href = "http://localhost:3000/seller_profile";

}

function get_product_info(product_name) {
    window.location.href = `http://localhost:3000/product_info?product_name=${product_name}`
}

document.addEventListener('DOMContentLoaded', async () => {
    get_cart_items()
});
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        search();
    }
});