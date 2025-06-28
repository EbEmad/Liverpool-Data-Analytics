from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO
def scrape_tables(url,club,xpath='',sleep_time=10):
    # set up chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--remote-debugging-port=9222')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(10)  # instead of default 120s
    driver.get(url)
    time.sleep(sleep_time)  # Wait for the page to load

    try:
        if club=='Liverpool':
            soup=BeautifulSoup(driver.page_source, 'html.parser')
            df=pd.read_html(StringIO(str(soup)))
            return df
        else:
            table_elemnt=driver.find_element(By.XPATH, xpath)
            table_html=table_elemnt.get_attribute('outerHTML')
            df=pd.read_html(StringIO(table_html))[0]
            return df
    except Exception as e:
        return f"Error while scraping: {e}"

    driver.quit()
    return df
        

