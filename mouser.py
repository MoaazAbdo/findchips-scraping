from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


PATH = "E:\chromedriver.exe"
driver= webdriver.Chrome(PATH)

def get_source(url):
    driver.get(f"{url}")
    try:
        element = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[1]/div[5]/div/form/div[2]/div[2]/table/tbody'))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    except:
        return "TimeOut"


page = get_source("https://www.mouser.com/c/?q=ABM3B-24.000M")
table = page.find("div",{"class": "scroll-body"}).find("table", {"id": "SearchResultsGrid_grid"}).tbody


rows = table.findAll("tr",{"class": ["", "even-row","last-row"]})


for i in range(len(rows)):
    print(rows[i].find("div",{"class": "mfr-part-num"}).a.text.strip())


