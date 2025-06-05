# 🛒 Amazon Product Price History Tracker

A desktop application to track price changes of Amazon products over time.

### 🔍 Features:
- Search products on Amazon (first page of results, configurable for more).
- View results in a CustomTkinter GUI with a scrollable interface.
- Track individual product price history.
- Display price vs. timestamp graphs using `matplotlib`.
- Store product data using SQLite.

### 🧰 Built With:
- Python
- Selenium
- CustomTkinter
- Matplotlib
- SQLite
- Fake UserAgent

### 📸 Screenshots:
![Demo Screenshot](https://github.com/Rafin-25/Amazon-Price-History-Tracker/blob/main/demo-screenshots/screenshot%201.png)
![Demo Screenshot](https://github.com/Rafin-25/Amazon-Price-History-Tracker/blob/main/demo-screenshots/screenshot%202.png)
![Demo Screenshot](https://github.com/Rafin-25/Amazon-Price-History-Tracker/blob/main/demo-screenshots/screenshot%203.png)


## 📦 Installation

To run this project, install the required packages by running the following command in your terminal, then run main.py:

```bash
pip install customtkinter matplotlib selenium fake-useragent undetected-chromedriver
python main.py
```


### 🚀 Future Improvements:
- Add support for multiple Amazon regions.
- Background price monitoring and notifications.
