from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_brand(brand, product_url):
    DRIVER_PATH = '/Users/alisonwong/Documents/chromedriver'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    actions = ActionChains(driver)
    driver.get(product_url) 
    scrape_data = {}
    
    if brand == 'patagonia':
        # Product Name, Color, Price
        scrape_data['product_name'] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'product-title'))).text
        photo_gallery = driver.find_element_by_xpath("/html/body/main/section/div[4]/div[2]/div[1]/div[2]/div/div")
        driver.execute_script("arguments[0].scrollIntoView();", photo_gallery)

        scrape_data['product_color'] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#hero-pdp__buy > div > div.buy-config__title.sk-init.sk-show.sk-viewport-in > span.js-buy-config-select-color.buy-config-select-color"))).text
        try: 
            # fetch sale price, if exists
            scrape_data['product_price'] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='hero-pdp__buy']/div/div[1]/span[2]/div/span/span[2]/span"))).text
        except: 
            # original price
            scrape_data['product_price'] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='hero-pdp__buy']/div/div[1]/span[2]/div/span/span/span"))).text

        # Product Overview
        overview_title = driver.find_element_by_xpath("/html/body/main/section/div[4]/section/div[2]/div/div/aside/h2")
        driver.execute_script("arguments[0].scrollIntoView();", overview_title)
        scrape_data['product_overview'] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/div[4]/section/div[2]/div/div/div/article/p"))).text
        specs_button = driver.find_element_by_xpath("/html/body/main/section/div[4]/section/div[2]/div/div/div/div[2]/a")
        specs_button.click()

        # Product Details Bullet Points 
        product_details_raw = driver.find_elements_by_xpath("/html/body/main/section/div[4]/section/div[3]/div/div/div/ul/li")
        scrape_data['product_details'] = []
        for detail in product_details_raw: 
            scrape_data['product_details'].append(detail.text.lower())
        fabric_raw = driver.find_elements_by_xpath("/html/body/main/section/div[4]/section/div[4]/div/div/div/ul/li")
        for detail in fabric_raw: 
            scrape_data['product_details'].append(detail.text.lower())

    elif brand == 'gap':
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

        # Product title (try gap, except old navy)
        try:
            scrape_data['product_name'] = driver.find_element_by_class_name('pdp-mfe-1stdnu').text 
        except:
            scrape_data['product_name'] = driver.find_element_by_class_name('pdp-mfe-1r6sye').text 

        #Product price
        scrape_data['product_price'] = driver.find_element_by_class_name('pdp-pricing__selected ').text    

    elif brand == 'adidas':
        scrape_data['product_name'] = driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/h1/span").text
        scrape_data['product_color'] = driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[2]/h5/span").text
        scrape_data['product_price'] = driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div").text
        driver.execute_script("window.scrollTo(0, 900)") 
        description_button = driver.find_element_by_id("description")
        driver.execute_script("arguments[0].scrollIntoView();", description_button)
        description_button.click()
        scrape_data['product_overview'] = driver.find_element_by_xpath("//*[@id='navigation-target-description']/div/div[1]/p").text
        details_button = driver.find_element_by_id('specifications')
        details_button.click()
        scrape_data['product_details'] = []
        details_title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='navigation-target-specifications']/div/h5")))
        product_details_raw = driver.find_elements_by_xpath("//*[@id='navigation-target-specifications']/div/div/ul/li")
        for detail in product_details_raw: 
            scrape_data['product_details'].append(detail.text.lower())

    else: 
        print('Could not scrape site')    
        pass
    
    driver.quit() 
    return scrape_data