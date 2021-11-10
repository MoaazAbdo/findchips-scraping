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
        with open("E:\python//blocked.csv","w", encoding="UTF-8", newline='') as myFile:
            wr = csv.writer(myFile)
            wr.writerow(["PartNumber"])
            wr.writerows(parts_input[indx2])

        driver.quit()    

        
        
        
        
        
        
        
        
        
        
        
import hashlib
import os
import re
import signal
from multiprocessing.pool import ThreadPool
import psutil
from colorama import Fore
from seleniumwire.webdriver import Chrome
from seleniumwire.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from fake_headers import Headers
import time
from lxml import html
from pymongo import MongoClient
import datetime
import multiprocessing
from selenium.webdriver.support.ui import WebDriverWait
from googletrans import Translator
#-------- Read Tool Configuration File ---------#
try :
    # Glbl_Vrbls = pd.read_excel('Farnell_Configuration.xlsx', sep='\t')
    Glbl_Vrbls = pd.read_excel(r'E:\Production\Farnell_Newark\Farnell_Configuration.xlsx' , sep = '\t')
    DownloadThreads = Glbl_Vrbls.iloc[0][1]
    ExtractionThreads = Glbl_Vrbls.iloc[1][1]
    chromedriver = Glbl_Vrbls.iloc[2][1]
    Proxy_Activation = Glbl_Vrbls.iloc[3][1]
    Proxy_Number = Glbl_Vrbls.iloc[4][1]
except Exception as Conn_file_err:
    print(Fore.RED , "Error during reading Configuration File : {}".format(Conn_file_err) , Fore.RESET)
Input_file_Path = r'Input.txt'
counter = 0
#---- Test Coll -----#
# uri = "mongodb://192.168.7.60:27017"
# client = MongoClient(uri)
# db = client.TreeSearch
# Out_collection = db.Test
# Input_Collection = db.Input_Test
#------- Production Coll ---------#
uri = "mongodb://192.168.7.93:27017"
client = MongoClient(uri)
db = client.Aggregator
Out_collection = db.Farnell_Output
Input_Collection = db.Farnell_Input
RawDataColl = db.ExtractedPartsTest
#----------------------- Reading Manual input file -------------------------#
def Manual_input():
    inputfile = ""
    try:
        #----- Text File -------#
        if '.txt' in Input_file_Path:
            inputfile = pd.read_csv(Input_file_Path, sep='\t',skip_blank_lines=True,error_bad_lines=False).values
        #----- Excel File ------#
        # elif '.xlsx' in Input_file_Path:
        #     inputfile = pd.read_excel(Input_file_Path)
    except Exception as in_file_err:
        print(Fore.RED, "Error during Reading input file : {}".format(in_file_err), Fore.RESET)
    links = [list(x)[0] for x in inputfile]
    return links
def Get_Mongo_Input():
    try:
        Filter = {"ProxyIP": {'$in': [Proxy_Number]}, "Status": {'$in': ['1' , '4']}}
        URLs = []
        Queue_List = list(Input_Collection.find(Filter , {'Partial': 1, '_id': 1}))
        Queue_List_Count = Queue_List.__len__()
        print("#------------ There are ({}) pending URLs ------------#".format(Queue_List_Count))
        if Queue_List_Count != 0:
            for Input_Arg in Queue_List:
                try:
                    link = Input_Arg['Partial']
                    URLs.append(link)
                except Exception as ex:
                    print(ex)
    except Exception as Err:
        print(Fore.RED , "Error during getting Input : {}".format(Err), Fore.RESET)
    return URLs
#----------generate Fake Header for request------------#
def Fake_Request_Header():
    try:
        header = Headers(
            browser="chrome",  # Generate only Chrome UA
            os="win",  # Generate ony Windows platform
            headers=True  # generate misc headers
        )
        r_Headers = header.generate()
    except Exception as Error:
        print(Error)
        r_Headers = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'}
    return r_Headers
#---------------- Function to check if page loaded completely or not --------------#
def wait_loading(Loading_time = 10):
    # print("#-------- Wait Loading ---------#")
    # wait_time = 0
    # try:
    #     # Java_ready = driver.execute_script("return document.readyState")
    #     Content_before = driver.page_source
    #     # while Java_ready not in ready_itms and jQuery_ready != 0 and animation == 0 and processing != 0 and wait_time < Loading_time:
    #     while str(Content_before) == str(driver.page_source) and wait_time < Loading_time:
    #         wait_time += 1
    #         time.sleep(1)
    # except Exception as wait_err:
    # print(Fore.RED, "Error during Wait page finish load : {}".format(wait_err), Fore.RESET)
    #------------------ Waiting Ajax to finish -------------------#
    wait = WebDriverWait(driver, Loading_time)
    try:
        # wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass
