from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import json
import time
import random

# URL сайта
url = "https://news.mail.ru/"

# Список User-Agent'ов
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    # Добавьте другие User-Agent'ы при необходимости
]

# Настройка Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск браузера в фоновом режиме
options.add_argument(f'user-agent={random.choice(user_agents)}')

driver = webdriver.Chrome(options=options)

# Функция для загрузки страницы с повторными попытками
def load_page(url, retries=3, wait_time=10):
    for attempt in range(retries):
        try:
            driver.get(url)
            # Ожидание загрузки основного контента
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.newsitem__title')))
            return True
        except (TimeoutException, WebDriverException) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(wait_time)
    return False

try:
    # Попытка загрузки страницы
    if not load_page(url):
        raise Exception("Failed to load page after multiple attempts")

    # Получение HTML страницы
    html = driver.page_source

    # Парсинг HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('a.newsitem__title')

    # Извлечение заголовков и ссылок
    news_data = []
    for article in articles:
        title = article.get_text(strip=True)
        link = article['href']
        news_data.append({'title': title, 'link': link})

    # Сохранение данных в формате JSON
    with open('news_mail_ru.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Закрытие браузера
    driver.quit()

# Пример содержимого JSON файла
if 'news_data' in locals():
    print(news_data)
else:
    print("No data extracted.")
