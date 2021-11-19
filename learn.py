from bs4 import BeautifulSoup
import requests

def data_grabber(url):

	try:

		page = requests.get(url, timeout=5)
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

	page 			 = item[0]
	Partial 		 = item[1]
	notfound = page.find("p",{"class":"no-results"})

	header = ["Partial", "Distributor", "Part Number", "SKU", "Price"]

	if notfound != None:

		PartialList.append(Partial)
		PartsList.append("Not Found")
		SkuList.append("Not Found") 
		PricingList.append("Not Found")
		DistributorsList.append("Not Found")

		with open("E:\python//result.txt","a") as f:
			for h in header:
				f.write(f'{h}\t')

		with open("E:\python//result.txt","a") as f:
			f.write(f'\n')
			for i,j,k,l,m in zip(PartialList, DistributorsList, PartsList, SkuList, PricingList):
				f.write(f'{i}\t{j}\t{k}\t{l}\t{m}\n')



	else:

		
		distributors = page.find_all("div",{"class": "distributor-results"})
		
		for i in range(len(distributors)):
			#distributor_name = distributors[i].find("h3",{"class":"distributor-title"}).text.strip()
			dist_name = distributors[i].find("h3",{"class":"distributor-title"}).text.strip()
			#print(distributors[i].find("h3",{"class":"distributor-title"}).text.strip())
			#print(dist_name)
			tb = distributors[i].find("table")
			rows = tb.find("tbody").find_all("tr")
			for x in range(len(rows)):
				# PartNumber
				"""
				try:

					print("PartNumber = ",rows[x].find("td",{"class":"td-part"}).a.text.strip())
				except:
					print("PartNumber = ","No Part Number")
				#Sku
				try:
					print("SKU = ", rows[x].find("td",{"class":"td-part"}).span.text.strip().replace("\n","").replace("DISTI #",""))
				except:
					print("SKU = ", "no sku")
				"""

				#Pricing
				try:
					if len(rows[x].find("td",{"class":"td-price"}).text) == 49:
						PartialList.append(Partial)
						DistributorsList.append(dist_name)
						print(dist_name)
						#PartNumber If Price IS Empty
						try:
							partNumber = rows[x].find("td",{"class":"td-part"}).a.text.strip()
							#print("PartNumber = ",rows[x].find("td",{"class":"td-part"}).a.text.strip())
							print("PartNumber = ", partNumber)
							PartsList.append(partNumber)
						except:
							partNumber = "No PartNumber"
							print("PartNumber = ",partNumber)
							PartsList.append(partNumber)
						#SKU If Price Is Empty
						try:
							sku = rows[x].find("td",{"class":"td-part"}).span.text.strip().replace("\n","").replace("DISTI #","")
							print("SKU = ", sku)
							SkuList.append(sku)
							#print("SKU = ", rows[x].find("td",{"class":"td-part"}).span.text.strip().replace("\n","").replace("DISTI #",""))
						except:
							sku = "No Sku"
							print("SKU = ", sku)
							SkuList.append(sku)
						
						print("Pricing: Empty")
						PricingList.append("No Price")

						with open("E:\python//result.txt","a") as f:
							for h in header:
								f.write(f'{h}\t')

						with open("E:\python//result.txt","a") as f:
							f.write(f'\n')
							for i,j,k,l,m in zip(PartialList, DistributorsList, PartsList, SkuList, PricingList):
								f.write(f'{i}\t{j}\t{k}\t{l}\t{m}\n')


 	
					else:
						
						all_pricing = rows[x].find("td",{"class":"td-price"}).find("ul", {"class": "price-list"}).find_all("li")
						for y in range(len(all_pricing)):
							if all_pricing[y].text != 'See More':
								print(dist_name)
								PartialList.append(Partial)
								DistributorsList.append(dist_name)
								# PartNumber Repeat With Every Row In Price
								try:
									partNumber = rows[x].find("td",{"class":"td-part"}).a.text.strip()
									#print("PartNumber = ",rows[x].find("td",{"class":"td-part"}).a.text.strip())
									print("PartNumber = ",partNumber)
									PartsList.append(partNumber)
								except:
									partNumber = "No Part Number"
									print("PartNumber = ",partNumber)
									PartsList.append(partNumber)
								#SKU Repeat With Every Row In Price
								try:
									sku = rows[x].find("td",{"class":"td-part"}).span.text.strip().replace("\n","").replace("DISTI #","")
									#print("SKU = ", rows[x].find("td",{"class":"td-part"}).span.text.strip().replace("\n","").replace("DISTI #",""))
									print("SKU = ", sku)
									SkuList.append(sku)
								except:
									sku = "No Sku"
									print("SKU = ", sku)
									SkuList.append(sku)
								# Price Row
								price = all_pricing[y].text	
								print(price)
								PricingList.append(price)
								#print(all_pricing[y].text)

						with open("E:\python//result.txt","a") as f:
							for h in header:
								f.write(f'{h}\t')

						with open("E:\python//result.txt","a") as f:
							f.write(f'\n')
							for i,j,k,l,m in zip(PartialList, DistributorsList, PartsList, SkuList, PricingList):
								f.write(f'{i}\t{j}\t{k}\t{l}\t{m}\n')

					
				
				
					print("Done")					

					#print("Pricing = ", len(rows[x].find("td",{"class":"td-price"}).text))
					#print("Pricing = ", rows[x].find("td",{"class":"td-price"}).text)
				except:
					print("Pricing: No Price")


		

#get_items(data_grabber("https://www.findchips.com/search/LM317LBD"))
#get_items(data_grabber("https://www.findchips.com/search/Moaaz"))


input_list = ["https://www.findchips.com/search/LM317LBD", "https://www.findchips.com/search/NTE248"]
for i in input_list:
	get_items(data_grabber(i))




