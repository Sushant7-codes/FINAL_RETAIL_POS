let cart = [];

function addToCart(id, name, price, stock) {
    const existingItem = cart.find(item => item.id === id);
    if (existingItem) {
        if (existingItem.quantity >= stock) {
            return;
        }
        existingItem.quantity++;
    } else {
        cart.push({
            id: id,
            name: name,
            price: Number(price),
            stock: stock,
            quantity: 1
        });
    }
    renderCart(); 
}

function renderCart() {
    const cartContainer = document.getElementById("cart-items");
    // Empty cart
    cartContainer.innerHTML = "";
if (cart.length === 0) {
    cartContainer.innerHTML = `
        <div
            id="empty-cart"
            class="h-full flex flex-col items-center justify-center text-center"
        >
            <div class="text-6xl mb-4">
                🛒
            </div>
            <h3 class="text-xl font-bold">
                Cart is Empty
            </h3>
            <p class="text-base-content/60 mt-2">
                Scan products or search items to begin billing.
            </p>
        </div>
    `;
    document.getElementById("item-count").textContent = "0";
    updateTotals();
    updateProductStocks();
    return;
}
    cartContainer.innerHTML = "";
    cart.forEach(item => {
        cartContainer.innerHTML += `
        <div class="border rounded-xl p-4 shadow-sm bg-base-100">
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="font-bold text-lg">${item.name}</h3>
                    <p class="text-sm text-base-content/60">
                        Rs. ${item.price}
                    </p>
                </div>
                <button
                    class="btn btn-error btn-xs"
                    onclick="removeFromCart(${item.id})"
                >
                    ✕
                </button>
            </div>
            <div class="flex justify-between items-center mt-4">
                <div class="join">
                    <button
                        class="btn btn-sm join-item"
                        onclick="changeQuantity(${item.id}, -1)"
                    >
                        -
                    </button>
                    <button
                        class="btn btn-sm join-item btn-disabled"
                    >
                        ${item.quantity}
                    </button>
                    <button
                        class="btn btn-sm join-item"
                        onclick="changeQuantity(${item.id}, 1)"
                    >
                        +
                    </button>
                </div>
                <div class="font-bold text-primary">
                    Rs. ${(item.price * item.quantity).toFixed(0)}
                </div>
            </div>
        </div>
        `;
    });
    document.getElementById("item-count").textContent = cart.length;

    updateTotals();
    updateProductStocks();
}

function changeQuantity(id, change) {
    const item = cart.find(i => i.id === id);
    if (!item) return;
    if (change > 0 && item.quantity >= item.stock) {
        return;
    }
    item.quantity += change;
    if (item.quantity <= 0) {
        removeFromCart(id);
        return;
    }
    renderCart();
}

function removeFromCart(id){
    const item = cart.find(i=>i.id===id);
    openConfirmModal(
        "Remove Item",
        `Remove ${item.name} from this bill?`,
        function(){
            cart = cart.filter(i=>i.id!==id);
            renderCart();
        }
    );
}

function clearCart() {
    if(cart.length===0) return;
    openConfirmModal(
        "🛒 Clear Cart",
        "Remove all items from this bill?",
        function(){
            cart=[];
            renderCart();
        }
    );
}

function updateProductStocks() {

    document.querySelectorAll(".card").forEach(card => {
        const id = Number(card.dataset.id);
        const originalStock = Number(card.dataset.stock);
        const cartItem = cart.find(i => i.id === id);
        const reserved = cartItem ? cartItem.quantity : 0;
        const remaining = originalStock - reserved;
        // Update stock number
        const stockSpan = card.querySelector(".stock-count");
        if (stockSpan) {
            stockSpan.textContent = remaining;
        }

        // Update Add button
        const addBtn = card.querySelector(".btn-primary");

        if (addBtn) {
            if (remaining <= 0) {
                addBtn.disabled = true;
                addBtn.innerHTML = "Unavailable";
                card.classList.add(
                    "opacity-70",
                    "cursor-not-allowed",
                    "border-error/30"
                );
                card.onclick = null;

            } else {
                addBtn.disabled = false;
                addBtn.innerHTML = '<i class="fas fa-plus"></i> Add';
                card.classList.remove(
                    "opacity-70",
                    "cursor-not-allowed",
                    "border-error/30"
                );
                card.onclick = function () {
                    addToCart(
                        id,
                        card.dataset.name,
                        Number(card.querySelector("h2")
                            .textContent.replace(/[^\d]/g, "")),
                        originalStock
                    );
                };
            }
        }
    });
}

function checkout() {
    alert('✅ Checkout functionality coming soon!\n\nTotal Amount: ' + document.getElementById('grand-total').textContent);
}