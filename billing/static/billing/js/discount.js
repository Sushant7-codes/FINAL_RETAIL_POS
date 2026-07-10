let discountPercent = 0;
    
function updateTotals() {
    let subtotal = 0;
    cart.forEach(item => {
        subtotal += item.price * item.quantity;
    });
    const discountAmount = subtotal * discountPercent / 100;
    const tax = 0;
    const total = subtotal - discountAmount + tax;
    document.getElementById("subtotal").textContent =
        `Rs. ${subtotal.toFixed(0)}`;
    document.getElementById("discount").textContent =
        `Rs. ${discountAmount.toFixed(0)}`;
    document.getElementById("grand-total").textContent =
        `Rs. ${total.toFixed(0)}`;
}
function changeDiscount(change) {
    discountPercent += change;
    if (discountPercent < 0)
        discountPercent = 0;
    if (discountPercent > 100)
        discountPercent = 100;
    document.getElementById("discount-input").value = discountPercent;
    updateTotals();
}
function setDiscount(value) {
    discountPercent = Number(value);
    if (isNaN(discountPercent))
        discountPercent = 0;
    if (discountPercent < 0)
        discountPercent = 0;
    if (discountPercent > 100)
        discountPercent = 100;
    document.getElementById("discount-input").value = discountPercent;
    updateTotals();
}