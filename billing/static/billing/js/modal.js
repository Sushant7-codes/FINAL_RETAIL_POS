let confirmCallback = null;

function openConfirmModal(title, message, callback) {
    document.getElementById("confirm-title").textContent = title;
    document.getElementById("confirm-message").textContent = message;
    confirmCallback = callback;
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