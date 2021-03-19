from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob
from fuzzywuzzy import fuzz

from scrape_product import scrape_product_details, scrape_for_alternatives
from material_matching import calculate_material_composition


def check_sus_rating(brand_name, item, driver):
    print("CHCKING SUS")
    product_details = scrape_product_details(brand_name, item, driver)
    print(product_details)
    rating_details = calculate_material_composition(product_details)
    print(rating_details)
    return rating_details


def scrape_setup():
    DRIVER_PATH = 'C:/Users/lli99/Downloads/chromedriver_win32/chromedriver.exe'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    return driver


def get_alternatives(query_list):
    driver = scrape_setup()
    pata_base_url = "https://www.patagonia.ca/search/?q="
    adidas_base_url = "https://www.adidas.ca/en/search?q="
    brand_names = ["patagonia", "adidas"]
    max_reached_pata = False
    max_reached_adidas = False
    query_index = 0
    products = set()
    alt_data = []
    while not max_reached_pata and query_index < 3:
        driver.get(pata_base_url + query_list[query_index])
        try:
            item1 = (WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    '//*[@id="product-search-results"]/div[2]/div/div/div[2]/div[1]/div/div'
                )))).get_attribute("data-monetate-producturl")
            if item1 not in products:
                rating_details = check_sus_rating(brand_names[0], item1,
                                                  driver)
                if rating_details['sus_rating'] == True:
                    products.add(item1)
            if len(products) == 2:
                max_reached_pata = True
                break
            driver.get(pata_base_url + query_list[query_index])
            item2 = (WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    '//*[@id="product-search-results"]/div[2]/div/div/div[2]/div[2]/div/div'
                )))).get_attribute("data-monetate-producturl")
            if item2 not in products:
                rating_details = check_sus_rating(brand_names[0], item2,
                                                  driver)
                if rating_details['sus_rating'] == True:
                    products.add(item2)
        except:
            print("nothing found")

        length = len(products)
        if length >= 2:
            max_reached_pata = True
        else:
            query_index += 1

    driver.quit()
    products_list = list(products)
    for product in products_list:
        product_data = scrape_for_alternatives(brand_names[0], product)
        product_data["url"] = product
        alt_data.append(product_data)

    driver = scrape_setup()
    query_index = 0
    products = set()
    while not max_reached_adidas and query_index < 3:
        driver.get(adidas_base_url + query_list[query_index])
        try:
            try:
                WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        '//*[@id="app"]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[2]/a/span'
                    )))
                item1 = (WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        '//*[@id="app"]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div/div/div/div[1]/a'
                    )))).get_attribute("href")
                if item1 not in products:
                    rating_details = check_sus_rating(brand_names[1], item1,
                                                      driver)
                    if rating_details['sus_rating'] == True:
                        products.add(item1)
                if len(products) == 2:
                    max_reached_adidas = True
                    break
                driver.get(adidas_base_url + query_list[query_index])
                item2 = (WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        '//*[@id="app"]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div/div/div/div/div/div[1]/a'
                    )))).get_attribute("href")
                if item2 not in products:
                    rating_details = check_sus_rating(brand_names[1], item2,
                                                      driver)
                    if rating_details['sus_rating'] == True:
                        products.add(item2)
            except:
                WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        '//*[@id="app"]/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/h1'
                    )))
                item1 = driver.current_url
                if item1 not in products:
                    rating_details = check_sus_rating(brand_names[1], item1,
                                                      driver)
                    if rating_details['sus_rating'] == True:
                        products.add(item1)
        except:
            print("nothing found")

        length = len(products)
        if length >= 2:
            max_reached_adidas = True
        else:
            query_index += 1

    products_list = list(products)
    for product in products_list:
        product_data = scrape_for_alternatives(brand_names[1], product)
        product_data["url"] = product
        alt_data.append(product_data)

    driver.quit()
    return alt_data


def get_query_list(brand, product_url):
    clothing = [
        'shirt', 'dress', 'pants', 'shorts', 'jeans', 'sweater', 'romper',
        'jeggings', 'jacket', 'top', 'jumpsuit', 'socks', 'skort', 'skirt',
        'joggers', 'sweatshirt', 'blazer', 'mask', 'boots', 'sandals', 'shoes'
    ]

    product_object = scrape_for_alternatives(brand, product_url)
    product_name_blob = TextBlob(product_object['product_name'].lower())
    phrases = product_name_blob.noun_phrases
    full_product_phrase = ''
    noun = ''
    if len(phrases) > 1:
        for phrase in phrases:
            if any(item in phrase for item in clothing):
                full_product_phrase = phrase
    if not full_product_phrase:
        full_product_phrase = max(phrases, key=len)

    for word in full_product_phrase.split()[-2:]:
        for word_pair in product_name_blob.tags:
            if word_pair[1][:2] == 'NN' and word_pair[0] == word:
                noun = word
    if full_product_phrase.split()[-1] == 'socks':
        noun = full_product_phrase.split()[-1]
    if not noun:
        noun = full_product_phrase.split()[1]
    query1 = " ".join([
        product_object['product_color'],
        " ".join(full_product_phrase.split()[-2:])
    ])
    query2 = " ".join(full_product_phrase.split()[-2:])
    query_list = [query1, query2, noun]
    return query_list, product_object['product_name']


def filter_alt_list(alt_data, orig_product_title):
    # for filtering the alternative list when it is size > 2
    match_score = []
    final_alt_list = []

    for alternative in alt_data:
        match_score.append(
            fuzz.token_set_ratio(alternative['product_name'],
                                 orig_product_title))
    # finds max
    max_score = max(match_score)
    final_alt_list.append(alt_data[match_score.index(max_score)])
    # removes from original list
    match_score.remove(max_score)
    alt_data.remove(final_alt_list[0])
    # finds 2nd max
    max_score = max(match_score)
    final_alt_list.append(alt_data[match_score.index(max_score)])

    return final_alt_list