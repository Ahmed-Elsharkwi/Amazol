async function get_main_page() {
    window.location.href = "http://localhost:3000/";

}
async function get_user_info() {
    try{
            const response_1 = await fetch('http://localhost:5000/Amazol/user_info', {
                method: 'GET',
                credentials: 'include'
            });
            const data = await response_1.json()
            if (response_1.ok){

                const user_image = document.getElementById('profile-image')
                const user_name = document.getElementById('seller-name')
                const user_email_address = document.getElementById('email-text')
                const user_address = document.getElementById('address-text')
                const user_phone_number = document.getElementById('phone-text')

                user_image.src = data.photo_url
                user_name.innerHTML = data.name
                user_email_address.innerHTML = data.email
                user_address.innerHTML = data.address
                user_phone_number.innerHTML = data.phone_number


            }
            else{
                if (response_1.status == 401){
                    window.location.href = 'http://localhost:3000/login?type=user&next_page=/user_profile'
                    return null
                }
                else{
                    console.log(data['state'])
                }
            }

        }
        catch (error){
            alert(error)
        }
    }
async function setupEditableFields() {
const editableContainers = document.querySelectorAll('.editable-container');
editableContainers.forEach(container => {
    const displaySection = container.querySelector('.display-section');
    const editSection = container.querySelector('.edit-section');
    const editButton = container.querySelector('.edit-button');
    const saveButton = container.querySelector('.save-button');
    const textElement = container.querySelector('.editable-text');
    const editableElement = container.querySelector('.editable-field');
    editSection.style.display = 'none';

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

        let data = {[key]: value}
        const response = await fetch(`http://localhost:5000/Amazol/new_user_info`, {
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
  document.addEventListener('DOMContentLoaded', async () => {
    let cards = [];
    let currentCardIndex = -1;
    await get_user_info()
    await setupEditableFields()
    const creditCardForm = document.getElementById('credit-card-form');
    const savedCardsList = document.getElementById('saved-cards');
    const cardExpiryMonth = document.getElementById('card-expiry-month');
    const cardExpiryYear = document.getElementById('card-expiry-year');
    const modifyModal = document.getElementById('modify-modal');
    const modifyCardForm = document.getElementById('modify-card-form');
    const modifyCardExpiryMonth = document.getElementById('modify-card-expiry-month');
    const modifyCardExpiryYear = document.getElementById('modify-card-expiry-year');
    const closeModal = document.getElementsByClassName('close')[0];
    

    try{
            const response = await fetch('http://localhost:5000/Amazol/payment_info', {
                method: 'GET',
                credentials: 'include'
            });
            const data = await response.json()
            if (response.ok){
                for (payment_method in data){
                    cards.push(data[payment_method])
                }
                updateCardList()
            }

            else{
                if (response.status != 401){
                    alert(data['state'])
                }
            }
        
        }
        catch(error){
            alert(error)
    }
// Populate month selects
[cardExpiryMonth, modifyCardExpiryMonth].forEach(select => {
    for (let i = 1; i <= 12; i++) {
        const option = document.createElement('option');
        option.value = i.toString().padStart(2, '0');
        option.textContent = i.toString().padStart(2, '0');
        select.appendChild(option);
    }
});

// Populate year selects
const currentYear = new Date().getFullYear();
[cardExpiryYear, modifyCardExpiryYear].forEach(select => {
    for (let i = currentYear; i <= currentYear + 10; i++) {
        const option = document.createElement('option');
        option.value = i.toString();
        option.textContent = i.toString();
        select.appendChild(option);
    }
});

// Input validation
document.getElementById('card-number').addEventListener('input', function(e) {
    this.value = this.value.replace(/\D/g, '').slice(0, 19);
});

document.getElementById('card-holder').addEventListener('input', function(e) {
    this.value = this.value.replace(/[^a-zA-Z\s]/g, '');
});

document.getElementById('card-cvv').addEventListener('input', function(e) {
    this.value = this.value.replace(/\D/g, '').slice(0, 4);
});

creditCardForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const number = document.getElementById('card-number').value;
    const holder_name = document.getElementById('card-holder').value;
    const cardExpiryMonth = document.getElementById('card-expiry-month').value;
    const cardExpiryYear = document.getElementById('card-expiry-year').value;
    const cardCvv = document.getElementById('card-cvv').value;

    if (number.length < 14) {
        alert('Card number must be at least 14 digits long');
        return;
    }
    const card_info = {
        'number': number, 
        'holder_name': holder_name, 
        'cvv': cardCvv, 
        'month': cardExpiryMonth, 
        'year': cardExpiryYear
    }
    try {
        const response = await fetch('http://localhost:5000/Amazol/new_payment_method',{
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(card_info),

        })
        message = await response.json()
        if (response.ok){
            const newCard = { 
                number, 
                holder_name, 
                expiry_date: `${cardExpiryMonth}/${cardExpiryYear}`,
                "id": message['id'],
            };
            cards.push(newCard);
            updateCardList();
            creditCardForm.reset();
        }
        else{
            alert(message['state'])
        }

    }
    catch (error){
        alert(error)
    }
});

function updateCardList() {
    savedCardsList.innerHTML = '';
    cards.forEach((card, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>
                ${card.number.slice(-4).padStart(16, '*')} | 
                ${card.holder_name} | 
                Expires: ${card.expiry_date}
            </span>
            <div>
                <button class="modify-btn" data-index="${index}">Modify</button>
                <button class="delete-btn" data-index="${index}">Delete</button>
            </div>
        `;
        savedCardsList.appendChild(li);
    });

    // Add event listeners for modify and delete buttons
    document.querySelectorAll('.modify-btn').forEach(btn => {
        btn.addEventListener('click', openModifyModal);
    });
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', deleteCard);
    });
}

function openModifyModal(e) {
    currentCardIndex = e.target.getAttribute('data-index');
    const card = cards[currentCardIndex];
    document.getElementById('modify-card-holder').value = card.holder_name;
    const [month, year] = card.expiry_date.split('/');
    document.getElementById('modify-card-expiry-month').value = month;
    document.getElementById('modify-card-expiry-year').value = `${year}`;
    modifyModal.style.display = 'block';
}

closeModal.onclick = function() {
    modifyModal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modifyModal) {
        modifyModal.style.display = 'none';
    }
}

modifyCardForm.addEventListener('submit', async(e) => {
    e.preventDefault();
    const holder_name = document.getElementById('modify-card-holder').value;
    const cardExpiryMonth = document.getElementById('modify-card-expiry-month').value;
    const cardExpiryYear = document.getElementById('modify-card-expiry-year').value;
    cards[currentCardIndex] = {
        'holder_name': holder_name,
        'month': cardExpiryMonth,
        'year': cardExpiryYear,
        'expiry_date': `${cardExpiryMonth}/${cardExpiryYear}`,
        'id': cards[currentCardIndex].id,
        'number': cards[currentCardIndex].number
    };

    try {
        const response = await fetch('http://localhost:5000/Amazol/new_payment_info', {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cards[currentCardIndex]),

        })
        const message = await response.json()
        if (response.ok){
            updateCardList();
            modifyModal.style.display = 'none';
        }
        alert(message["state"])
    } catch (error) {
        alert(error)
    }
});

async function deleteCard(e) {
    const index = e.target.getAttribute('data-index');
    try {
        const response = await fetch('http://localhost:5000/Amazol/payment_not_exist', {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'id':cards[index].id}),

        })
        const message = await response.json()
        if (response.ok){
            cards.splice(index, 1);
            updateCardList();
        }
        alert(message["state"])
    } catch (error) {
        alert(error)
    }
}


document.getElementById('modify-card-holder').addEventListener('input', function(e) {
    this.value = this.value.replace(/[^a-zA-Z\s]/g, '');
});
});