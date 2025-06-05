from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.parse
import time
import random
from fake_useragent import UserAgent
import database
import undetected_chromedriver as uc


def get_driver():
    ua = UserAgent()
    user_agent = ua.random


    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US,en")

    return uc.Chrome(options=options)
def price_check(search: str):
    driver = get_driver()
    result = []
    for i in range(1,2):
        encoded_search = urllib.parse.quote_plus(search)
        search_url = f"https://www.amazon.com/s?k={encoded_search}&page={i}"
        print(f"[INFO] Fetching URL: {search_url}")
        driver.get(search_url)
        time.sleep(random.uniform(4, 8))
        products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
        time.sleep(random.uniform(2,5))
        for product in products:
            try:
                names = product.find_elements(By.TAG_NAME, 'h2')
                full_name = " ".join(name.text for name in names)
                try:
                    price_whole = product.find_element(By.CSS_SELECTOR, ".a-price-whole").text.replace(',', '')
                    price_fraction = product.find_element(By.CSS_SELECTOR, ".a-price-fraction").text
                    full_price = float(f"{price_whole}.{price_fraction}")
                except:
                    full_price = None
                product_url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
                
                result.append({
                    "Name": full_name,
                    "Price": full_price,
                    "URL": product_url
                })
            except Exception as e:
                print(f"[ERROR] Skipping product due to error: {e}")
                continue

    if result:
        database.add_many([(r["Name"], r["Price"], r["URL"]) for r in result])
    driver.quit()
    return result


