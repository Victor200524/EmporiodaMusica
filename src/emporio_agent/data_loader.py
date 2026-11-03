# Load the store data from the CSV files

import json
import unicodedata
import pandas as pd

DATA_FOLDER = "data"

# Make text lowercase and remove accents
def normalize(text):
    text = str(text).lower().strip()
    text = unicodedata.normalize("NFKD", text)
    result = ""
    for char in text:
        if not unicodedata.combining(char):
            result = result + char
    return result


# Read one CSV file from the data folder
def read_csv(name):
    return pd.read_csv(DATA_FOLDER + "/" + name + ".csv")


# Load all tables and prepare them for the tools
def load_data():
    products = read_csv("products")
    categories = read_csv("categories")
    promotions = read_csv("promotions")
    orders = read_csv("orders")
    order_items = read_csv("order_items")
    customers = read_csv("customers")

    # Add the category name to each product
    category_names = {}
    for _, row in categories.iterrows():
        category_names[row["category_id"]] = row["name"]
    products["category"] = products["category_id"].map(category_names)

    # Specs is a JSON text, convert it to a Python dict
    products["specs"] = products["specs"].apply(json.loads)

    # Text without accents, used by the product search
    products["search_text"] = (products["name"] + " " + products["category"]).apply(normalize)

    # Empty cells become empty text
    orders = orders.fillna("")

    return {
        "products": products,
        "categories": categories,
        "promotions": promotions,
        "orders": orders,
        "order_items": order_items,
        "customers": customers,
    }