#-----------Selenium driver Connection-------------#
def Open_driver():
    try:
        webdriver_options = ChromeOptions()
        # set_seleniumwire_options = {'disable_encoding': True,
        #                             # 'verify_ssl': True,  # Verify SSL certificates but beware of errors with self-signed certificates
        #                             'proxy': {
        #                                 'http': 'http://{}'.format("5.79.73.131:13150"),
        #                                 'https': 'https://{}'.format("5.79.73.131:13150"),
        #                                 'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
        #                             }
        #                             }
        webdriver_options.add_extension(r"E:\Production\Farnell_Newark\proxy.zip")
        webdriver_options.add_argument("--log-level=3")
        webdriver_options.add_argument('--disable-gpu')
        webdriver_options.add_argument('--no-sandbox')
        profile = {"browser.cache.disk.enable": False,
                   "browser.cache.memory.enable": False,
                   "browser.cache.offline.enable": False,
                   "network.http.use-cache": False}
        webdriver_options.add_experimental_option("prefs", profile)
        # webdriver_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        # webdriver_options.add_argument('--headless')
        # os.environ["webdriver.chrome.driver"] = r"E:\Webdrivers\chromedriver.exe"
        global driver
        driver = Chrome(executable_path=chromedriver , options=webdriver_options)
        driver.minimize_window()
        driver.set_page_load_timeout(120)
        # driver.set_window_position(-10000, 0)
    except Exception as driver_err:
        print(Fore.RED, "Error during opening driver : {}".format(driver_err), Fore.RESET)
def Get_Status_Code():
    StatusCode = 502
    Error = None
    try:
        serverissue = check_exists_by_xpath('//html/body/h1')
        if serverissue == True:
            StatusCode = 502
            Error = StatusCode
            wait_loading()
        # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sProdList"]/tbody/tr')))
        #--------------- Check Wrong Page --------------------#
        WrongPage = check_exists_by_xpath('//div[@class="categoryContainer"]')
        if WrongPage == True:
            StatusCode = 301
            Error = "Wrong Page"
        page = check_exists_by_xpath('//*[@id="sProdList"]/tbody/tr')
        if page == True:
            StatusCode = 200
    except Exception as err:
        Error = "Error during getting Status Code : {}".format(err)
    return (StatusCode,Error)
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
#------------- Download Function to get HTML_Source and save Local -----------#
def Get_Content(URL):
    # print("#.............................. Opening URL ...................................#")
    # print("SourceURL : {}".format(URL))
    HTML_Content = None
    Status_Code = 0
    Error = None
    try:
        Fake_Header = Fake_Request_Header()
        driver._client.set_header_overrides(headers=Fake_Header)
        driver.get(URL)
        wait_loading()
        #------ check Reload -------#
        if 'Reload' in driver.page_source:
            driver.refresh()
            wait_loading()
        Status_Code,Error = Get_Status_Code()
        #------ wait driver to load all javascript Content -------#
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.xpath, '//*[@id="sProdList"]/tbody/tr')))
        # time.sleep(0.5)
        # Status_Code = Get_Status_Code(Content)
        if Status_Code == 200:
            HTML_Content = driver.page_source
    except Exception as err:
        Error = "Error during getting HTML Content : {}".format(str(err).replace('\n', ''))
        print(Fore.RED , Error , Fore.RESET)
    return (Status_Code , HTML_Content , Error)
def Mongo_RawData_Insert(Doc,Filter):
    try:
        RawDataColl.update(Filter,Doc,upsert=True)
    except Exception as err:
        print(Fore.RED , "Error during Inserting Document to RawData : {}".format(err) , Fore.RESET)
def Mongo_Insert(Doc , Filter):
    try:
        # count = Out_collection.count(Filter)
        # if count !=0:
        Out_collection.update(Filter,Doc,upsert=True)
        # else:
        #     Out_collection.insert_one(Doc)
    except Exception as err:
        print(Fore.RED , "Error during Inserting Document to Mongo : {}".format(err) , Fore.RESET)
