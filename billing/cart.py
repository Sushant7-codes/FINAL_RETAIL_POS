from decimal import Decimal


class Cart:
    def __init__(self, request):
        """
        Initialize the shopping cart stored in session.
        """
        self.session = request.session

        cart = self.session.get("cart")

        if cart is None:
            cart = self.session["cart"] = {}

        self.cart = cart

    def save(self):
        """
        Mark session as modified.
        """
        self.session.modified = True

    def add(self, item):
        """
        Add an item to the cart.
        If already present, increase quantity.
        """

        item_id = str(item.id)

        if item_id not in self.cart:
            self.cart[item_id] = {
                "id": item.id,
                "name": item.name,
                "price": str(item.amount),
                "quantity": 1,
            }
        else:
            self.cart[item_id]["quantity"] += 1

        self.save()

    def remove(self, item_id):
        """
        Remove an item completely.
        """

        item_id = str(item_id)

        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def update_quantity(self, item_id, quantity):
        """
        Update quantity of an item.
        """

        item_id = str(item_id)

        if item_id in self.cart:
            if quantity <= 0:
                self.remove(item_id)
            else:
                self.cart[item_id]["quantity"] = quantity

            self.save()

    def clear(self):
        """
        Empty the cart.
        """

        self.session["cart"] = {}
        self.save()

    def get_items(self):
        """
        Return cart items with subtotal.
        """

        items = []

        for item in self.cart.values():

            price = Decimal(item["price"])

            subtotal = price * item["quantity"]

            items.append({
                **item,
                "subtotal": subtotal
            })

        return items

    def get_subtotal(self):
        """
        Calculate total bill.
        """

        total = Decimal("0.00")

        for item in self.cart.values():

            total += Decimal(item["price"]) * item["quantity"]

        return total

    def count(self):
        """
        Total number of products.
        """

        return sum(item["quantity"] for item in self.cart.values())