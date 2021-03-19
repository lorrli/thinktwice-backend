from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_setup(product_url):
    DRIVER_PATH = 'C:/Users/lli99/Downloads/chromedriver_win32/chromedriver.exe'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(product_url)
    return driver


def scrape_product_name_overview(brand, product_url):
    # function provides product name and overview
    driver = scrape_setup(product_url)
    scrape_data = {}

    if brand == 'patagonia':
        # Product Name
        scrape_data['product_name'] = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'product-title'))).text
        # Product Overview
        overview_title = driver.find_element_by_xpath(
            "/html/body/main/section/div[4]/section/div[2]/div/div/aside/h2")
        driver.execute_script("arguments[0].scrollIntoView();", overview_title)
        scrape_data['product_overview'] = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "/html/body/main/section/div[4]/section/div[2]/div/div/div/article/p"
            ))).text

    elif brand == 'gap' or brand == 'oldnavy':
        oldnavy_gap_setup(brand, driver)

        # Product title (try gap, except old navy)
        try:
            scrape_data['product_name'] = driver.find_element_by_class_name(
                'pdp-mfe-1stdnu').text
        except:
            scrape_data['product_name'] = driver.find_element_by_class_name(
                'pdp-mfe-1r6sye').text
        # Product overview, if exists
        details_drawer = driver.find_elements_by_class_name(
            'pdp-drawer-trigger')
        details_drawer[0].click()
        try:
            scrape_data[
                'product_overview'] = driver.find_element_by_class_name(
                    "product-information-item__overview").text
        except:
            scrape_data['product_overview'] = None

    elif brand == 'adidas':
        scrape_data['product_name'] = driver.find_element_by_xpath(
            "//*[@id='app']/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/h1/span"
        ).text
        driver.execute_script("window.scrollTo(0, 400)")
        description_button = driver.find_element_by_id("description")
        driver.execute_script("arguments[0].scrollIntoView();",
                              description_button)
        description_button.click()
        scrape_data['product_overview'] = driver.find_element_by_xpath(
            "//*[@id='navigation-target-description']/div/div[1]/p").text

    else:
        print('Could not find product name and overview on ' + brand)
        pass

    driver.quit()
    return scrape_data


def scrape_product_details(brand, product_url, driver):
    # function provides product details
    driver.get(product_url)
    scrape_data = {}

    if brand == 'patagonia':
        overview_title = driver.find_element_by_xpath(
            "/html/body/main/section/div[4]/section/div[2]/div/div/aside/h2")
        driver.execute_script("arguments[0].scrollIntoView();", overview_title)
        specs_button = driver.find_element_by_xpath(
            "/html/body/main/section/div[4]/section/div[2]/div/div/div/div[2]/a"
        )
        specs_button.click()
        # Product Details Bullet Points
        product_details_raw = driver.find_elements_by_xpath(
            "/html/body/main/section/div[4]/section/div[3]/div/div/div/ul/li")
        product_details = []
        for detail in product_details_raw:
            product_details.append(detail.text.lower())
        fabric_raw = driver.find_elements_by_xpath(
            "/html/body/main/section/div[4]/section/div[4]/div/div/div/ul/li")
        for detail in fabric_raw:
            product_details.append(detail.text.lower())

    elif brand == 'gap' or brand == 'oldnavy':
        oldnavy_gap_setup(brand, driver)

        details_drawer = driver.find_elements_by_class_name(
            'pdp-drawer-trigger')
        details_drawer[0].click()
        # Product details bullet points
        product_details_raw = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'product-information-item__list-item')))
        product_details_raw = driver.find_elements_by_class_name(
            "product-information-item__list-item")
        product_details = []
        for detail in product_details_raw:
            product_details.append(detail.text.lower())
        fabric_drawer = driver.find_element_by_id(
            "product-info-tabs-button--1")
        fabric_drawer.click()
        fabric_raw = driver.find_elements_by_class_name(
            "product-information-item__list-item")
        for detail in fabric_raw:
            product_details.append(detail.text.lower())
        product_details = list(filter(None, product_details))

    elif brand == 'adidas':
        driver.execute_script("window.scrollTo(0, 400)")
        details_button = driver.find_element_by_id('specifications')
        details_button.click()
        product_details = []
        details_title = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//*[@id='navigation-target-specifications']/div/h5")))
        product_details_raw = driver.find_elements_by_xpath(
            "//*[@id='navigation-target-specifications']/div/div/ul/li")
        for detail in product_details_raw:
            product_details.append(detail.text.lower())
    else:
        print('Could not find product details on ' + brand)
        pass
    return product_details


