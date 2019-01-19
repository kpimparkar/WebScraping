# WebScraping
This repo holds mini projects involving web scraping and analysis of the scraped data.
# List of Projects :
1. Famous restaurants in your city.
2. Scrape baby girl names.  

# PROJECT 1 : FAMOUS RESTAURANTS IN YOUR CITY !!
- **PROJECT SUMMARY :**  
   This project is to provide a command line python script to extract and analyze data of local restaurants. The script allows users to provide a city name and state code as the input. The source of information is www.yelp.com.

   The python script connects with www.yelp.com and searches list of restaurant from the provided city. This information is stored in a `.csv` format. This output file is then accessed in this jupyter notebook to perform further analysis.


- **COMPONENTS INVOLVED IN THE PROJECT :**    
   - **getRestaurantData.py** : Python script to connect to www.yelp.com and extract details of enlisted restaurants. Tasks performed by this script :
     - [X] Take city name and state code as mandatory user inputs  
     - [x] Take output file name, location and delay time as optional user inputs  
     - [x] Connect to www.yelp.com to fetch list of testaurants of provided city  
     - [x] Extract data such as name, website, rating, number of reviews, food category, proce category, phone number, address and locality of the enlisted restaurant  
     - [x] Manage pagination to extract all enlisted restaurants  
     - [x] Store this data in an output file in a comma separated values format  
          
   - **FA18_WebScraping_Project01_getRestaurants.ipynb** : To show summary, usage and analysis of the project. Tasks performed by this .ipynb :
     - [x] Load the data in a pandas dataframe
     - [x] Find most and least reviewed restaurant food category
     - [x] Plot bar chart of restaurant categories against number of reviews to show poplarity of categories
     - [x] Enlist restaurants with highest rating
     - [x] Enlist restaurants with maximum number of reviews
     - [x] Plot a bar chart of price categories against number of reviews to show popularity of price categories


- **USAGE**    
   - **python getRestaurantData.py -h**  

```
C:\Study\IUMSDS\FA18-WebScraping\Project>python getRestaurantData.py -h

getRestaurantData.py --cityState="<cityName>" --oPath=<outfilePath> --oFile=<outFileName>

cityName    : Mandatory. Name of the city and state code to search restaurants.Enclosed in double quotes. Ex: "Salt lake city, UT"
outfilePath : Optional. Location of the output file. Default : Current location.
outFileName : Optional. Restaurant list will be stored in this file. Preferred format .csv. Default : RestaurantData.csv

C:\Study\IUMSDS\FA18-WebScraping\Project>
```
# PROJECT 2 : SCRAPE BABY GIRL NAMES !!
- **PROJECT SUMMARY :**  
   This python script scrpaes baby girl names from firstcry.com. List of baby names along with meaning and firstcry link are provided as output of this python script in a .csv file.
