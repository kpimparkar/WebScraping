import sys, getopt
import os
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import csv
import time

def getYelpUrl(ipCity):
	#https://www.yelp.com/search?cflt=restaurants&find_loc=Salt+Lake+City%2C+UT
	baseUrl = "https://www.yelp.com/search?"
	urlQuery = {'cflt':'restaurants','find_loc':ipCity}
	url = baseUrl + urlencode(urlQuery)
	print("CONNECTING TO URL : ", url)
	return(url)


def fetchData(url,opPath,opFile,opFileMode):
	# Creating request headers
	req_headers = {}
	req_headers['user-agent'] = r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'

	# Creating a request object
	req = Request(url, headers=req_headers)
	#req = Request(url)
	
	# Requesting data from the website
	# fill in the blanks
	try:
		response = urlopen(req)
		print("THE CONNECTION STATUS = ", response.status)
		page_content = response.read().decode('utf-8')
		#print(len(page_content))
		bs = BeautifulSoup(page_content,'html5lib')
		#print("bs done")
		htmldata = bs.prettify()
		with open("htmldata.html", "w", encoding='utf-8',) as ho:
			ho.writelines(htmldata)
		
		fileObj = opPath + "\\" + opFile
		#print(fileObj)
		nextURL = ' '

		with open(fileObj,opFileMode,newline='') as fo:
			opWriter = csv.writer(fo)
			#print("REACHED FILE")
			if bs.find('div', class_="biz-attributes"):
#				print("FOUND biz-attributes")
				nextURL = "https://www.yelp.com"+bs.body.find('a',class_="u-decoration-none next pagination-links_anchor")['href']
				#print("THE NEXT URL IS = ",nextURL)
				
				for i in bs.find_all('div', class_="biz-attributes"):
					opName,opLink,opRating,opReviewCount,opPriceRange,opCategory,opPhone,opAddress,opLocality = ' '*9
					#print("REACHED FOR")
					if i.find('span',class_="indexed-biz-name"):
						#print("REACHED IF")
						name=i.find('span',class_="indexed-biz-name")
						opName = name.a.text
						if i.a:
							opLink = "https://www.yelp.com/"+i.a['href']
						if i.find('div', class_="i-stars"):
							opRating=i.find('div', class_="i-stars")['title'].split()[0]
						if i.find('span', class_="review-count rating-qualifier"):
							opReviewCount=i.find('span', class_="review-count rating-qualifier").text.strip().split()[0]
						if i.find('span', class_="business-attribute price-range"):
							opPriceRangeT = i.find('span', class_="business-attribute price-range").text
							if opPriceRangeT.strip() == "$":
								opPriceRange = "Low"
							elif opPriceRangeT.strip() == "$$":
								opPriceRange = "Moderate"
							elif opPriceRangeT.strip() == "$$$":
								opPriceRange = "High"
						if i.find('span', class_="category-str-list"):
							category=[]
							cats = i.find('span', class_="category-str-list")
							for cat in cats.find_all('a'):
								category.append(cat.text)
							opCategory=category
						address = i.find('div', class_="secondary-attributes")
						if address.find('span', class_='biz-phone'):
							opPhone=address.find('span', class_='biz-phone').text.strip()
						if address.find('address'):
							opAddress=address.find('address').text.strip()
						if address.find('span', class_='neighborhood-str-list'):
							opLocality = address.find('span', class_='neighborhood-str-list').text.strip()
						#print(opName,",",opLink,",",opRating,",",opReviewCount,",",opPriceRange,",",opCategory,",",opPhone,",",opAddress,",",opLocality)
						#global counter += 1
						opWriter.writerow([opName,opLink,opRating,opReviewCount,opPriceRange,opCategory,opPhone,opAddress,opLocality])
				return nextURL
			else:
				#print("NOT FOUND biz-attributes")
				if bs.find('div', class_="lemon--div__373c0__6Tkil largerScrollablePhotos__373c0__3FEIJ arrange__373c0__UHqhV border-color--default__373c0__2oFDT"):
					#print("BUT FOUND OTHER CLASS.")
					nextURL = "https://www.yelp.com" + bs.body.find('a',class_="next-link")['href']
					#print("NEXT LINK = " ,nextURL)
					for i in bs.find_all('div', class_="lemon--div__373c0__6Tkil largerScrollablePhotos__373c0__3FEIJ arrange__373c0__UHqhV border-color--default__373c0__2oFDT"):
						opName,opLink,opRating,opReviewCount,opPriceRange,opCategory,opPhone,opAddress,opLocality = ' '*9
						#if i.find('span',class_="indexed-biz-name"):  ### check this if to avoid "ADs" in o/p
						#print("REACHED IF")
						name=i.find('a',class_="lemon--a__373c0__1_OnJ link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5")
						opName = name.text
						if i.find('p',class_="yloca-pill__373c0__3Owv4"):
							if i.find('p',class_="yloca-pill__373c0__3Owv4").text =='Ad':
								#print("SKIPPED :", opName)
								continue
						if name:
							opLink = "https://www.yelp.com"+name['href']
						if i.find('div', class_="i-stars__373c0__Y2F3O"):
							opRating= i.find('div', class_="i-stars__373c0__Y2F3O")["aria-label"].split()[0]
						if i.find('span', class_="reviewCount__373c0__2r4xT"):
							opReviewCount=i.find('span', class_="reviewCount__373c0__2r4xT").text.strip().split()[0]
						if i.find('span', class_="priceRange__373c0__2DY87"):
							opPriceRangeT = i.find('span', class_="priceRange__373c0__2DY87").text
							if opPriceRangeT.strip() == "$":
								opPriceRange = "Low"
							elif opPriceRangeT.strip() == "$$":
								opPriceRange = "Moderate"
							elif opPriceRangeT.strip() == "$$$":
								opPriceRange = "High"
						if i.find('div', class_="lemon--div__373c0__6Tkil priceCategory__373c0__3zW0R border-color--default__373c0__2oFDT"):
							category=[]
							cats = i.find('div', class_="lemon--div__373c0__6Tkil priceCategory__373c0__3zW0R border-color--default__373c0__2oFDT")
							for cat in cats.find_all('a'):
								category.append(cat.text)
							opCategory=category
						address = i.find('div', class_="secondaryAttributes__373c0__7bA0w")
						if address.find('div', class_='lemon--div__373c0__6Tkil display--inline-block__373c0__2de_K border-color--default__373c0__2oFDT'):
							opPhone=address.find('div', class_='lemon--div__373c0__6Tkil display--inline-block__373c0__2de_K border-color--default__373c0__2oFDT').text.strip()
						if address.find('address'):
							opAddress=address.find('address').text.strip()
						if address.find('div', class_='lemon--div__373c0__6Tkil u-space-t1 border-color--default__373c0__2oFDT'):
							opLocality = address.find('div', class_='lemon--div__373c0__6Tkil u-space-t1 border-color--default__373c0__2oFDT').text.strip()
						#global counter += 1
						opWriter.writerow([opName,opLink,opRating,opReviewCount,opPriceRange,opCategory,opPhone,opAddress,opLocality])
					return nextURL
	except Exception as e:
		print("EXCEPTION BLOCK OF FUNCTION fetchData :", e)
		sys.exit(2)
		
