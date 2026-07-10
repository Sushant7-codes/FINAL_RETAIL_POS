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

    if (!validateCustomer()) return;

    const customer = document.getElementById("customer-name").value;
    const phone = document.getElementById("customer-phone").value;
    const total = document.getElementById("grand-total").textContent;
    const items = cart.reduce((sum, item) => sum + item.quantity, 0);

    openConfirmModal(
        "🧾 Complete Sale",
        `
        <div class="space-y-3">
            <div class="grid grid-cols-2 gap-2 text-sm">
                <span class="font-semibold">Customer</span>
                <span>${customer}</span>
                <span class="font-semibold">Phone</span>
                <span>${phone}</span>
                <span class="font-semibold">Items</span>
                <span>${items}</span>
                <span class="font-semibold">Discount</span>
                <span>${discountPercent}%</span>
            </div>
            <div class="divider my-1"></div>
            <div class="flex justify-between text-xl font-bold text-primary">
                <span>Total</span>
                <span>${total}</span>
            </div>
            <p class="text-center text-base-content/70 mt-2">
                Are you sure you want to complete this sale?
            </p>
        </div>
        `,
        function () {
            completeSale();
        }
    );

}