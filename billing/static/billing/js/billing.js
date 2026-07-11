document.addEventListener('DOMContentLoaded', function() {
    const savedScrollPosition = sessionStorage.getItem('billingPageScrollPosition');
    if (savedScrollPosition) {
        window.scrollTo(0, parseInt(savedScrollPosition));
        sessionStorage.removeItem('billingPageScrollPosition');
    }
});

async function completeSale() {

    const payload = {

        customer_name: document.getElementById("customer-name").value,
        customer_phone: document.getElementById("customer-phone").value,
        discount_percent: discountPercent,
        cart: cart.map(item => ({
            price_id: item.id,
            quantity: item.quantity
        }))
    };

    const response = await fetch("/sales/checkout/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(payload)
    });
    const result = await response.json();

    if (!result.success) {
        alert(result.message);
        return;
    }


    cart.forEach(item => {
        const card = document.querySelector(`.card[data-id="${item.id}"]`);     
        if (!card) return;      
        const currentStock = Number(card.dataset.stock);        
        const newStock = currentStock - item.quantity;      
        // Update the card's "real" stock
        card.dataset.stock = newStock;      
        // Update the visible stock
        card.querySelector(".stock-count").textContent = newStock;
    });
    
    cart = [];
    discountPercent = 0;
    document.getElementById("discount-input").value = 0;
    document.getElementById("customer-name").value = "";
    document.getElementById("customer-phone").value = "";
    renderCart();

    openSuccessToast(
        `Invoice ${result.invoice} completed successfully!`
    );

    console.log(result);
}

function openSuccessToast(message){
    const toast = document.createElement("div");
    toast.className =
        "alert alert-success shadow-lg";
    toast.innerHTML = `
        <span>${message}</span>
    `;
    document
        .getElementById("toast-container")
        .appendChild(toast);
    setTimeout(()=>{
        toast.remove();
    },3000);
}

function getCookie(name) {

    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}