def Update_Input_Collection(Filter ,Status_Doc):
    try:
        # Mongo_Doc_count = Input_Collection.count(Filter)
        # if Mongo_Doc_count != 0:
        Input_Collection.update(Filter,Status_Doc,upsert=True)
        # Input_Collection.insert_one(Status_Doc)
    except Exception as Error:
        Mongo_Error = "Error during Inserting Document to Part_Search Results Collection : {}".format(Error)
        print(Mongo_Error)
def translate(text):
    new_word = text
    try:
        translator = Translator()
        translation = translator.translate(text , dest='en')
        new_word = translation.text
        # gs = goslate.Goslate()
        # new_word = gs.translate(text, 'de')
        # translator= Translator(from_lang="german",to_lang="english")
        # new_word = translator.translate(text)
    except Exception as tr_err:
        translate = None
        # print(Fore.RED , "Error during translate : {}".format(text), Fore.RESET)
        # print(Fore.RED, tr_err, Fore.RESET)
    return new_word
def text(elt):
    try:
        return elt.text_content().strip().replace(u'\xa0', u' ').replace("\n" , "")
    except:
        return elt.text.strip().replace(u'\xa0', u' ').replace("\n" , "")
def GetHashCode(pricesListFinal,partNumber,mfr,stock,sku,packaging):
    ###########################HashCode####################################
    try:
        pricesListFinal = sorted(pricesListFinal, key=lambda i: i['priceBreak'])
        hashstring = 'Farnell' + partNumber + mfr + str(stock) + str(sku) + str(packaging)
        hashstringNew = 'Farnell' + partNumber + mfr + str(stock) + str(sku)
        for item in pricesListFinal:
            hashstring += ',' + str(item['priceBreak']) + str(item['price'])
            hashstringNew += ',' + str(item['priceBreak']) + str(item['price'])
            index = pricesListFinal.index(item)
            pricesListFinal[index] = {'priceBreak': item['priceBreak'],
                                      'price': item['price']}
        hashstringencod = hashstring.encode()
        hashstringencodNew = hashstringNew.encode()
        hash512 = hashlib.sha512(hashstringencod).hexdigest()
        hash512New = hashlib.sha512(hashstringencodNew).hexdigest()
    except Exception as Err:
        print("Error during Hashing : {}".format(Err))
    return hash512New
