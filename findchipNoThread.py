from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest
import xlrd
from xlrd import sheet
from time import perf_counter
from threading import Thread




def data_grabber(url):
	try:
		page = requests.get(url, timeout=10)
		if page.status_code == 200:
			html = page.text
			soup = BeautifulSoup(html,'html.parser')
			return soup, url
		else:
			#soup = None
			return "Block", url

	except requests.Timeout as err:
		print("Timeout")
		return "Timeout" , url
	except Exception as err:
		print(err)
		return "Timeout" , url


def write_result(data):
	with open("findchips.csv","a",encoding="UTF-8", newline='') as f:
		wr = csv.writer(f)
		wr.writerows(data)

		
		
	
def get_items(item):

	PartialList 	 = []
	PartsList 		 = []
	SkuList 		 = [] 
	PricingList		 = []
	DistributorsList = []
	MfrList			 = []
	DescriptionList  = []
	StockList	     = []

	page 			 = item[0]
	UrlPartial 		 = item[1]
	Partial 		 = UrlPartial.replace("https://www.findchips.com/search/", "").replace("?currency=USD", "")

	
	if page == 'Timeout':

		PartialList.append(Partial)
		PartsList.append("Timeout")
		SkuList.append("Timeout") 
		PricingList.append("Timeout")
		DistributorsList.append("Timeout")
		MfrList.append("Timeout")
		DescriptionList.append("Timeout")
		StockList.append("Timeout")
		
		fileList = [PartialList, DistributorsList, PartsList, SkuList, MfrList, DescriptionList, StockList, PricingList]
		exported = zip_longest(*fileList)
		write_result(exported)
		print(Partial, " Time Out")

	elif page == 'Block':
		PartialList.append(Partial)
		PartsList.append("Block")
		SkuList.append("Block") 
		PricingList.append("Block")
		DistributorsList.append("Block")
		MfrList.append("Block")
		DescriptionList.append("Block")
		StockList.append("Block")
		
		fileList = [PartialList, DistributorsList, PartsList, SkuList, MfrList, DescriptionList, StockList, PricingList]
		exported = zip_longest(*fileList)
		write_result(exported)
		

		print(Partial, " Block")

	else:
				

		notfound = page.find("p",{"class":"no-results"})

		header = ["Partial", "Distributor", "Part Number", "SKU", "Price"]

		if notfound != None:

			PartialList.append(Partial)
			PartsList.append("Not Found")
			SkuList.append("Not Found") 
			PricingList.append("Not Found")
			DistributorsList.append("Not Found")
			MfrList.append("NotFound")
			DescriptionList.append("Not Found")
			StockList.append("Not Found")
			
			fileList = [PartialList, DistributorsList, PartsList, SkuList, MfrList, DescriptionList, StockList, PricingList]
			exported = zip_longest(*fileList)
			write_result(exported)

		else:

			
			distributors = page.find_all("div",{"class": "distributor-results"})
			
			for i in range(len(distributors)):
				dist_name = distributors[i].find("h3",{"class":"distributor-title"}).text.strip()
				tb = distributors[i].find("table")
				rows = tb.find("tbody").find_all("tr")
				for x in range(len(rows)):
					
					try:
						if len(rows[x].find("td",{"class":"td-price"}).text) == 49:
							PartialList.append(Partial)
							DistributorsList.append(dist_name)
							#PartNumber If Price IS Empty
							try:
								partNumber = rows[x].find("td",{"class":"td-part"}).a.text.strip()
								PartsList.append(partNumber)
							except:
								partNumber = "No PartNumber"
								PartsList.append(partNumber)
							#SKU If Price Is Empty
							try:
								sku = rows[x].find("td",{"class":"td-part"}).span.text.strip().replace("\n"," ").replace("DISTI #","")
								SkuList.append(sku)
							except:
								sku = "No Sku"
								SkuList.append(sku)
							
							#MFR If Price Is Empty
							try:
								mfr = rows[x].find("td",{"class":"td-mfg"}).span.text.strip()
								MfrList.append(mfr)
							except:
								mfr = "No Mfr"
								MfrList.append(mfr)

							#Description If Price IS Empty
							try:
								descrition = rows[x].find("td",{"class":"td-desc"}).text.strip()
								DescriptionList.append(descrition.replace("\n", " ").replace("                      ", ""))
							except:
								descrition = "No Descrition"
								DescriptionList.append(descrition)

							#Stock If Price IS Empty
							try:
								stock = rows[x].find("td",{"class":"td-stock"}).text.strip()
								
								StockList.append(stock.replace('"', '').replace("\n"," "))
							except:
								stock = "No Stock"
								StockList.append(stock)

							#Price
							PricingList.append("No Price")

						else:
							
							all_pricing = rows[x].find("td",{"class":"td-price"}).find("ul", {"class": "price-list"}).find_all("li")
							for y in range(len(all_pricing)):
								if all_pricing[y].text != 'See More':
									PartialList.append(Partial)
									DistributorsList.append(dist_name)
									# PartNumber Repeat With Every Row In Price
									try:
										partNumber = rows[x].find("td",{"class":"td-part"}).a.text.strip()
										PartsList.append(partNumber)
									except:
										partNumber = "No Part Number"
										PartsList.append(partNumber)
									#SKU Repeat With Every Row In Price
									try:
										sku = rows[x].find("td",{"class":"td-part"}).span.text.strip().replace("\n"," ").replace("DISTI #","")
										SkuList.append(sku)
									except:
										sku = "No Sku"
										SkuList.append(sku)
									# Price Row
									price = all_pricing[y].text	

									#MFR Repeat With Every Row In Price
									try:
										mfr = rows[x].find("td",{"class":"td-mfg"}).span.text.strip()
										MfrList.append(mfr)
									except:
										mfr = "No Mfr"
										MfrList.append(mfr)


									#Description Repeat With Every Row In Price
									try:
										descrition = rows[x].find("td",{"class":"td-desc"}).text.strip().replace(",","")
										DescriptionList.append(descrition.replace("\n"," ").replace("                      ", ""))
									except:
										descrition = "No Descrition"
										DescriptionList.append(descrition)

									#Stock Repeat With Every Row In Price
									try:
										stock = rows[x].find("td",{"class":"td-stock"}).text.strip()
										StockList.append(stock.replace('"', '').replace("\n"," "))
									except:
										stock = "No Stock"
										StockList.append(stock)


									#All Price Rows
									PricingList.append(price)
									
					except:
						print("Pricing: No Price")


			fileList = [PartialList, DistributorsList, PartsList, SkuList, MfrList, DescriptionList, StockList, PricingList]
			exported = zip_longest(*fileList)
			write_result(exported)


		print(Partial, " Done")
			
"""
replace / >> %2F .. , >> %2C ..  

"""

input_file = input("PLease Enter The Path Of Excel Sheet That Contains Part Numbers you want to Run On It : ")

web = xlrd.open_workbook(input_file)
sheet = web.sheet_by_index(0)
input_list = []
for i in range(sheet.nrows):
    input_list.append(sheet.cell_value(i,0))


with open("findchips.csv","w",encoding="UTF-8", newline='') as f:
	wr = csv.writer(f)
	wr.writerow(["Partial", "Distributor", "Part Number", "SKU", "MFR", "Description", "Stock", "Price"])

start = perf_counter()
for i in input_list:
	get_items(data_grabber(f'https://www.findchips.com/search/{i}?currency=USD'))

end = perf_counter()

print(f"Task Takes {round(end-start,2)} seconds... ")
print("############ End OF Task..!!! ############")


