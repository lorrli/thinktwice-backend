from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 

DRIVER_PATH = '/Users/alisonwong/Documents/chromedriver'
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
actions = ActionChains(driver)
# This script will work with any Old Navy or Gap Link, to test, change the PRODUCT_URL variable 

# find a way to get the url or brand namefrom the front end 
# which will be sent to the backend for info 
PRODUCT_URL = "https://oldnavy.gapcanada.ca/browse/product.do?pid=551203023&rrec=true&mlink=5050,12413545,onproduct2_rr_3&clink=12413545"

# product page 
driver.get(PRODUCT_URL) 
# driver.save_screenshot('/src/webscraping/ss_actual orig screen.png')

details_drawer = driver.find_elements_by_class_name('pdp-drawer-trigger')
try:
    details_drawer[0].click()
except: 
    actions.send_keys(Keys.SPACE)
    actions.perform()
    details_drawer[0].click()
    
# Product details 
try: 
    product_overview = driver.find_element_by_class_name("product-information-item__overview").text
except: 
    product_overview = "N/A"

# Product Details Bullet Points 
product_details_raw = driver.find_elements_by_class_name("product-information-item__list-item")
total_details = []
for detail in product_details_raw: 
    total_details.append(detail.text)
fabric_drawer = driver.find_element_by_id("product-info-tabs-button--1")
fabric_drawer.click()
fabric_raw = driver.find_elements_by_class_name("product-information-item__list-item")
for detail in fabric_raw: 
    total_details.append(detail.text)
total_details = list(filter(None, total_details))
close_drawer = driver.find_element_by_class_name('pdp-drawer__close-button')
close_drawer.click()

# Product picture / color
product_color = driver.find_element_by_xpath("//*[@id='swatch-label--Color']").text
product_color = product_color[7:]

# product title
try:
    product_name = driver.find_element_by_class_name('pdp-mfe-1stdnu').text #gap class
except:
    product_name = driver.find_element_by_class_name('pdp-mfe-1r6sye').text #old navy class

#price
product_price = driver.find_element_by_class_name('pdp-pricing__selected ').text

print ('Name: ' + product_name)
print('Overview: ' + product_overview)
print('Details: ')
print(total_details)
print('Color: ' + product_color)
print('Price: ' + product_price)
driver.quit() 