def Extract_Raw(Entry):
    indx , url , Html_page  = Entry
    All_Raws_xpath = '//*[@id="sProdList"]/tbody/tr'
    PartNumber = ''
    PartNumber_URL = ''
    SKU = ''
    Datasheet = ''
    LC_Status = ''
    ROHS = ''
    MFR = ''
    Description = ''
    Stock = 0
    StockFlag = ''
    Packaging = ''
    Raw_Status=''
    All_Price_breaks = []
    MOQ = 0
    try:
        try:
            PartNumber = text(Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '/td[@class="productImage mftrPart"]/a')[0])
            PartNumber_URL = Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '/td[@class="productImage mftrPart"]/a')[0].xpath('self::*//@href')[0]
        except Exception as prt_err:
            print("PartNumber Data notfound in Raw {} : {}".format(indx, prt_err))
        if PartNumber !='':
            # ------------- Extract SKU --------------#
            try:
                SKU = text(Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '//p[@class="sku"]')[0])
            except Exception as sku_err:
                print("SKU notfound in Raw {} : {}".format(indx, sku_err))
            # -------------- Extract Datasheet ---------------#
            try:
                Datasheet_lst = Html_page.xpath(All_Raws_xpath + '[{}]'.format(
                    indx) + '/td/div[@class="attachmentIcons"]/a[@data-dtm-eventinfo="Data Sheet"]')
                if len(Datasheet_lst) != 0:
                    Datasheet = Datasheet_lst[0].xpath('self::*//@href')[0]
            except Exception as dsht_err:
                print("Datasheet notfound in Raw {} : {}".format(indx, dsht_err))
            # ------------- Extract_LC_Status -------------#
            try:
                LC_Status_lst = Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '/td/div[@class="attachmentIcons"]/div[@class="attachmentText"]')
                if len(LC_Status_lst) != 0:
                    LC_Status = translate(text(LC_Status_lst[0]))
            except Exception as lc_err:
                print("LC_Status notfound in Raw {} : {}".format(indx, lc_err))
            # ------------- Extract_ROHS -------------#
            try:
                ROHS_lst = Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '/td/div[@class="attachmentIcons"]/a[@data-dtm-eventinfo="RoHS"]')
                if len(ROHS_lst) != 0:
                    ROHS = ROHS_lst[0].xpath('self::*//@href')[0]
            except Exception as rhs_err:
                print("ROHS Data notfound in Raw {} : {}".format(indx, rhs_err))
            # ------------- Extract MFR & Description -------------#
            try:
                MFR = text(Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '//td[@class="description enhanceDescClmn"]/p[@class="manufacturerName"]')[0])
                Description = translate(text(Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '//td[@class="description enhanceDescClmn"]/a')[0]))
            except Exception as mfr_err:
                print("MFR & Description Data notfound in Raw {} : {}".format(indx, mfr_err))
            # -------------- Stock and StockFlag -----------------#
            try:
                StockArea = Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '//td[@class="availability"]/div/span/a/p')
                if len(StockArea) != 0:
                    try:
                        Stock = int(''.join([letter for letter in text(StockArea[0]) if letter in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]))
                    except:
                        Stock = 0
                    try:
                        StockFlag = translate(''.join([letter for letter in text(StockArea[0]) if letter not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]))
                    except:
                        StockFlag = translate(text(StockArea[0]))
                else:
                    StockFlag = translate(text(Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '/td[@class="availability"]/div/span/a/p')[0]))
            except Exception as stck_err:
                Stock = 0
            # -------------- OnOrder -----------------#
            try:
                OnOrderArea = Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '//td[@class="availability"]/div/span/p')
                if len(OnOrderArea) != 0:
                    try:
                        OnOrder=translate(OnOrderArea[0].text.strip().replace(u'\xa0', u' ').replace("\n", "").replace("\t", " "))
                    except:
                        OnOrder = ''
                else:
                    OnOrder = ''
            except Exception as stck_err:
                OnOrder = ''
            # --------------- Packaging ----------------#
            try:
                Packaging = translate(text(Html_page.xpath(All_Raws_xpath + '[{}]'.format(indx) + '//td[@class="listPrice enhanceListPrice"]/p')[0]))
            except Exception as pckg_err:
                print("Packaging notFound in Raw {} : {}".format(indx, pckg_err))
            # ------------------- Breaks -------------------#
            try:
                PriceperBreaks_lst = Html_page.xpath(
                    All_Raws_xpath + '[{}]'.format(indx) + '//td[@class="listPrice enhanceQtyColumn"]/div/p/span')
                All_Price_breaks = []
                for p in PriceperBreaks_lst:
                    pricebreak = None
                    price = None
                    pricebreak = int(text(p[0]).replace("+", ""))
                    pricestring = text(p[1]).replace(' €', '').replace('$', '')
                    if ',' in pricestring and '.' in pricestring:
                        price = float(pricestring.replace(',',''))
                    else:
                        price = float(pricestring.replace(',','.').replace('$', ''))
                    price_doc = {"priceBreak": pricebreak,
                                 "price": price}
                    All_Price_breaks.append(price_doc)
            except Exception as Brks_err:
                print("priceBreaks notFound in Raw {} : {}".format(indx, Brks_err))
            #--------------- moq ---------------#
            try:
                multqty_Area = Html_page.xpath(
                    All_Raws_xpath + '[{}]'.format(indx) + '/td[@class="qty"]/div/span[2]/span/div[@class="multqty"]/span')
                if len(multqty_Area) != 0:
                    i = 0
                    for area in multqty_Area:
                        if text(area) == 'Min:':
                            MOQ = int(text(multqty_Area[i + 1]))
                        i += 1
            except Exception as moq_err:
                print("MOQ notFound in Raw {} : {}".format(indx, moq_err))
            #--------------------- Hashing ----------------------#
            HashCode = GetHashCode(All_Price_breaks,PartNumber,MFR,Stock,SKU,Packaging)
            Raw_Status = 'Done'
            try:
                # ------------------ Prepare Document ---------------------#
                Filter = {"partNumber": PartNumber, "packagingName": Packaging}
                Doc = {"extractionDate": datetime.datetime.now(),
                       "SourceName": "Farnell", "partNumber": PartNumber,
                       "partNumber_URL": PartNumber_URL,
                       "packagingName": Packaging, "mfr": MFR, "stock": Stock,
                       "StockFlag": StockFlag,"OnOrder":OnOrder,
                       "SourceURL": url, "sku": SKU, 'moq': MOQ,
                       'Aggregator': "Farnell",
                       "distributorType": "true",
                       'hashcode': HashCode,
                       "Description": Description, "Currency": "€",
                       "DataSheet": Datasheet,
                       'ROHS': ROHS,
                       'LC_Status': LC_Status,
                       "pricesPerBreaks": {'originalCurrency': 'EUR',
                                           'currencyRation': 1,
                                           'pricesList': All_Price_breaks},
                       "part_Status": None}
                RawDataFilter = {"SourceName": "Farnell", "partNumber": PartNumber, "sku": SKU,
                                         'mfr': MFR, 'stock': Stock}
                RawDataDoc = {
                       "extractionDate": datetime.datetime.now(),
                       "SourceName": "Farnell", "partNumber": PartNumber,
                       "packagingName": Packaging, "mfr": MFR, "stock": Stock,
                       "StockFlag": StockFlag,
                       "SourceURL": url, "sku": SKU, 'moq': MOQ,
                       'Aggregator': "Farnell",
                       "distributorType": "true",
                       'hashcode': HashCode,
                       "Description": Description, "Currency": "€",
                       "DataSheet": Datasheet,
                       "pricesPerBreaks": {'originalCurrency': 'EUR',
                                           'currencyRation': 1,
                                           'pricesList': All_Price_breaks},
                       "part_Status": None,
                       "ImporterFlag": 1
                }
                # ------------ Update Document to Resuts Collection -------------#
                if Raw_Status == 'Done' and PartNumber!='':
                    Mongo_Insert(Doc, Filter)
                    # Mongo_RawData_Insert(RawDataDoc , RawDataFilter)
            except Exception as mngo_err:
                print(Fore.RED , "Error during update result in Mongo : {}".format(mngo_err) , Fore.RESET)
    except Exception as Raw_err:
        print(Fore.RED, "Error in Raw {} : {}".format(indx, Raw_err), Fore.RESET)
    return Raw_Status
