document.getElementById('barcode-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        alert('📷 Barcode scanned: ' + this.value);
        this.value = '';
    }
});
const scanButton = document.getElementById("scan-barcode-btn");
const cameraModal = document.getElementById("cameraModal");
const video = document.getElementById("camera-preview");
let stream = null;

function closeCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    cameraModal.close();
}
document.getElementById("barcode-input").addEventListener("input", function () {
    const barcode = this.value.trim();
    const cards = document.querySelectorAll(".grid .card");
    let found = false;
    cards.forEach(card => {
        const cardBarcode = card.dataset.barcode;
        if (barcode === "" || cardBarcode.includes(barcode)) {
            card.style.display = "block";
            found = true;
        } else {
            card.style.display = "none";
        }
    });
});
scanButton.addEventListener("click", async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: "environment"
            }
        });
        video.srcObject = stream;
        cameraModal.showModal();
    }
    catch (err) {
        alert("Unable to access camera.");
        console.error(err);
    }
});