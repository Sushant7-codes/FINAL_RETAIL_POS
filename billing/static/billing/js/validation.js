function validateCustomer() {

    const nameInput = document.getElementById("customer-name");
    const phoneInput = document.getElementById("customer-phone");

    const name = nameInput.value.trim();
    const phone = phoneInput.value.trim();

    // Remove previous error styles
    nameInput.classList.remove("input-error");
    phoneInput.classList.remove("input-error");

    // Name validation
    if (name.length < 2) {

        nameInput.classList.add("input-error");
        nameInput.focus();

        openConfirmModal(
            "Customer Required",
            "Please enter a valid customer name."
        );

        return false;
    }

    // Phone validation
    if (!/^\d{10}$/.test(phone)) {

        phoneInput.classList.add("input-error");
        phoneInput.focus();

        openConfirmModal(
            "Invalid Phone",
            "Phone number must contain exactly 10 digits."
        );

        return false;
    }

    // Cart validation
    if (cart.length === 0) {

        openConfirmModal(
            "Empty Cart",
            "Please add at least one product before checkout."
        );

        return false;
    }

    return true;
}

document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("customer-name")
        .addEventListener("input", function () {
            this.classList.remove("input-error");
        });
    
    document.getElementById("customer-phone")
        .addEventListener("input", function () {
            this.classList.remove("input-error");
        });

});