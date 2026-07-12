let confirmCallback = null;

function openConfirmModal(title, message, callback = null) {
    document.getElementById("confirm-title").textContent = title;
    document.getElementById("confirm-message").innerHTML = message;
    confirmCallback = callback;
    const confirmBtn = document.getElementById("confirm-btn");
    
    const cancelBtn = document.querySelector(
        "#confirmModal .modal-action button"
    );
    
    if (callback) {
    
        confirmBtn.style.display = "";
        confirmBtn.textContent = "Confirm";
        cancelBtn.textContent = "Cancel";
    } else {
        confirmBtn.style.display = "none";
        cancelBtn.textContent = "Close";
    }
    
    document.getElementById("confirmModal").showModal();
}


function closeConfirmModal() {
    document.getElementById("confirmModal").close();
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("confirm-btn").onclick = function () {
        if (confirmCallback) confirmCallback();
        closeConfirmModal();
    };
});