def Extraction(HTML_Content , url):
    # print("#---Start_Extraction---#")
    Error = None
    All_Raws = []
    Extraction_Status = '4'
    All_Raws_Status = []
    try:
        Html_page = html.fromstring(HTML_Content)
        All_Raws_xpath = '//*[@id="sProdList"]/tbody/tr'
        All_Raws = Html_page.xpath(All_Raws_xpath)
    except Exception as Ex_Err:
        Extraction_Status = '4'
        Error = "Error during Extraction : {}".format(Ex_Err)
        print(Fore.RED, Error, Fore.RESET)
    Raws_Count = len(All_Raws)
    if Raws_Count != 0:
        #------------- prepare all Input for threading ----------------#
        try:
            All_Extract_in = []
            indx = 1
            for filed in All_Raws:  # Loop range according to no of input file raws
                P = (indx , url , Html_page)
                All_Extract_in.append(P)
                indx = indx + 1
        except Exception as er:
            Error = "Error during preparing Raw Extract input : {}".format(er)
            print(Fore.RED , Error , Fore.RESET)
        try:
            results = ThreadPool(ExtractionThreads).imap_unordered(Extract_Raw, All_Extract_in)
            for Raw_status in results:
                if Raw_status != None:
                    All_Raws_Status.append(Raw_status)
        except Exception as thrd_err:
            Error = "Error during Extraction Threading : {}".format(thrd_err)
            print(Fore.RED, Error, Fore.RESET)
            Extraction_Status = '4'
    if 'Done' in All_Raws_Status:
        Extraction_Status = '3'
    return (Extraction_Status,Error)
    #--------------- Get No of Next Pages ------------------#
    # if Flag == 'Main_URL':
    #     try:
    #         Next_Pages_Range = len(Html_page.xpath('//*[@id="paraSearch"]/div[4]/div/div[1]/nav/span[2]/span'))
    #     except Exception as err:
    #         print("Error during getting Next Pages Range : {}".format(err))
    # return Next_Pages_Range
