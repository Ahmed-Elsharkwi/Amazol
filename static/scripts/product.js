const closePopupBtn = document.getElementById('closePopup');
        const popup = document.getElementById('popup');
        const overlay = document.getElementById('overlay');

        async function place_order_fun(data) {
            const response = await fetch(`http://localhost:5000/Amazol/new_order`, {
                method: 'POST',
                credentials:"include",

                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            const message = await response.json()
            alert(message['state'])
            
        }

        async function Buy_product(amount, product) {
            try {
                const response = await fetch(`http://localhost:5000/Amazol/payment_info`, {
                    method: 'GET',
                    credentials:"include"
                });
                if (response.ok){                     
                    const payment_methods = await response.json();
                    popup.innerHTML=''
                    let data = {}
                    let place_order = null

                    for (const payment_method in payment_methods) {
                        const new_payment_method = document.createElement("div");
                        new_payment_method.className = 'payment_method';
                        
                        new_payment_method.onclick = function() {
                            // Reset the background color of all payment_method divs
                            const allPaymentMethods = document.querySelectorAll('.payment_method');
                            allPaymentMethods.forEach(method => {
                                method.style.backgroundColor = ''; // Reset to default
                            });

                            // Set the background color of the clicked div
                            this.style.backgroundColor = 'lightblue';
                            data["payment_type"] = payment_methods[payment_method].number;

                            if (place_order)
                            {
                                popup.removeChild(place_order)
                            }
                            data["product_id"] = product.id
                            data["amount"] = amount
                            place_order = document.createElement('button')
                            place_order.className = "buttons"
                            place_order.id = "place_order"
                            place_order.innerHTML = `Place Order`
                            place_order.onclick = function(){
                                place_order_fun(data)
                            
                            };
                            popup.appendChild(place_order)

                    }

                        new_payment_method.innerHTML = `
                            <p class='method_name'> ${payment_methods[payment_method].number} </p>
                            <p class='holder_name'> ${payment_methods[payment_method].holder_name} </p>
                            <p class='expiry_date'> ${payment_methods[payment_method].expiry_date} </p>
                        `;
                        new_payment_method.style.marginBottom = '10px';
                        
                        popup.appendChild(new_payment_method);
                    }
                    total_amount_price = amount * product.price
                    let total_price = document.createElement('div')
                    total_price.className = 'payment_method'
                    total_price.id = "total_price"
                    total_price.innerHTML = `Total price: ${total_amount_price}`
                    popup.appendChild(total_price)
                    let place_order_div = document.createElement('div')
                    
                    popup.appendChild(place_order_div)


                }
                else{
                    const message = await response.json()

                    if (response.status == 401){
                        window.location.href = `http://localhost:3000/login?type=user&next_page=/product_info?product_name= ${product.name}`;
                        return null
                    }
                    else{
                        alert(message['state'])
                        return null
                    }
            
                }
                popup.style.display = 'block';
                overlay.style.display = 'block';
            }
            catch (error){
                alert(error)
            }
        }

        closePopupBtn.addEventListener('click', () => {
            popup.style.display = 'none';
            overlay.style.display = 'none';
        });

        overlay.addEventListener('click', () => {
            popup.style.display = 'none';
            overlay.style.display = 'none';
        });

        async function list_nums(quantitySelect, maxQuantity){
            for (let i = 1; i <= maxQuantity; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            quantitySelect.appendChild(option);
            }
        }
        async function get_product_info(product_name) {
            try {
                const response = await fetch(`http://localhost:5000/Amazol/product_info?name=${product_name} `, {
                    method: 'GET',
                });
                if (response.ok){                     
                    let product_info = document.getElementById("product_info")
                    let product_details = document.getElementById("product_details")
                    const product = await response.json();
                    product_details.innerHTML = `
                        <h1 class="product-title">${ product.name }</h1>
                        <p class="product-price">$${product.price}</p>
                        <p class="product-description">
                            ${product.description}
                        </p>

                    `
                    product_info.innerHTML = `
                        <img src="${product.photo_url}" alt="Product Image" class="product-image">
                    `
                    

                    if (product.amount != 0) {
                        let product_amount = document.createElement('div');
                        product_amount.className = 'product_amount';

                        let amount_label = document.createElement('label');
                        amount_label.innerHTML = `Quantity:`;

                        let query_select = document.createElement('select');
                        await list_nums(query_select, product.amount);

                        product_amount.appendChild(amount_label);
                        product_amount.appendChild(query_select);
                        product_details.appendChild(product_amount);

                        const button = document.createElement("button");
                        button.className = "buttons";
                        button.innerHTML = "Add to Cart";
                        button.onclick = function() {
                            addToCart(product);
                        };
                        product_details.appendChild(button);

                        const buy_button = document.createElement("button");
                        buy_button.className = "buttons";
                        buy_button.innerHTML = "Buy";
                        buy_button.id = "buy_button";
                        buy_button.onclick = function() {
                            Buy_product(query_select.value, product);
                        };
                        product_details.appendChild(buy_button);
                    } else {
                        const message = document.createElement("h2");
                        message.innerHTML = "The product is not available";
                        product_details.appendChild(message);
                    }

                    product_info.appendChild(product_details);
                }

                else {
                    let message = await response.json()
                    alert(message['state'])
                }
            }
            catch (error) {
                alert(error)
            }
        }
async function get_cart() {
    window.location.href = "http://localhost:3000/cart"
}
        