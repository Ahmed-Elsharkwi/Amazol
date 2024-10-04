        // Mock data for orders

        async function get_main_page() {
            window.location.href = "http://localhost:3000/";
        }

        async function renderOrders() {
            const ordersContainer = document.getElementById('orders-container');
            ordersContainer.innerHTML = '';

            try {
                const response = await fetch('http://localhost:5000/Amazol/orders_info',{
                    method: 'GET',
                    credentials: 'include'
                })
                const orders = await response.json()
                if (response.ok){
                    for(let order in orders){
                        const orderCard = document.createElement('div');
                        orderCard.className = 'order-card';

                        orderCard.innerHTML = `
                            <div class="order-header">
                                <div class="order-details">
                                    <div>Order Date: ${orders[order].order_date.slice(0, 16)}</div>
                                    <div>Total Price: $${orders[order].Total_price.toFixed(2)}</div>
                                    <div>Shipping Address: ${orders[order].billing_address}</div>
                                </div>
                                <div class='order_info'>
                                    <div class="order-id">Order ID: ${order} </div>
                                    <div class="payment_method">Payment method: ${orders[order].payment_method}</div>
                                </div>
                            </div>
                            <div class="order-content">
                                    <div class="product" data-product-id="${orders[order].product_id}">
                                        <div class="product-info">
                                            <img src="${orders[order].product_photo_url}" alt="${orders[order].product_name}" class="product-image" id="product_info" onclick="get_product_info('${orders[order].product_name}')">
                                            <p id="product_info" onclick="get_product_info('${orders[order].product_name}')">${orders[order].product_name}</p>
                                        </div>
                                        <button class="delete-btn" onclick="deleteProduct('${orders[order].product_id}')">Delete</button>
                                    </div>
                            </div>
                        `;

                            ordersContainer.appendChild(orderCard);

                    }
                }
                else{
                    if (response.status == 401){
                        window.location.href = 'http://localhost:3000/login?type=user&next_page=/orders_info'

                    }
                    
                    else{
                        alert(orders["state"])
                    }
        
                }
            } catch (error) {
                alert(error)
            }
        }

        async function deleteProduct(productId) {
            try {
                const response = await fetch('http://localhost:5000/Amazol/order_not_exist', {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({'product_id':productId}),

                })
                const message = await response.json()
                if (response.ok){
                    renderOrders();
                }
                alert(message["state"])
            } 
            catch (error) {
                alert(error)
            }
        }

    async function get_product_info(product_name) {
        window.location.href = `http://localhost:3000/product_info?product_name=${product_name}`

    }
        // Initial render
    document.addEventListener('DOMContentLoaded', async () => {
        await renderOrders();
    })