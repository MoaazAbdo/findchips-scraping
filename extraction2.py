import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import os, shutil
import xlrd
from xlrd import sheet

# Start Prepare Input
loc = input("Please enter path of your input file: ")
web = xlrd.open_workbook(loc)
sheet = web.sheet_by_index(0)
parts_input = []
for i in range(sheet.nrows):
    parts_input.append(sheet.cell_value(i,0))

print(parts_input)

# Start Declare Lists to store extracted data in

final_distributors      = []
parts                   = []
mfrs                    = []
stocks                  = []
buy                     = []
prices                  = []
searches                = []
distis                  = []
descriptions            = []
additional_descriptions = []




# start extract data through a list of input
for iterable in range(len(parts_input)):
    
    
    result = requests.get(f"https://www.findchips.com/search/{parts_input[iterable]}")
    
    src = result.content

    soup = BeautifulSoup(src, "lxml")


    found = soup.find("p", {"class": 'no-results'})
    if found:
        searchedPart = soup.find("h1", {"class": 'title'})
        searches.append(searchedPart.text.strip().replace(" price and stock", ""))
        buy.append("Part Not Found")
        final_distributors.append("Part Not Found")
        parts.append("Part Not Found")
        distis.append("Part Not Found")
        mfrs.append("Part Not Found")
        descriptions.append("Part Not Found")
        additional_descriptions.append("Part Not Found")
        stocks.append("Part Not Found")
        prices.append("Part Not Found")

    else:
        searchedPart = soup.find("h1", {"class": 'title'})
        distributor2 = soup.find_all("a", {"data-click-name": "part number"},onclick=True)
        part_number  = soup.find_all("td", {"class": "td-part"})
        mfr          = soup.find_all("td", {"class": "td-mfg"})
        description  = soup.find_all("td", {"class": "td-desc"})
        stock        = soup.find_all("td", {"class": "td-stock"})
        price_list   = soup.find_all("td", {"class":"td-price"})
        buynow       = soup.find_all("td", {"class": "td-buy"})
        disti        = soup.find_all("div", {"class": "part-name"})

        distributors            = []
        for i in distributor2:
            x = i.attrs['onclick'].replace("recordUserClick","").split(",")
            distributors.append(x[1])
        
    
        for x in range(len(distributors)):
            
            final_distributors.append(distributors[x].replace("'", "")[1:])
            parts.append(part_number[x].a.text.strip())
            mfrs.append(mfr[x].text.strip())
            stocks.append(stock[x].text.strip())
            price_content = ""
            price_content = price_list[x].text.strip()+" || "
            price_content = price_content[:-3]
            price_content = price_content.replace("\n", ",").replace("See More", "")
            price_content = price_content[:-1]
            prices.append(price_content)
            buy.append(buynow[x].a.attrs["href"])
            searches.append(searchedPart.text.strip().replace(" price and stock", ""))

            
            if disti[x].find("span", {"class": "additional-description"}):
                distis.append(disti[x].find("span", {"class": "additional-description"}).text.strip().replace("\n", ""))
            else:
                distis.append("Empty")
            
            if description[x].find("span", {"class": "td-description"}):
                
                main_description = description[x].find("span", {"class": "td-description"}).text.strip()
                descriptions.append(main_description)
                
                additional = description[x].find_all("span", {"class": "additional-description"})
                if additional == [] :
                    additional_descriptions.append("No Additional Description")
                    
                else:
                    additional_description = ""
                    for a in range(len(additional)):
                    
                        index = str(x)+additional[a].text[0]
                        
                        if x == int(index):
                        
                            additional_description += additional[a].text.replace("                    ", " ").strip().replace("\n","")+","
                    
                    additional_descriptions.append(additional_description)

                
                
            else:
                descriptions.append("No Description")
                additional_descriptions.append("No Additional Description")
    print(parts_input[iterable], "Done")


directory = "Results"
parent_dir = "D:\\findchips\\"
path = os.path.join(parent_dir, directory)
if os.path.exists(path) == False:
    os.mkdir(path)
else:
    shutil.rmtree(path)
    os.mkdir(path)


fileList = [searches, buy, final_distributors,parts, distis,mfrs, descriptions , additional_descriptions , stocks, prices]
exported = zip_longest(*fileList)

result = path+"//data.csv"