def selenium(url):
    global counter
    counter = counter + 1
    # print("#---------------------------- Running on URL : {} ------------------------------#".format(counter*int(DownloadThreads)))
    Last_Run_Date = datetime.datetime.now()
    Error = None
    Extraction_Status = '4'
    Status_Code = 502
    (Status_Code,HTML_Content,Error) = Get_Content(url)
    if Status_Code == 200:
        Extraction_Status,Error = Extraction(HTML_Content, url)
    # else:
    #     print(Fore.RED ,"Status Code : {}".format(Status_Code) , Fore.RESET)
    if Extraction_Status == '3' :
        print(datetime.datetime.now() , Fore.GREEN, "Extraction_Status : ", Extraction_Status, Fore.RESET)
    else:
        print(datetime.datetime.now(), Fore.RED, "Extraction_Status : ", Extraction_Status, Fore.RESET)
    Filter = {'Partial' : url}
    Status_Doc = {'Partial':url,'Status':Extraction_Status,'Exception':Error,'ProxyIP':Proxy_Number , 'Last_Run_Date':Last_Run_Date}
    Update_Input_Collection(Filter ,Status_Doc)
    # ---------------- Pagination -----------------#
    # if Next_Pages_Range !=0 or Next_Pages_Range != None:
    #     for x in range(Next_Pages_Range):
    #         if x not in [0,1]:
    #             Next_URL = url+'/{}'.format(x)
    #             try:
    #                 print("#----- Click Next Page -----#")
    #                 # driver.find_element_by_xpath('//span[@class="paginNextArrow"]').click()
    #                 # next_url = driver.current_url
    #                 selenium(Next_URL , Flag = 'Next_URL')
    #             except Exception as nxt_err:
    #                 print("#------- Next Finished ----------#")
def Close_driver():
    try:
        driver.quit()
    except Exception as drvr_err:
        print("#-------- Kill driver with pid--------#")
        Parent_pid = driver.service.process.pid
        driver_process = psutil.Process(Parent_pid)
        Subprocesses = driver_process.children(recursive=True)
        try:
            os.kill(int(Subprocesses[0].pid), signal.SIGTERM)
        except Exception as err:
            kill = 'NotDone'
        try:
            os.kill(int(Parent_pid), signal.SIGTERM)
        except Exception as eerr:
            kill = 'NotDone'
    time.sleep(.5)
def Start_Run(Input):
    links = Input
    indx = 1
    for url in links:
        time.sleep(2)
        try:
            Open_driver()
            selenium(url)
            Close_driver()
        except Exception as Err:
            print(Fore.RED ,"Error in Download Function : {}".format(Err) , Fore.RESET)
        indx += 1
def main():
    # Delete_Temp()
    while(1):
        # links = Manual_input()
        links = Get_Mongo_Input()
        # links = ['https://de.farnell.com/c/burobedarf-computer-netzwerk-produkte/prl/ergebnisse/33']
        # links = ['https://de.farnell.com/search?st=bav99']
        # links = ['https://de.farnell.com/w/c/gleichrichter-transistoren-thyristoren-dioden/dioden/kleinsignaldioden/prl/ergebnisse/9?st=bav']
        # links = ['https://de.farnell.com/c/embedded-computers-education-maker-boards/arduino/embedded-development-kits-arduino/prl/results/1']
        Input_Count = len(links)
        try:
            if Input_Count < DownloadThreads:
                Threads_Num = 1
                Batches_Inpt = [links[x:x + int(Input_Count / Threads_Num)] for x in
                                range(0, len(links), int(Input_Count / Threads_Num))]
            else:
                Threads_Num = DownloadThreads
                Batches_Inpt = [links[x:x + int(Input_Count / Threads_Num)] for x in
                                range(0, len(links), int(Input_Count / Threads_Num))]
        except Exception as Batches_err:
            print(Fore.RED, "Error during dividing Input to Batches input : {}".format(Batches_err), Fore.RESET)
        #--------------------- Pass Threads to Engine ------------------------#
        try:
            # --------------- Go with One Thread to Start Running ----------------#
            procs = []
            for Thrd_indx, One_Thread_links in zip(range(Threads_Num), Batches_Inpt):
                # One_Thread_Input = (Thrd_indx, One_Thread_links)
                Thrd = multiprocessing.Process(target=Start_Run, args=(One_Thread_links,))
                Thrd.start()
                procs.append(Thrd)
            multiprocessing.active_children()        #--------------------- Like await ------------------------#
            for process in procs:
                process.join()
            # ------------- Kill Chromdrivers and chromeBrowser -------------#
        except Exception as Sys_err:
            print(Fore.RED, "Error in Manual Engine : {}".format(Sys_err), Fore.RESET)
        print("#------------------ All URLs Done --------------------#")
if __name__ == '__main__': main()
    
    
