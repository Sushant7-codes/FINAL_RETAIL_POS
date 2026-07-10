document.addEventListener('keydown', function(e) {
    // Ctrl + S - Focus search
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        document.getElementById('search-input').focus();
    }
    // F2 - Focus barcode
    if (e.key === 'F2') {
        e.preventDefault();
        document.getElementById('barcode-input').focus();
    }
    // F9 - Checkout
    if (e.key === 'F9') {
        e.preventDefault();
        checkout();
    }
    // Escape - Clear cart
    if (e.key === 'Escape') {
        clearCart();
    }
});