with open(result,"w", encoding="UTF-8", newline='') as myFile:
    wr = csv.writer(myFile)
    wr.writerow(["Searched","Buy Now", "distributors", "Part #", "DISTI #","MFR", "Description" , "Additional Description","Stock", "Price V1"])
    wr.writerows(exported)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
import datetime
import os
import re
from lxml import html
import string
import urllib.request
import bs4 as bs
import requests
from time import time as timer
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup
from pymongo import MongoClient, InsertOne, ReplaceOne, UpdateOne, UpdateMany
from itertools import cycle
import traceback
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bson.objectid import ObjectId
from decimal import Decimal
import hashlib
import re
from lxml import html
from bs4 import BeautifulSoup
import warnings
import time
from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
warnings.filterwarnings('ignore')
try:
    # Python 3.x
    from urllib.parse import quote_plus
except ImportError:
    # Python 2.x
    from urllib import quote_plus
# uri = "mongodb://%s:%s@%s" % (
#     quote_plus('userag'), quote_plus('Aggregator_325'), '192.168.7.45')
client = MongoClient('192.168.7.93')
db = client.Aggregator
collectionRawData = db.ExtractedParts
collectionMouserDK = db.DKPartial_105_Output
Aggregatorcollection = db.HighRunnersPartials
####################################################
# urimouser = "mongodb://%s:%s@%s" % (
#     quote_plus('inv1'), quote_plus('inv1321'), '192.168.7.45')
clientMouser = MongoClient('192.168.7.93')
dbMouser = clientMouser.INVHistory
collectionMouser = dbMouser.Mouser
collectionMouserPCN = dbMouser.Mouser_Pcn
Currency=[]
FinchipInputBulk = []
FinchipOutputBulk = []
RawDataBulk = []
class PriceList:
    def __init__(self, price, priceBreak):
        self.price = price
        self.priceBreak = priceBreak
from lxml.html import fromstring
def getCurrency(databasecurrency,price):
    try:
        if str(price).find('$')!=-1:
            price=str(price).replace('$','')
            ratio = Currency[databasecurrency]
            c = CurrencyCodes()
            symbol = c.get_symbol(databasecurrency)
            price = round((float(str(price).replace(',','')) ), 3)
        else:
            ratio = Currency[databasecurrency]
            c = CurrencyCodes()
            symbol = c.get_symbol(databasecurrency)
            price = str(price).replace(symbol, '')
            price = round((float(str(price).replace(',',''))),3)
        return price
    except Exception as ex:
        return 0
