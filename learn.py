from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest



def data_grabber(url):

	try:

		page = requests.get(url, timeout=0.000001)
		if page.status_code == 200:
			html = page.text
			soup = BeautifulSoup(html,'html.parser')
			#print(soup)
			#print(url)
			return soup, url
		else:
			soup = None

	except requests.Timeout as err:
		print("Timeout")
		return None, url

	except Exception as err:
		print(err)
		return None, url
	
	
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
	#print(Partial)
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
			
		with open("E:\python//findchips.csv","a",encoding="UTF-8", newline='') as f:
			wr = csv.writer(f)
			wr.writerows(exported)

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
							sku = rows[x].find("td",{"class":"td-part"}).span.text.strip().replace("\n","").replace("DISTI #","")
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
							descrition = rows[x].find("td",{"class":"td-desc"}).span.text.strip()
							DescriptionList.append(descrition)
						except:
							descrition = "No Descrition"
							DescriptionList.append(descrition)

						#Stock If Price IS Empty
						try:
							stock = rows[x].find("td",{"class":"td-stock"}).span.text.strip()
							StockList.append(stock)
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
									sku = rows[x].find("td",{"class":"td-part"}).span.text.strip().replace("\n","").replace("DISTI #","")
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
									descrition = rows[x].find("td",{"class":"td-desc"}).span.text.strip()
									DescriptionList.append(descrition)
								except:
									descrition = "No Descrition"
									DescriptionList.append(descrition)

								#Stock Repeat With Every Row In Price
								try:
									stock = rows[x].find("td",{"class":"td-stock"}).span.text.strip()
									StockList.append(stock)
								except:
									stock = "No Stock"
									StockList.append(stock)


								#All Price Rows
								PricingList.append(price)
								
				except:
					print("Pricing: No Price")


		fileList = [PartialList, DistributorsList, PartsList, SkuList, MfrList, DescriptionList,PricingList]
		exported = zip_longest(*fileList)

		with open("E:\python//findchips.csv","a",encoding="UTF-8", newline='') as f:
			wr = csv.writer(f)
			wr.writerows(exported)

	print(Partial, " Done")
		




		
#LM317LBD = 82, NTE248 = 24 BT151X-800R/DG,127


"""
replace / >> %2F .. , >> %2C ..  

"""

input_list = ["https://www.findchips.com/search/LM317LBD?currency=USD", 
			  "https://www.findchips.com/search/NTE248?currency=USD",
			  "https://www.findchips.com/search/moaaz?currency=USD",
			  "https://www.findchips.com/search/BT151X-800R/DG,127?currency=USD",
			  "https://www.findchips.com/search/BT151X-800R%2fDG%2c127?currency=USD"
			  ]


with open("E:\python//findchips.csv","w",encoding="UTF-8", newline='') as f:
	wr = csv.writer(f)
	wr.writerow(["Partial", "Distributor", "Part Number", "SKU", "MFR", "Description", "Price"])
	
for i in input_list:
	get_items(data_grabber(i))


