let products = [];
let editingIndex = -1;

async function get_main_page() {
    window.location.href = "http://localhost:3000/";

}
async function get_seller_info() {
    try {
                const response = await fetch(`http://localhost:5000/Amazol/seller_info`, {
                    method: 'GET',
                    credentials:"include"
                });
                if (response.ok){                     
                    const seller_info = await response.json();

                    const seller_image = document.getElementById('profile-image')
                    const seller_name = document.getElementById('seller-name')
                    const seller_email_address = document.getElementById('email-text')
                    const seller_address = document.getElementById('address-text')
                    const seller_phone_number = document.getElementById('phone-text')

                    seller_image.src = seller_info.photo_url
                    seller_name.innerHTML = seller_info.name
                    seller_email_address.innerHTML = seller_info.email
                    seller_address.innerHTML = seller_info.address
                    seller_phone_number.innerHTML = seller_info.phone_number


                    
                }
                else{
                    const message = await response.json()

                    if (response.status == 401){
                        window.location.href = `http://localhost:3000/login?type=seller&next_page=/seller_profile`;
                    }
                    else{
                        alert(message['state'])
                    }
            
                }
        }
    catch(error){
        alert(error)
    }
}

async function get_proucts_info() {
    try {
                const response = await fetch(`http://localhost:5000/Amazol/seller_products_info`, {
                    method: 'GET',
                    credentials:"include"
                });
                if (response.ok){                     
                    const products_info = await response.json();
                    for (let product in products_info){
                        products.push(products_info[product])
                    }

                }
                else{
                    const message = await response.json()

                    if (response.status == 401){
                        window.location.href = `http://localhost:3000/login?type=seller&next_page=/seller_profile`;
                    }
                    else{
                        alert(message['state'])
                    }
            
                }
        }
    catch(error){
        alert(error)
    }
}
    

    

document.addEventListener('DOMContentLoaded', async () => {
    await get_seller_info()
    await get_proucts_info()
    document.getElementById('add-product-form').addEventListener('submit', addProduct);
    document.getElementById('edit-product-form').addEventListener('submit', await saveEdit);
    document.querySelector('.close').addEventListener('click', closeModal);
    window.addEventListener('click', (event) => {
        if (event.target == document.getElementById('edit-modal')) {
            closeModal();
        }
    });
    updateProductList();
    await setupEditableFields();
});

async function setupEditableFields() {
    const editableContainers = document.querySelectorAll('.editable-container');
    editableContainers.forEach(container => {
        const displaySection = container.querySelector('.display-section');
        const editSection = container.querySelector('.edit-section');
        const editButton = container.querySelector('.edit-button');
        const saveButton = container.querySelector('.save-button');
        const textElement = container.querySelector('.editable-text');
        const editableElement = container.querySelector('.editable-field');

        editButton.addEventListener('click', () => {
            displaySection.style.display = 'none';
            editableElement.innerHTML = textElement.innerHTML
            editSection.style.display = 'flex';
            editableElement.focus();
        });

        saveButton.addEventListener('click', async() => {
            const value = editableElement.innerText;
            const id = editableElement.id
            let key = ""
            textElement.innerText = value;
            displaySection.style.display = 'flex';
            editSection.style.display = 'none';

            if (id == "phone-editable"){
                key = "phone_number" 
            }
            else{
                key = "address"
            }
    
            data = {[key]: value}
            const response = await fetch(`http://localhost:5000/Amazol/new_seller_info`, {
                method: 'PUT',
                credentials:"include",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            const message = await response.json()
            alert(message['state'])
        });
    });
}
    

function addProduct(e) {
    e.preventDefault();
    const name = document.getElementById('product-name').value;
    const price = document.getElementById('product-price').value;
    const amount = document.getElementById('product-amount').value;
    const description = document.getElementById('product-description').value;
    const photo = document.getElementById('product-photo').files[0];

    if (name && price && amount && description && photo) {
        const reader = new FileReader();
        reader.onload = async function(e) {
            const photo_content = reader.result.replace('data:', '').replace(/^.+,/, '');

            const product = { 'name':name, 'price': price, 'amount': amount, 'description': description, 'photo': photo_content, 'photo_url': e.target.result};

            const response = await fetch(`http://localhost:5000/Amazol/new_product`, {
                method: 'POST',
                credentials:"include",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(product),
            });
            const message = await response.json()
            if (response.ok){
                product["id"] = message['product_id']
                products.push(product);
                updateProductList();
                document.getElementById('add-product-form').reset();
            }
            alert(message['state'])  

        };
        reader.readAsDataURL(photo);
    } else {
        alert('Please fill all fields and select a photo.');
    }
}

async function updateProductList() {
    const list = document.getElementById('product-list');
    const noProductsMessage = document.getElementById('no-products-message');
    if (products.length === 0) {
        list.innerHTML = '';
        noProductsMessage.classList.remove('hidden');
    } else {
        noProductsMessage.classList.add('hidden');
        list.innerHTML = '';
        products.forEach((product, index) => {
            const item = document.createElement('div');
            item.className = 'product-item';
            item.innerHTML = `
                <img src="${product.photo_url}" alt="${product.name}" style="width:100%; height:150px; object-fit:cover; border-radius:5px;">
                <h3>${product.name}</h3>
                <p>$${product.price} - ${product.amount} available</p>
                <div class="product-actions">
                    <button onclick="editProduct(${index})">Edit</button>
                    <button onclick="deleteProduct(${index})">Delete</button>
                </div>
            `;
            list.appendChild(item);
        });
    }
}

async function deleteProduct(index) {
    let product = {'product_id': products[index].id}
    const response = await fetch(`http://localhost:5000/Amazol/product_not_exist`, {
        method: 'DELETE',
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(product),
    });
    const message = await response.json()
    alert(message['state'])
    if (response.ok){
        products.splice(index, 1);
        await updateProductList();
    }

}

function editProduct(index) {
    editingIndex = index;
    const product = products[index];
    document.getElementById('edit-modal').style.display = 'block';
}

async function saveEdit(e) {
    e.preventDefault();
    const elements = document.querySelectorAll('.data_modification');

    let product = {};

    const readFile = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const photo_content = reader.result.replace('data:', '').replace(/^.+,/, '');
                products[editingIndex]['photo_url'] = e.target.result;
                resolve(photo_content)
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    };

    for (let i = 0; i < elements.length; i++) {
        if (elements[i].value != "") {
            if (elements[i].name == 'photo') {
                product['photo'] = await readFile(elements[i].files[0]);
            } else {
                product[elements[i].name] = elements[i].value;
                products[editingIndex][elements[i].name] = elements[i].value;
            }
        }
    }

    product['product_id'] = products[editingIndex].id;

    const response = await fetch(`http://localhost:5000/Amazol/new_product_info`, {
        method: 'PUT',
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(product),
    });

    if (response.ok) {
        await updateProductList();
        await closeModal();
        
    }
    else{
        const message = await response.json();
        alert(message['state']);
    }
}



async function closeModal() {
    document.getElementById('edit-modal').style.display = 'none';
}