def ExtractFromTable(table, url):
    try:
        RealTable = table.find('table')
        if RealTable != None:
            distributorTypeTag = table.select_one('.other-disti-details')
            if distributorTypeTag != None:
                distributorTypeText = distributorTypeTag.text.strip()
                if distributorTypeText != '':
                    distributorType = 'true'
                    if table.select_one('h3').find('a') != None:
                        SellerNameWithSpan = table.select_one('h3').find('a').text.strip()
                        SellerNameSpan = table.select_one('h3').find('span').text.strip()
                        SellerName = str(SellerNameWithSpan).replace(SellerNameSpan, '').strip()
                        if SellerName == 'Digi-Key':
                            print(SellerName)
                            return;
                    else:
                        SellerNameWithSpan = table.select_one('h3').text.strip()
                        SellerNameSpan = table.select_one('h3').find('span').text.strip()
                        SellerName = str(SellerNameWithSpan).replace(SellerNameSpan, '').strip()
                        if SellerName == 'Digi-Key':
                            print(SellerName)
                            return;
                    PartRowListTag = RealTable.select_one('tbody').select('.row')
                    print('===========================================================')
                    if PartRowListTag != None:
                        for Row in PartRowListTag:
                            pricesListFinal = []
                            partNumber = Row.select_one('.td-part').select_one('a').text.strip()
                            prices = Row.select_one('.td-price')
                            if prices != None:
                                pricesUlList = prices.select('ul')
                                if len(pricesUlList) != 0:
                                    pricesilList = prices.select('li')
                                    if len(pricesilList) != 0:
                                        for il in pricesilList:
                                            if (il.select_one('.label')) != None:
                                                priceBreak = il.select_one('.label').text.strip()
                                                databasecurrency = il.select_one('.value').attrs['data-basecurrency']
                                                priceStr = il.select_one('.value').text.strip()
                                                if priceBreak != '':
                                                    if databasecurrency != 'USD':
                                                        price = getCurrency(databasecurrency, priceStr)
                                                        # print(
                                                        #     'Price= ' + str(price) + '     ' + 'priceBreak= ' + priceBreak)
                                                        pricesList = {"priceBreak": int(priceBreak.replace(',', '')),
                                                                      "price": price}
                                                        pricesListFinal.append(pricesList)
                                                    else:
                                                        price = str(priceStr).replace('$', '')
                                                        # print(
                                                        #     'Price= ' + str(round(float(price),3)) + '     ' + 'priceBreak= ' + priceBreak)
                                                        pricesList = {
                                                            "priceBreak": int(str(priceBreak).replace(',', '')),
                                                            "price": round(float(str(price).replace(',', '')), 3)}
                                                        pricesListFinal.append(pricesList)
                            try:
                                ###############################################################
                                partNumber = Row.select_one('.td-part').select_one('a').text.strip()
                                print('partNumber= ' + partNumber)
                                ###############################################################
                                mfr = Row.select_one('.td-mfg').text.strip()
                                # print('mfr= ' + mfr)
                                ###############################################################
                                descriptiondesc = Row.select_one('.td-desc')
                                if descriptiondesc != None:
                                    if Row.select_one('.td-desc').text.strip() != "":
                                        description = Row.select_one('.td-description')
                                        if description != None:
                                            description = Row.select_one('.td-description').text.strip()
                                        else:
                                            description = Row.select_one('.additional-description').text.strip()
                                        # print('description= ' + description)
                                    else:
                                        description = ''
                                ###############################################################
                                try:
                                    stock = int(Row['data-instock'])
                                except:
                                    stock = 0
                                # print('stock= ' + str(stock))
                                ###############################################################
                                # print('distributorType= ' + distributorType)
                                ###############################################################
                                try:
                                    BuyNow = Row.select_one('.td-buy').select_one('a')['href']
                                    # print('BuyNow= ' + BuyNow)
                                except:
                                    BuyNow = ''
                                ###############################################################
                                sku = ''
                                Parttag = Row.select_one('.part-name')
                                if Parttag != None:
                                    skutag = Parttag.select_one('.additional-value')
                                    if skutag != None:
                                        sku = Parttag.select_one('.additional-value').text.strip()
                                        if sku =='':
                                            sku = partNumber
                                    else:
                                        sku = partNumber
                                if SellerName == 'Sager':
                                    sku = partNumber
                                #     print(sku)
                                # print('sku= ' + sku)
                                ###############################################################
                                packaging = ""
                                # moq = None
                                if Row.select('.additional-description') != None:
                                    for p in Row.select('.additional-description'):
                                        title = p.select_one('.additional-title')
                                        if title != None:
                                            if 'Container' in title.text.strip():
                                                if p.select('.additional-value') != None:
                                                    packaging = p.select_one('.additional-value').text.strip()
                                            # elif title.text.strip() == 'Min Qty:':
                                            #     if p.select('.additional-value') != None:
                                            #         moq = p.select_one('.additional-value').text.strip()
                                ###########################HashCode####################################
                                InsertionDate = datetime.datetime.now()
                                pricesListFinal = sorted(pricesListFinal, key=lambda i: i['priceBreak'])
                                if len(pricesListFinal) != 0:
                                    prcicebreacks = [o['priceBreak'] for o in pricesListFinal]
                                    moq = min(prcicebreacks)
                                hashstring = SellerName + partNumber + mfr + str(stock) + str(sku) + str(packaging)
                                hashstringNew = SellerName + partNumber + mfr + str(stock) + str(sku)
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
                                ###############################################################
                                collectionRawData.update(
                                    {"SourceName": SellerName, "partNumber": partNumber, "sku": sku,
                                     'mfr': mfr, 'stock': stock},
                                    {"extractionDate": InsertionDate,
                                     "SourceName": SellerName, "partNumber": partNumber,
                                     "packagingName": packaging, "mfr": mfr, "stock": stock, 'moq': moq,
                                     "SourceURL": url, "sku": sku,
                                     'Aggregator': "FindChips",
                                     "distributorType": distributorType,
                                     "hashcode": hash512,
                                     "Description": description, "Currency": "$",
                                     "pricesPerBreaks": {"originalCurrency": "USD",
                                                         "currencyRatio": 1,
                                                         "pricesList": pricesListFinal},
                                     "part_Status": None}, upsert=True
                                )
                                collectionMouserDK.update(
                                    {"SourceName": SellerName, "partNumber": partNumber, "sku": sku,
                                     'mfr': mfr, 'stock': stock},
                                    {"extractionDate": InsertionDate,
                                     "SourceName": SellerName, "partNumber": partNumber,
                                     "packagingName": packaging, "mfr": mfr, "stock": stock, 'moq': moq,
                                     "SourceURL": url, "sku": sku,
                                     'Aggregator': "FindChips",
                                     "distributorType": distributorType,
                                     "hashcode": hash512New,
                                     "Description": description, "Currency": "$",
                                     "pricesPerBreaks": {"originalCurrency": "USD",
                                                         "currencyRatio": 1,
                                                         "pricesList": pricesListFinal},
                                     "part_Status": None}, upsert=True
                                )
                                ###############################################################
                            except Exception as ex:
                                cc = 0
                    print('===========================================================')
                else:
                    distributorType = 'false'
                    if table.select_one('h3').find('a') != None:
                        SellerNameWithSpan = table.select_one('h3').find('a').text.strip()
                        SellerNameSpan = table.select_one('h3').find('span').text.strip()
                        SellerName = str(SellerNameWithSpan).replace(SellerNameSpan, '').strip()
                        if SellerName == 'Digi-Key':
                            print(SellerName)
                            return;
                    else:
                        SellerNameWithSpan = table.select_one('h3').text.strip()
                        SellerNameSpan = table.select_one('h3').find('span').text.strip()
                        SellerName = str(SellerNameWithSpan).replace(SellerNameSpan, '').strip()
                        if SellerName == 'Digi-Key':
                            print(SellerName)
                            return;
                    PartRowListTag = RealTable.select_one('tbody').select('.row')
                    print('===========================================================')
                    if PartRowListTag != None:
                        for Row in PartRowListTag:
                            pricesListFinal = []
                            partNumber = Row.select_one('.td-part').select_one('a').text.strip()
                            prices = Row.select_one('.td-price')
                            if prices != None:
                                pricesUlList = prices.select('ul')
                                if len(pricesUlList) != 0:
                                    pricesilList = prices.select('li')
                                    if len(pricesilList) != 0:
                                        for il in pricesilList:
                                            if (il.select_one('.label')) != None:
                                                priceBreak = il.select_one('.label').text.strip()
                                                databasecurrency = il.select_one('.value').attrs['data-basecurrency']
                                                priceStr = il.select_one('.value').text.strip()
                                                if priceBreak != '':
                                                    if databasecurrency != 'USD':
                                                        price = getCurrency(databasecurrency, priceStr)
                                                        # print(
                                                        #     'Price= ' + str(price) + '     ' + 'priceBreak= ' + priceBreak)
                                                        pricesList = {"priceBreak": int(priceBreak.replace(',', '')),
                                                                      "price": price}
                                                        pricesListFinal.append(pricesList)
                                                    else:
                                                        price = str(priceStr).replace('$', '')
                                                        # print(
                                                        #     'Price= ' + str(round(float(price),3)) + '     ' + 'priceBreak= ' + priceBreak)
                                                        pricesList = {
                                                            "priceBreak": int(str(priceBreak).replace(',', '')),
                                                            "price": round(float(str(price).replace(',', '')), 3)}
                                                        pricesListFinal.append(pricesList)
                            try:
                                ###############################################################
                                partNumber = Row.select_one('.td-part').select_one('a').text.strip()
                                print('partNumber= ' + partNumber)
                                ###############################################################
                                mfr = Row.select_one('.td-mfg').text.strip()
                                # print('mfr= ' + mfr)
                                ###############################################################
                                descriptiondesc = Row.select_one('.td-desc')
                                if descriptiondesc != None:
                                    if Row.select_one('.td-desc').text.strip() != "":
                                        description = Row.select_one('.td-description')
                                        if description != None:
                                            description = Row.select_one('.td-description').text.strip()
                                        else:
                                            description = Row.select_one('.additional-description').text.strip()
                                        # print('description= ' + description)
                                    else:
                                        description = ''
                                ###############################################################
                                try:
                                    stock=int(Row['data-instock'])
                                except:
                                    stock = 0
                                # print('stock= ' + str(stock))
                                ###############################################################
                                # print('distributorType= ' + distributorType)
                                ###############################################################
                                try:
                                    BuyNow = Row.select_one('.td-buy').select_one('a')['href']
                                    # print('BuyNow= ' + BuyNow)
                                except:
                                    BuyNow = ''
                                ###############################################################
                                sku = ''
                                Parttag = Row.select_one('.part-name')
                                if Parttag != None:
                                    skutag = Parttag.select_one('.additional-value')
                                    if skutag != None:
                                        sku = Parttag.select_one('.additional-value').text.strip()
                                        if sku =='':
                                            sku = partNumber
                                    else:
                                        sku = partNumber
                                if SellerName == 'Sager':
                                    sku = partNumber
                                # if sku == 'BAV99LT1GOSTR-ND':
                                #     print(sku)
                                # print('sku= ' + sku)
                                ###############################################################
                                packaging = ""
                                # moq = None
                                if Row.select('.additional-description') != None:
                                    for p in Row.select('.additional-description'):
                                        title = p.select_one('.additional-title')
                                        if title != None:
                                            if 'Container' in title.text.strip():
                                                if p.select('.additional-value') != None:
                                                    packaging = p.select_one('.additional-value').text.strip()
                                            # elif title.text.strip() == 'Min Qty:':
                                            #     if p.select('.additional-value') != None:
                                            #         moq = p.select_one('.additional-value').text.strip()
                                ###########################HashCode####################################
                                InsertionDate = datetime.datetime.now()
                                pricesListFinal = sorted(pricesListFinal, key=lambda i: i['priceBreak'])
                                if len(pricesListFinal) != 0:
                                    prcicebreacks = [o['priceBreak'] for o in pricesListFinal]
                                    moq = min(prcicebreacks)
                                hashstring = SellerName + partNumber + mfr + str(stock) + str(sku) + str(packaging)
                                hashstringNew = SellerName + partNumber + mfr + str(stock) + str(sku)
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
                                ###############################################################
                                collectionRawData.update(
                                    {"SourceName": SellerName, "partNumber": partNumber, "sku": sku,
                                     'mfr': mfr, 'stock': stock},
                                    {"extractionDate": InsertionDate,
                                     "SourceName": SellerName, "partNumber": partNumber,
                                     "packagingName": packaging, "mfr": mfr, "stock": stock, 'moq': moq,
                                     "SourceURL": url, "sku": sku,
                                     'Aggregator': "FindChips",
                                     "distributorType": distributorType,
                                     "hashcode": hash512,
                                     "Description": description, "Currency": "$",
                                     "pricesPerBreaks": {"originalCurrency": "USD",
                                                         "currencyRatio": 1,
                                                         "pricesList": pricesListFinal},
                                     "part_Status": None}, upsert=True
                                )
                                collectionMouserDK.update(
                                    {"SourceName": SellerName, "partNumber": partNumber, "sku": sku,
                                     'mfr': mfr, 'stock': stock},
                                    {"extractionDate": InsertionDate,
                                     "SourceName": SellerName, "partNumber": partNumber,
                                     "packagingName": packaging, "mfr": mfr, "stock": stock, 'moq': moq,
                                     "SourceURL": url, "sku": sku,
                                     'Aggregator': "FindChips",
                                     "distributorType": distributorType,
                                     "hashcode": hash512New,
                                     "Description": description, "Currency": "$",
                                     "pricesPerBreaks": {"originalCurrency": "USD",
                                                         "currencyRatio": 1,
                                                         "pricesList": pricesListFinal},
                                     "part_Status": None}, upsert=True
                                )
                                ###############################################################
                            except Exception as ex:
                                cc = 0
                    print('===========================================================')
            else:
                i = 0
        else:
            i = 0
    except Exception as ex:
        print(ex)
