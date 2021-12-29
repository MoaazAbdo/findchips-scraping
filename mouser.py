from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


PATH = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(PATH)

def get_source(url):
    driver.get(f"{url}")
    try:
        element = WebDriverWait(driver, 60).until(
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
    try:
        mfr_pn = rows[i].find("div", {"class": "mfr-part-num"}).a.text.strip()
        print(mfr_pn)
    except:
        mfr_pn = "No MFR Part"

    try:
        mfr = rows[i].find("td",{"class": "mfr-column"}).a.text.strip()
        print("mfr = ", mfr)
    except:
        mfr = "NO MFR"

    try:
        datasheet = rows[i].find("td", {"class": "column hide-xsmall"}).find("a", {"class": "text-nowrap"}).get['href']
        print("datasheet =", datasheet)
    except:
        datasheet = "No DataSheet"
    # print(rows[i].find("div",{"class": "mfr-part-num"}).a.text.strip())