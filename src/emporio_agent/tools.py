# Tools the agent can call to look up store data

import os
from datetime import datetime

from emporio_agent.data_loader import load_data, normalize

DATA = load_data()


# Return the active promotion of a product, or None
def get_active_promotion(product_id):
    promotions = DATA["promotions"]
    active = promotions[(promotions["product_id"] == product_id) & (promotions["is_active"] == 1)]
    if len(active) == 0:
        return None
    return active.iloc[0]


# Convert a product row into a simple dict for the agent
def product_to_dict(product):
    result = {
        "product_id": int(product["product_id"]),
        "name": product["name"],
        "category": product["category"],
        "price_brl": float(product["price_brl"]),
        "stock_quantity": int(product["stock_quantity"]),
        "status": product["status"],
    }

    promotion = get_active_promotion(product["product_id"])
    if promotion is not None:
        discount = int(promotion["discount_percent"])
        result["promotion"] = promotion["description"]
        result["discount_percent"] = discount
        result["final_price_brl"] = round(result["price_brl"] * (100 - discount) / 100, 2)

    return result

def search_products(
    query: str = "",
    category: str = "",
    min_price: float = 0.0,
    max_price: float = 0.0,
    only_available: bool = True,
) -> dict:
    """Search products in the store catalog.

    Args:
        query: Words to find in the product name, like a brand or model. Example: "Takamine GD20".
        category: Exact category name, like "Violões" or "Guitarras".
        min_price: Minimum price in BRL. Use 0 for no limit.
        max_price: Maximum price in BRL. Use 0 for no limit.
        only_available: If true, return only active products with stock.
    """
    products = DATA["products"]

    # Keep only products that have every word of the query
    if query != "":
        for word in normalize(query).split():
            products = products[products["search_text"].str.contains(word, regex=False)]

    if category != "":
        products = products[products["category"].apply(normalize) == normalize(category)]

    if min_price > 0:
        products = products[products["price_brl"] >= min_price]

    if max_price > 0:
        products = products[products["price_brl"] <= max_price]

    if only_available:
        products = products[(products["stock_quantity"] > 0) & (products["status"] == "active")]

    # Cheapest first, and at most 15 results
    products = products.sort_values("price_brl")
    results = []
    for _, product in products.head(15).iterrows():
        results.append(product_to_dict(product))

    return {"total_found": len(products), "products": results}

def get_product_details(product_id: int) -> dict:
    """Get full details of one product: description, specs and promotions.

    Args:
        product_id: The product id, found with search_products.
    """
    products = DATA["products"]
    found = products[products["product_id"] == product_id]
    if len(found) == 0:
        return {"error": "Product not found."}

    product = found.iloc[0]
    result = product_to_dict(product)
    result["description"] = product["description"]
    result["specs"] = product["specs"]

    # Old promotions, so the agent can say they are no longer valid
    promotions = DATA["promotions"]
    old = promotions[(promotions["product_id"] == product_id) & (promotions["is_active"] == 0)]
    result["expired_promotions"] = list(old["description"])

    return result


def list_categories() -> dict:
    """List all product categories sold by the store."""
    categories = []
    for _, row in DATA["categories"].iterrows():
        categories.append({"name": row["name"], "description": row["description"]})
    return {"categories": categories}

def get_active_promotions(category: str = "") -> dict:
    """List products with an active promotion.

    Args:
        category: Optional category name, like "Ukuleles". Empty for all categories.
    """
    promotions = DATA["promotions"]
    products = DATA["products"]
    active = promotions[promotions["is_active"] == 1]

    results = []
    for _, promotion in active.iterrows():
        product = products[products["product_id"] == promotion["product_id"]].iloc[0]
        if category != "" and normalize(product["category"]) != normalize(category):
            continue
        results.append(product_to_dict(product))

    return {"promotions": results}


# Keep only the digits of a text, like a phone number
def only_digits(text):
    result = ""
    for char in str(text):
        if char.isdigit():
            result = result + char
    return result


def get_order_status(order_id: int, email_or_phone: str) -> dict:
    """Get the status of an order. The customer must give the email or phone used in the purchase.

    Args:
        order_id: The order number.
        email_or_phone: Email or phone of the customer who made the order.
    """
    # Same message for both errors, so we don't reveal if the order exists
    not_found = {"error": "Order not found or contact does not match."}

    orders = DATA["orders"]
    found = orders[orders["order_id"] == order_id]
    if len(found) == 0:
        return not_found
    order = found.iloc[0]

    # Check the identity of the customer before showing the order
    customers = DATA["customers"]
    customer = customers[customers["customer_id"] == order["customer_id"]].iloc[0]
    contact = email_or_phone.strip().lower()
    email_ok = contact == customer["email"].lower()
    phone_ok = only_digits(contact) != "" and only_digits(contact) == only_digits(customer["phone"])
    if not email_ok and not phone_ok:
        return not_found

    # Products in the order
    products = DATA["products"]
    order_items = DATA["order_items"]
    items = []
    for _, item in order_items[order_items["order_id"] == order_id].iterrows():
        product = products[products["product_id"] == item["product_id"]].iloc[0]
        items.append({"product": product["name"], "quantity": int(item["quantity"])})

    return {
        "order_id": int(order["order_id"]),
        "customer_first_name": customer["name"].split()[0],
        "order_date": order["order_date"],
        "status": order["status"],
        "total_brl": float(order["total_brl"]),
        "payment_method": order["payment_method"],
        "tracking_code": order["tracking_code"],
        "estimated_delivery": order["estimated_delivery"],
        "notes": order["notes"],
        "items": items,
    }

def register_complaint(customer_name: str, contact: str, complaint: str, order_id: int = 0) -> dict:
    """Register a customer complaint and send it to the store manager.

    Args:
        customer_name: Name of the customer.
        contact: Email or phone to send the answer.
        complaint: Short summary of the problem.
        order_id: Related order number. Use 0 if there is no order.
    """
    # In this prototype the complaint is saved in a local file
    os.makedirs("logs", exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("logs/complaints.txt", "a", encoding="utf-8") as file:
        file.write(f"{now} | {customer_name} | {contact} | order {order_id} | {complaint}\n")

    return {"registered": True, "answer_deadline": "24 business hours"}
