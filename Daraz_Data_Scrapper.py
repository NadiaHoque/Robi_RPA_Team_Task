from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time
import pandas as pd



class Scrape:
    def scrape():
        data_name = []
        data_price = []
        PATH = r"C:\Users\mouri.nadia\Downloads\chromedriver_win32\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        time.sleep(1)


        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-error")
        options.add_argument("--ignore-ssl-errors")


        s = Service(PATH)
        driver = webdriver.Chrome(service=s)
        url = "https://www.daraz.com.bd/"
        driver.get(url)


        user_input = input("What do you want to search?  ")
        driver.find_element(By.XPATH, "//input[@id='q']").send_keys(user_input)
        driver.find_element(By.XPATH, "//button[contains(text(),'SEARCH')]").send_keys(Keys.RETURN)
        time.sleep(3)


        items = driver.find_elements(By.CSS_SELECTOR, ".c2prKC")
        page = driver.find_elements(By.CSS_SELECTOR, ".ant-pagination-item")
        page_len = len(page)+1
        print(page_len)
        product_len = len(items)+1
        print(product_len)

        for i in range(1, page_len):
            print(i)
            for j in range(1, product_len):
                print(product_len)
                print(j)
                j = str(j)
                try:
                    name = driver.find_element(By.XPATH, "//body/div[@id='root']/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[" + j + "]/div[1]/div[1]/div[2]/div[2]").text
                    price = driver.find_element(By.XPATH, "//body/div[@id='root']/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[" + j + "]/div[1]/div[1]/div[2]/div[3]").text
                    print("Product name: " + name)
                    print("Product price: " + price)
                    # list of name and prices
                    data_name.append(name)
                    data_price.append(price)
                except:
                    print("We are done scraping!")

            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-pagination-next"))).click()
                time.sleep(20)
            except Exception as e:
                print(f'Error: {e}')
                break


        df = pd.DataFrame(list(zip(data_name, data_price)),columns =['Name', 'Price'])
        print(df)


        with pd.ExcelWriter('Daraz_Data_pandora.xlsx') as writer:
            df.to_excel(writer, sheet_name='sheet1', index=False)

        driver.close()