def scrape_for_alternatives(brand, product_url):
    # function provides product name, color, price
    driver = scrape_setup(product_url)
    scrape_data = {}

    if brand == 'patagonia':
        scrape_data['product_name'] = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'product-title'))).text
        photo_gallery = driver.find_element_by_xpath(
            "/html/body/main/section/div[4]/div[2]/div[1]/div[2]/div/div")
        driver.execute_script("arguments[0].scrollIntoView();", photo_gallery)
        scrape_data['image'] = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                "body > main > section > div.page.page-pdp.product-detail > div.hero.hero-pdp > div.hero-pdp__content-top > div.hero-pdp__slider > div > div > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > div > img"
            ))).get_attribute("src")
        style_number = driver.find_element_by_xpath(
            "//*[@id='hero-pdp__buy']/div/div[1]/strong")
        driver.execute_script("arguments[0].scrollIntoView();", style_number)
        scrape_data['product_color'] = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                "#hero-pdp__buy > div > div.buy-config__title.sk-init.sk-show.sk-viewport-in > span.js-buy-config-select-color.buy-config-select-color"
            ))).text
        try:
            # fetch sale price, if exists
            scrape_data['product_price'] = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//*[@id='hero-pdp__buy']/div/div[1]/span[2]/div/span/span[2]/span"
                ))).text
        except:
            # original price
            scrape_data['product_price'] = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//*[@id='hero-pdp__buy']/div/div[1]/span[2]/div/span/span/span"
                ))).text

    elif brand == 'gap' or brand == 'oldnavy':
        oldnavy_gap_setup(brand, driver)

        # Product title (gap, else old navy)
        if brand == 'gap':
            scrape_data['product_name'] = driver.find_element_by_class_name(
                'pdp-mfe-1stdnu').text
        else:
            scrape_data['product_name'] = driver.find_element_by_class_name(
                'pdp-mfe-1r6sye').text
        # Product color
        scrape_data['product_color'] = driver.find_element_by_xpath(
            "//*[@id='swatch-label--Color']").text[7:]
        #Product price
        scrape_data['product_price'] = driver.find_element_by_class_name(
            'pdp-pricing__selected ').text

    elif brand == 'adidas':
        scrape_data['product_name'] = driver.find_element_by_xpath(
            "//*[@id='app']/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/h1/span"
        ).text
        scrape_data['product_color'] = driver.find_element_by_xpath(
            "//*[@id='app']/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[2]/h5/span"
        ).text
        scrape_data['product_price'] = driver.find_element_by_xpath(
            "//*[@id='app']/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div"
        ).text

    else:
        print('Could not find alternative details on ' + brand)
        pass

    driver.quit()
    return scrape_data


def oldnavy_gap_setup(brand, driver):
    # removes the promo drawer from the DOM
    promo_drawer = driver.find_element_by_id("wrapper-for-mobile-app")
    driver.execute_script(
        """var promo_drawer = arguments[0];
    promo_drawer.parentNode.removeChild(promo_drawer);
        """, promo_drawer)

    # closes coupon popup
    if brand == 'gap':
        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[6]/div/div[2]/div[1]/button')))
            close_button.click()
        except:
            pass