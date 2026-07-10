document.addEventListener('DOMContentLoaded', function() {
    const savedScrollPosition = sessionStorage.getItem('billingPageScrollPosition');
    if (savedScrollPosition) {
        window.scrollTo(0, parseInt(savedScrollPosition));
        sessionStorage.removeItem('billingPageScrollPosition');
    }
});

function completeSale(){
    console.log(cart);
    cart=[];
    discountPercent=0;
    document.getElementById("discount-input").value=0;
    document.getElementById("customer-name").value="";
    document.getElementById("customer-phone").value="";
    renderCart();
    openSuccessToast(
        "Sale Completed Successfully"
    );
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