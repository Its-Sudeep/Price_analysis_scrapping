from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.flipkart.com/")

curr_title = driver.title
print(curr_title)
expected_title = "Online Shopping Site for Mobiles, Electronics, Furniture, Grocery, Lifestyle, Books & More. Best Offers!"

if curr_title != expected_title:
    print("Went to Flipkart.com but got wrong title. Current title : {}.". format(curr_title))


try:
    search_btn_elm = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.NAME,"q"))
    )
    search_btn_elm.send_keys("laptops")
    search_btn_elm.send_keys(Keys.RETURN)

    product_name_elm = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="KzDlHZ"]'))
    )

    product_price_elm = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Nx9bqj _4b5DiR"]'))
    )
    
    product_name = [prod.text for prod in product_name_elm[:10]]
    prices = [price.text for price in product_price_elm[:10]]

    if not product_name or not prices:
        print("Error: No data found!")

    # Saving data to csv
    df = pd.DataFrame({"Product Name": product_name, "Product Prices": prices})
    df.to_csv("flipkart_laptops.csv", index=False)

    print("Scrapping Completed! Data saved to flipkart_laptops.csv")


except Exception as e:
    print(f"Error!: {e}")

finally:
    driver.quit()