import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import os, shutil

# Start Prepare Input

#input_text = "C1005X7R1H104K050BB nte248 HLG-240H-C2100"
input_text = "450-0064 nte248 LTST-C191KGKT"
input = input_text.split(" ")

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
for iterable in range(len(input)):
    
    print(input[iterable])
    result = requests.get(f"https://www.findchips.com/search/{input[iterable]}")
    
    src = result.content

    soup = BeautifulSoup(src, "lxml")



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


