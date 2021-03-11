from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = '/Users/alisonwong/Documents/chromedriver'
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
actions = ActionChains(driver)
# This script will work with any Patagonia link, to test, change the PRODUCT_URL variable 

PRODUCT_URL = "https://www.patagonia.ca/product/womens-powslayer-ski-snowboard-pants/30345.html?dwvar_30345_color=CUA&cgid=root"

# product page 
driver.get(PRODUCT_URL) 

# Product Name, Color, Price
product_name = driver.find_element_by_id('product-title').text 
photo_gallery = driver.find_element_by_xpath("/html/body/main/section/div[4]/div[2]/div[1]/div[2]/div/div")
driver.execute_script("arguments[0].scrollIntoView();", photo_gallery)

product_color = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#hero-pdp__buy > div > div.buy-config__title.sk-init.sk-show.sk-viewport-in > span.js-buy-config-select-color.buy-config-select-color"))).text
try: 
    # sale price
    product_price = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='hero-pdp__buy']/div/div[1]/span[2]/div/span/span[2]/span"))).text
except: 
    # original price
    product_price = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='hero-pdp__buy']/div/div[1]/span[2]/div/span/span/span"))).text

# Product Overview
overview_title = driver.find_element_by_xpath("/html/body/main/section/div[4]/section/div[2]/div/div/aside/h2")
driver.execute_script("arguments[0].scrollIntoView();", overview_title)
product_overview = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/div[4]/section/div[2]/div/div/div/article/p"))).text
specs_button = driver.find_element_by_xpath("/html/body/main/section/div[4]/section/div[2]/div/div/div/div[2]/a")
specs_button.click()

# Product Details Bullet Points 
product_details_raw = driver.find_elements_by_xpath("/html/body/main/section/div[4]/section/div[3]/div/div/div/ul/li")
total_details = []
for detail in product_details_raw: 
    total_details.append(detail.text)
fabric_raw = driver.find_elements_by_xpath("/html/body/main/section/div[4]/section/div[4]/div/div/div/ul/li")
for detail in fabric_raw: 
    total_details.append(detail.text)

print('\n')
print ('Name: ' + product_name)
print('Overview: ' + product_overview)
print('Details: ')
print(total_details)
print('Color: ' + product_color)
print('Price: ' + product_price)
driver.quit() 