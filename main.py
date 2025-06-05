import customtkinter
import scraper
from customtkinter import CTkScrollableFrame
import database
import customtkinter as ctk
import matplotlib.pyplot as plt

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1300x800")
app.title("Price Tracker")

frame_1 = customtkinter.CTkFrame(master=app, fg_color="transparent")
frame_1.pack()

label_1 = customtkinter.CTkLabel(master=frame_1, text='Amazon Price History Tracker', font=('times new roman', 24))
label_1.pack(padx=20, pady=20)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text='Enter Product Name')
entry_1.pack(side='left', padx=10, pady=10)

button_1 = customtkinter.CTkButton(master=frame_1, text="Search")
button_1.pack(side='left', padx=10, pady=10)

frame = customtkinter.CTkFrame(master=app)
frame.pack(padx=10, pady=10, fill="both", expand=True)

header_frame = customtkinter.CTkFrame(master=frame)
header_frame.pack(fill="x", pady=5)

customtkinter.CTkLabel(master=header_frame, text="Name", width=300).pack(side="left", padx=5)
customtkinter.CTkLabel(master=header_frame, text="Price", width=100).pack(side="left", padx=15)
customtkinter.CTkLabel(master=header_frame, text="URL", width=600).pack(side="left", padx=5)
customtkinter.CTkLabel(master=header_frame, text="History", width=100).pack(side="left")
# customtkinter.CTkLabel(master=header_frame, text="Graph", width=100).pack(side="left", padx = (0, 30))
customtkinter.CTkLabel(
    master=header_frame,
    text="Graph",
    width=100,
    anchor="w",  
    justify="left"  
).pack(side="left", padx=(5, 0))  
product_rows_frame = CTkScrollableFrame(master=frame, width=1100, height=500)  # adjust size as needed
product_rows_frame.pack(fill="both", expand=True, padx=10, pady=10)


def track_product(product_info):
    # print("Tracking:", product_info)
    product_details = database.search_product_by_exact_name(product_info['Name'])
    
    if not product_details:
        print("Product not found in database.")
        return

    new_window = ctk.CTkToplevel()
    new_window.geometry("700x500")
    new_window.title("Product history")

    # Title label
    label = ctk.CTkLabel(new_window, text=f"Product History of {product_details[0][0]}")
    label.pack(pady=10, padx=10)

    # ✅ Scrollable Frame
    scrollable_frame = ctk.CTkScrollableFrame(new_window, width=650, height=400)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Loop through each row (in case there are multiple matches)
    for row in product_details:
        print("Row: ", row)
        name, price, url, timestamp = row
        # print(f"Tracked Product: {name} {price} {url}")

        # Display Name and Price
        ctk.CTkLabel(scrollable_frame, text=f"Name: {name}").pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(scrollable_frame, text=f"Price: {price}").pack(anchor="w", padx=5, pady=5)

        # URL inside sub-frame for alignment
        url_frame = ctk.CTkFrame(master=scrollable_frame, fg_color="transparent")
        url_frame.pack(anchor="w", padx=5, pady=5)

        ctk.CTkLabel(url_frame, text="URL:", font=('times new roman', 18)).pack(side="left", padx=5)
        url_entry = ctk.CTkEntry(master=url_frame, width=500)
        url_entry.insert(0, url)
        url_entry.configure(state="readonly")
        url_entry.pack(side="left", padx=5)


    
def wrap_text(text, limit=60):
    """Wraps text after `limit` characters (word-safe)."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) + 1 <= limit:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return "\n".join(lines)

def plot_by_rowid(product_info):
    # print("Tracking:", product_info)
    product_details = database.search_product_by_exact_name_with_row_id(product_info['Name'])
    
    if not product_details:
        print("Product not found in database.")
        return

    
    timestamps = [row[3] for row in product_details]
    prices = [row[1] for row in product_details]
    plt.figure(figsize=(10,6))
    plt.plot(timestamps, prices, marker='o')
    plt.xlabel("Timestamp")
    plt.ylabel("Price")
    plt.title("Price History")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def button_callback(product):
    if not product:
        return
    for widget in product_rows_frame.winfo_children():
        widget.destroy()
    example_data = scraper.price_check(product)
    # example_data = database.search_product_by_name(product)
    if not example_data:
        customtkinter.CTkLabel(product_rows_frame, text="No products found.").pack()
        return
    for item in example_data:
        row_frame = customtkinter.CTkFrame(master=product_rows_frame)
        row_frame.pack(fill="x", pady=2)

        wrapped_name = wrap_text(item["Name"], limit=40)

        customtkinter.CTkLabel(master=row_frame, text=wrapped_name, width=300, anchor='w', justify='left').pack(side="left", padx=5)
        customtkinter.CTkLabel(master=row_frame, text=str(item["Price"]) if item["Price"] else "N/A", width=100).pack(side="left", padx=5)
        url_entry = customtkinter.CTkEntry(master=row_frame, width=600)
        url_entry.insert(0, item["URL"])
        url_entry.configure(state="readonly")  # So user can't accidentally edit
        url_entry.pack(side="left", padx=5)
        customtkinter.CTkButton(master=row_frame, text="Track", width=80, command=lambda i=item: track_product(i)).pack(side="left", padx=5)
        customtkinter.CTkButton(master=row_frame, text="Plot Graph", width=80, command=lambda i=item: plot_by_rowid(i)).pack(side="left", padx=5)



# Link button to callback
button_1.configure(command=lambda: button_callback(entry_1.get()))

app.mainloop()