def main(argv):
	try:
		opts, args = getopt.getopt(argv,"h",["cityState=","oPath=","oFile=","delay="])
		#print("opts: " , opts)
		#print("args : " , args)
	except getopt.GetoptError as e:
		print ("INVALID INPUT. CORRECT FORMAT =\n", 'getRestaurantData.py --cityState="<cityName>" --oPath=<outfilePath> --oFile=<outFileName')
		print ("ERROR : ", e)
		print("FOR MORE DETAILS : getRestaurantData.py -h")
		sys.exit(2)
	ipCity = None
	opPath = None
	opFile = None
	ipDelay = None
	for option, value in opts:
		if option == "-h":
			print('\ngetRestaurantData.py --cityState="<cityName>" --oPath=<outfilePath> --oFile=<outFileName>')
			print("\ncityName    : Mandatory. Name of the city and state code to search restaurants.Enclosed in double quotes. Ex: \"Salt lake city, UT\"\noutfilePath : Optional. Location of the output file. Default : Current location.\noutFileName : Optional. Restaurant list will be stored in this file. Preferred format .csv. Default : RestaurantData.csv")
			sys.exit()
		elif option == "--cityState":
			ipCity = value
			print("Searching restaurants located in ", ipCity)
		elif option == "--oPath":
			opPath = value
			#print("getopt:", opPath)
		elif option == "--oFile":
			opFile = value
			#print("getopt:", opFile)
		elif option == "--delay":
			ipDelay = value
	if ipCity == None:
		print("--cityState ARGUEMENT IS MANDATORY. FOR MORE DETAILS : getRestaurantData.py -h")
		sys.exit(2)
	if opPath == None:
		opPath = os.getcwd()
	if opFile == None:
		opFile = "RestaurantData.csv"
	if ipDelay == None:
		ipDelay = 10
		
	url = getYelpUrl(ipCity)
	nextURL = fetchData(url,opPath,opFile,"w")

	while True:
		if nextURL:
		##SLEEP
			print("FETCHING DATA FROM : {}".format(nextURL))
			nextURL=fetchData(nextURL,opPath,opFile,"a")
		else:
			break

if __name__ == "__main__":
	start = time.time()
	main(sys.argv[1:])
	duration = time.time() - start
	mins, sec = divmod(duration,60)
	print("\nDATA EXTRACTION COMPLETED IN {} MINS AND {} SECONDS".format(mins, sec))
	
