import sqlite3
from datetime import datetime

def add_many(data):
    conn = sqlite3.connect('PriceTrackerDatabase.db')
    c = conn.cursor()

    # Get current timestamp in desired format
    current_time = datetime.now().strftime("%H:%M %d-%m-%Y")  # e.g. "14:32 03-06-2025"

    # Add timestamp to each data row
    data_with_time = [(name, price, url, current_time) for (name, price, url) in data]

    # Make sure to use 4 placeholders now
    c.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", data_with_time)
    conn.commit()
    conn.close()
def search_product_by_exact_name(name: str):
    conn = sqlite3.connect('PriceTrackerDatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE Name = ?", (name,))
    
    detailed_product = c.fetchall()
    # print(f"Product Type--------------------------------------------------------> {type(detailed_product)}")
    conn.close()
    return detailed_product


def search_product_by_exact_name_with_row_id(name: str):
    conn = sqlite3.connect('PriceTrackerDatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE Name = ?", (name,))
    
    detailed_product = c.fetchall()
    # print(f"Product Type--------------------------------------------------------> {type(detailed_product)}")
    conn.close()
    return detailed_product


def search_product_by_lower_case_name(name: str):
    conn = sqlite3.connect('PriceTrackerDatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE LOWER(Name) = LOWER(?)", (name,))
    detailed_product = c.fetchall()
    conn.close()
    return detailed_product

def search_product_by_name(name: str):
    conn = sqlite3.connect('PriceTrackerDatabase.db')
    conn.row_factory = sqlite3.Row  #
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE Name LIKE ?", ('%' + name + '%',))
    matched_products = c.fetchall()
    
    conn.close()
    return matched_products