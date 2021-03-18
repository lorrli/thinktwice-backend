from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob
from scrape_product import scrape_for_alternatives


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

def get_query_list(brand, product_url): 
    clothing = ['shirt', 'dress', 'pants', 'shorts', 'jeans', 'sweater', 'romper', 'jeggings', 'jacket', 'top',
                'jumpsuit', 'socks', 'skort', 'skirt', 'joggers', 'sweatshirt', 'blazer', 'mask', 'boots', 'sandals', 'shoes']

    alt_object = scrape_for_alternatives(brand, product_url)
    product_name_blob = TextBlob(alt_object['product_name'].lower())
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
    query1 = " ".join([alt_object['product_color'], " ".join(full_product_phrase.split()[-2:])])
    query2 = " ".join(full_product_phrase.split()[-2:])
    query_list = [query1, query2, noun]
    return query_list


