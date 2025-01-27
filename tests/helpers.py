from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json 

class TxParseVerification:

    # Locate the textarea input element and the button (using class names)
    xpath_textarea = '/html/body/div/div[2]/div[2]/main/div/div/div[1]/div[1]/textarea'
    xpath_decode = '/html/body/div/div[2]/div[2]/main/div/div/div[1]/div[1]/div/button[1]'
    xpath_parsed_tx = '/html/body/div/div[2]/div[2]/main/div/div/div[1]/div[2]/div[2]/pre'
  
    def __init__(self,raw_tx, url="https://www.blockchain.com/explorer/assets/btc/decode-transaction"):
        self.raw_tx = raw_tx
        self.url = url 
        options = Options()
        options.add_argument("--headless")  # Runs Chrome in headless mode
        options.add_argument("--no-sandbox")  # For environments like Docker
        options.add_argument("--disable-dev-shm-usage")  # To avoid certain ChromeDriver issues
        self.driver = webdriver.Firefox(options=options)

    def __call__(self,) -> dict: 
        self.driver.get(self.url)
        time.sleep(3)
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, TxParseVerification.xpath_textarea))).send_keys(self.raw_tx)
        self.driver.find_element(By.XPATH, TxParseVerification.xpath_decode).click()
        result = json.loads(self.driver.find_element(By.XPATH, TxParseVerification.xpath_parsed_tx).text)
        self.driver.quit()
        return result 