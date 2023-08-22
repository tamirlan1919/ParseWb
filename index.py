from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import collections
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')

ParseResult = collections.namedtuple('ParseResult', ['brand_name', 'goods_name', 'url'])

class Client:
    def __init__(self):
        # Настройки для Chrome WebDriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Запустить браузер в фоновом режиме (без отображения окна)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.result = []

    def load_page(self, url):
        self.driver.get(url)
        page_content = self.driver.page_source
        return page_content

    def parse_page(self, text: str):
        self.result = []
        self.driver.get(text)  # Перейдите на страницу, используя переданный URL
        container = self.driver.find_elements(By.CSS_SELECTOR, 'div.product-card__wrapper')
        for block in container:
            print(block)
            self.parse_block(block=block)
        
        self.write_to_csv()


    def parse_block(self, block):
        url_block = self.driver.find_element(By.CSS_SELECTOR, 'a.product-card__link')
        #url = url_block.get_attribute('href')
        print('-------------------------------------',url_block)
        # name_block = block.find_element(By.CSS_SELECTOR, 'div.product-card__middle-wrap')
        # brand_name_element = name_block.find_element(By.CSS_SELECTOR, 'span.product-card__name')
        # brand_name = brand_name_element.text.strip().replace('/', ' ')

        # # Создаем кортеж с данными и добавляем его в список результатов
        # data = (brand_name, url)
        # self.result.append(data)



    def run(self, el):
        text = self.load_page(el)
        self.parse_page(text=text)

    def write_to_csv(self):
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Brand', 'URL'])  # Заголовки столбцов
            for data in self.result:
                csv_writer.writerow(data)

if __name__ == '__main__':
    elem = 'https://example.com'  # Замените на нужный URL
    parser = Client()
    parser.run(elem)
