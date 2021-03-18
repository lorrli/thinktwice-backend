from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob

def get_alternatives(): 
    DRIVER_PATH = '/Users/alisonwong/Documents/chromedriver'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    actions = ActionChains(driver)
    driver.get(product_url) 

    #function here 




    driver.quit()


    # textBlob investigation here 
