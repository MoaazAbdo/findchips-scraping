from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
from itertools import zip_longest
from selenium.webdriver import ActionChains
import xlrd
from xlrd import sheet



loc = input("please exnter path of excel sheet contain parts you want to scrap: ")
web = xlrd.open_workbook(loc)
sheet = web.sheet_by_index(0)
parts_input = []
for i in range(sheet.nrows):
    parts_input.append(sheet.cell_value(i,0))   

#print(parts_input)

distributors = []
parts        = []
skus         = []
mfrs         = []
stocks       = []
descritions  = []
urls         = []
prices       = [] 



for indx2 in range(len(parts_input)):

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    driver.get(f'https://www.findchips.com/search/{parts_input[indx2]}?currency=USD')
    #driver.get('https://www.findchips.com/search/moaaz?currency=USD')


    try:
        page = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'page'))
        )
        
        try:
            page.find_element_by_xpath('//*[@id="page"]/p')
            distributors.append("notfound")
            parts.append(parts_input[indx2])
            skus.append("notfound")
            mfrs.append("notfound")
            stocks.append("notfound")
            urls.append("notfound")
            prices.append("notfound")
            descritions.append("notfound")
            
            driver.quit()
        except NoSuchElementException:

            data = page.find_elements_by_class_name("distributor-results")
                    
            for distributor in range(len(data)):
                
                distributorName = data[distributor].find_element_by_class_name("distributor-title")       
                rows = data[distributor].find_elements_by_class_name("row")
                
                for r in range(len(rows)):
                    try:
                        Pricing = rows[r].find_elements_by_link_text("See More")
                        for i in range(len(Pricing)):
                            Pricing[i].click()

                        descrition = rows[r].find_elements_by_link_text("more")
                        for x in range(len(descrition)):
                            descrition[x].click()

                    except NoSuchElementException:
                        print("no Price")

                    distributors.append(distributorName.text)
                    partNumber = rows[r].find_element_by_css_selector("div.part-name a").text
                    parts.append(partNumber)
                    try:
                        sku = rows[r].find_element_by_css_selector("div.part-name .additional-value").text
                        skus.append(sku)

                    except NoSuchElementException:
                        skus.append("No SKU Found")

                    mfr = rows[r].find_element_by_class_name("td-mfg").text
                    mfrs.append(mfr)

                    stock = rows[r].find_element_by_class_name("td-stock").text.replace("In Stock ","").replace(' "',"").replace('"',"").replace("\n","")
                    stocks.append(stock)
                               
                    price = rows[r].find_element_by_class_name("td-price")
                    if len(price.text) > 1:   
                        prices.append(price.text.replace("\n","|"))
                    else:
                        prices.append("No Price")
                    
                    desc = rows[r].find_element_by_class_name("td-desc").text
                    if len(desc) > 1:
                        descritions.append(desc.replace("\n",""))
                    else:
                        descritions.append("no description")

                    buynow = rows[r].find_element_by_class_name("td-buy")
                    url = buynow.find_element_by_tag_name("a").get_attribute("href")
                    urls.append(url)
                    

                    fileList = [parts,distributors, skus, mfrs,stocks,descritions,urls,prices]        
                    exported = zip_longest(*fileList)
                    
                    with open("E:\python//data.csv","w", encoding="UTF-8", newline='') as myFile:
                        wr = csv.writer(myFile)
                        wr.writerow(["PartNumber","Distributor", "Sku","MFR","Stock","Descrition","BuyNow","Pricing"])
                        wr.writerows(exported)

            driver.quit()
    except:
        print("Time Out")
        with open("E:\python//data.csv","w", encoding="UTF-8", newline='') as myFile:
            wr = csv.writer(myFile)
            wr.writerow(["PartNumber"])
            wr.writerows(parts_input[indx2])

        driver.quit()    

