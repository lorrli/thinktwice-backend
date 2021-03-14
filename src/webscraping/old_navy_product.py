from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 

def scrape_old_navy_gap(product_url):
    # need to figure out these configurations in terms of deployment
    DRIVER_PATH = '/Users/alisonwong/Documents/chromedriver'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    actions = ActionChains(driver)
    scrape_data = {}

    driver.get(product_url) 

    # dismissing promo popup, if exists
    details_drawer = driver.find_elements_by_class_name('pdp-drawer-trigger')
    try:
        details_drawer[0].click()
    except: 
        actions.send_keys(Keys.SPACE)
        actions.perform()
        details_drawer[0].click()
        
    # Product overview, if exists
    try: 
        scrape_data['product_overview'] = driver.find_element_by_class_name("product-information-item__overview").text
    except: 
        scrape_data['product_overview'] = None

    # Product details bullet points 
    product_details_raw = driver.find_elements_by_class_name("product-information-item__list-item")
    product_details = []
    for detail in product_details_raw: 
        product_details.append(detail.text.lower())
    fabric_drawer = driver.find_element_by_id("product-info-tabs-button--1")
    fabric_drawer.click()
    fabric_raw = driver.find_elements_by_class_name("product-information-item__list-item")
    for detail in fabric_raw: 
        product_details.append(detail.text.lower())
    scrape_data['product_details'] = list(filter(None, product_details))
    close_drawer = driver.find_element_by_class_name('pdp-drawer__close-button')
    close_drawer.click()

    # Product color
    scrape_data['product_color'] = driver.find_element_by_xpath("//*[@id='swatch-label--Color']").text[7:]

    # Product title
    try:
        #gap class
        scrape_data['product_name'] = driver.find_element_by_class_name('pdp-mfe-1stdnu').text 
    except:
        #old navy class
        scrape_data['product_name'] = driver.find_element_by_class_name('pdp-mfe-1r6sye').text 

    #Product price
    scrape_data['product_price'] = driver.find_element_by_class_name('pdp-pricing__selected ').text    
    driver.quit() 
    return scrape_data
