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

function openPaymentModal() {

    document.getElementById("payment-total").textContent =
        document.getElementById("grand-total").textContent;

    document.getElementById("cash-received").value = "";
    document.getElementById("change-amount").textContent = "Rs. 0";
    document.getElementById("paymentModal").showModal();
}

function closePaymentModal() {
    document.getElementById("paymentModal").close();
}

function changePaymentMethod() {

    const method =
        document.querySelector(
            'input[name="payment-method"]:checked'
        ).value;
    document
        .getElementById("cash-section")
        .classList.toggle(
            "hidden",
            method !== "cash"
        );
    document
        .getElementById("khalti-section")
        .classList.toggle(
            "hidden",
            method !== "khalti"
        );

}

function calculateChange() {

    const total =
        parseFloat(
            document
                .getElementById("grand-total")
                .textContent
                .replace("Rs.", "")
        );
    const received =
        parseFloat(
            document.getElementById("cash-received").value
        ) || 0;
    const change = received - total;
    document.getElementById("change-amount").textContent =
        "Rs. " + Math.max(change,0).toFixed(0);

}

function confirmPayment() {

    const method =
        document.querySelector(
            'input[name="payment-method"]:checked'
        ).value;

    if (method === "cash") {

        const total =
            parseFloat(
                document
                    .getElementById("grand-total")
                    .textContent
                    .replace("Rs.", "")
            );

        const received =
            parseFloat(
                document.getElementById("cash-received").value
            ) || 0;

        if (received < total) {

            openConfirmModal(
                "Payment Error",
                "Cash received is less than the bill amount."
            );

            return;

        }

        closePaymentModal();

        checkout();

        return;

    }

    // Khalti Payment
    if (method === "khalti") {

        closePaymentModal();

        initiateKhaltiPayment();

    }

}

async function initiateKhaltiPayment() {

    const payload = {

        customer_name: document.getElementById("customer-name").value,

        customer_phone: document.getElementById("customer-phone").value,

        discount_percent: discountPercent,

        cart: cart.map(item => ({
            price_id: item.id,
            quantity: item.quantity
        }))

    };

    const response = await fetch(
        "/sales/khalti/initiate/",
        {

            method: "POST",

            headers: {

                "Content-Type":"application/json",

                "X-CSRFToken":getCookie("csrftoken")

            },

            body:JSON.stringify(payload)

        }
    );

    const result = await response.json();
    
    if (!response.ok) {
    
        openConfirmModal(
            "Payment Error",
            result.detail || "Unable to initiate Khalti payment."
        );
    
        return;
    
    }
    
    window.location.href = result.payment_url;
}