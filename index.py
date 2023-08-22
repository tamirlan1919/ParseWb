import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()




def load_page(url):
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-card__wrapper')))
    page_content = driver.page_source
    return page_content

def parse_page(url):
    page_content = load_page(url)
    parse_blocks(page_content=page_content)

def parse_blocks(page_content):
    container = driver.find_elements(By.CSS_SELECTOR, 'div.product-card__wrapper')
    for block in container:
        brand_name = block.find_element(By.CSS_SELECTOR, 'span.product-card__name').text.strip().replace('/', ' ')
        product_url = block.find_element(By.CSS_SELECTOR, 'a.product-card__link').get_attribute('href')
        print(f'Brand Name: {brand_name}')
        print(f'Product URL: {product_url}')
        print('-' * 50)

def run(url):
    parse_page(url=url)
    driver.quit()

