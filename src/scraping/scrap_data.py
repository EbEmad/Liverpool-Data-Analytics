from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import service
from webdriver_manager.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from io import StringIO
import pandas as pd

def scrape_tables(url,club,xpath='',slepp_time=10):

    # set up chrome
    options=Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    # set up the chrome driver
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)

    # wait ofr the page to load
    time.sleep(slepp_time)

    try:
        if club=='Liverpool':
            soup=BeautifulSoup(driver.page_source)
            df=pd.read_html(StringIO(str(soup)))
        else:
            table_element=driver.find_element(By.XPATH,xpath)
            table_html=table_element.get_attribute('outerHTML')
            df=pd.read_html(StringIO(table_html))[0]
            return df
    except Exception as e:
        return f"Error while Scraping: {e}"
    driver.quit()
    
        