def fetch_url(entry):
    try:
        Server, Partial = entry
        session = requests.Session()
        # session.config['keep_alive'] = False
        timeout = 10
        retry = Retry(connect=2, backoff_factor=5)
        adapter = HTTPAdapter(max_retries=retry)
        adapter.config['keep_alive'] = True
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        headers = {"Pragma": "no-cache", 'Cache-Control': 'no-cache', 'referer': 'www.findchips.com',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
        proxies = {'https': '108.59.14.200:13152'}
        Url='https://www.findchips.com/search/'+Partial+'?currency=USD'
        # Url='https://www.findchips.com/search/H-120?currency=USD'
        r = session.get(Url, headers=headers,proxies=proxies, allow_redirects=False)
        r.encoding = 'utf-8'
        # driver = webdriver.Chrome(executable_path=r"D:\Tools\Mouser_New_D\chromedriver.exe")
        # driver.get(uri)
        myquery={}
        newvalues={}
        if r.status_code == 200:
            # soup = BeautifulSoup(r.text, features="html.parser")
            soup = BeautifulSoup(r.text, features="lxml")
            AllDistTables = soup.select('.distributor-results')
            checkFoundPart = soup.select('.no-results')
            if len(checkFoundPart) == 0:
                print(len(AllDistTables))
                InsertionDate = datetime.datetime.now()
                if AllDistTables != None:
                    if len(AllDistTables) != 0:
                        for table in AllDistTables:
                            ExtractFromTable(table, Url)
                        myquery = {"Partial": Partial, "Server": Server}
                        newvalues = {"$set": {"FC_Status": "3"}}
                    else:
                        myquery = {"Partial": Partial, "Server": Server}
                        newvalues = {"$set": {"FC_Status": "4", "Exception": "Wrong html"}}
            else:
                myquery = {"Partial": Partial, "Server": Server}
                newvalues = {"$set": {"FC_Status": "4", "Exception": "Part No Results"}}
        else:
            myquery = {"Partial": Partial,"Server": Server}
            newvalues = {"$set": {"FC_Status": "4", "Exception": "Not Found"}}
        Aggregatorcollection.update_many(myquery, newvalues)
        return Url
    except Exception as ex:
        print(ex)
        myquery = {"Partial": Partial,"Server": Server}
        newvalues = {"$set": {"FC_Status": "4", "Exception": "Blocked"}}
        Aggregatorcollection.update_many(myquery, newvalues)
        return None
def ResetFCInput(Aggregator,Server):
    print("###################################### Start Reset FC Input ###############################")
    myquery = {"Aggregator": Aggregator,"Server": Server}
    newvalues = {"$set": {"FC_Status": "1", "Exception": ""}}
    Aggregatorcollection.update_many(myquery, newvalues)
    print("###################################### Done Reset FC Input ###############################")
    # FinchipInputBulk.append(UpdateMany(myquery, newvalues))
def getAllCurrency():
    try:
        session = requests.Session()
        retry = Retry(connect=2, backoff_factor=5)
        adapter = HTTPAdapter(max_retries=retry)
        adapter.config['keep_alive'] = True
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        headers = {"Pragma": "no-cache", 'Cache-Control': 'no-cache', 'referer': 'www.findchips.com',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
        proxies = {'https': '108.59.14.200:13152'}
        Url='https://api.exchangerate-api.com/v4/latest/USD'
        r = session.get(Url, headers=headers,proxies=proxies, allow_redirects=False)
        r.encoding = 'utf-8'
        if r.status_code == 200:
            datajson=json.loads(r.text)
            currencies=datajson['rates']
            return currencies
        else:
            return ''
    except:
        return ''
urls = []
Currency=getAllCurrency()
while 1:
        urls=[]
        FinchipInputBulk = []
        FinchipOutputBulk = []
        RawDataBulk = []
        if Currency !='':
            FidChipsPartial = list(Aggregatorcollection.find({'Aggregator': "FindChips","FC_Status":"1","Server":{'$in':["106"]}},
                                                             {'Partial': 1, 'Server': 1}))
            if len(FidChipsPartial) != 0:
                for item in FidChipsPartial:
                    #x =  FindChipsUrl = 'https://www.findchips.com/search/'+item['Partial']+'?currency=USD'
                    # myquery = {"Partial": item['Partial']}
                    # newvalues = {"$set": {'Status': "2"}}
                    # Aggregatorcollection.update_many(myquery, newvalues)
                    x = item['Partial']#'https://www.findchips.com/search/BAV99?currency=USD
                    y = str(item['Server'])
                    a = (y, x)
                    urls.append(a)
                try:
                    start = timer()
                    results = ThreadPool(50).imap_unordered(fetch_url, urls)
                    for path in results:
                        if path != None:
                            print(path)
                    print(f"Elapsed Time: {timer() - start}")
                    # if len(RawDataBulk) != 0:
                    #     resultRawData = collectionRawData.bulk_write(RawDataBulk)
                    # if len(FinchipOutputBulk) != 0:
                    #     resultFinchipOutput = collectionMouserDK.bulk_write(FinchipOutputBulk)
                    # if len(FinchipInputBulk) != 0:
                    #     resultFinchipInput = Aggregatorcollection.bulk_write(FinchipInputBulk)
                except Exception as ex:
                     print(ex)
            else:
                ResetFCInput("FindChips", "106")
        else:
            print('Wrong Get Currencies')
            
