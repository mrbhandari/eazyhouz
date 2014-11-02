import json
import sys,os
import datetime
from decimal import *
import datetime

your_djangoproject_home="/Users/pradeep/eazyhouz/eazyhouz/mysite"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
getcontext().prec = 5
from search.models import PrevHomeSales

files = []
filename = sys.argv[1]
print filename
files.extend(filename)

houses = []
for f in files:
    houses.extend(json.load(open(f)))

def good_house(house):
    return bool(house.get("beds")) and bool(house.get("baths")) and bool(house.get("address")) and bool(house.get("zipcode")) and bool(house.get("state")) and bool(house.get("city")) and bool(house.get("price")) and bool(house.get("sqft")) and bool(house.get("year_built")) and bool(house.get("last_sold_date")) and bool(house.get("latitude")) and bool(house.get("longitude"))

city="san mateo"
num_good_houses = 0
num_houses_with_exceptions = 0
for house in houses:
	try:
	    if good_house(house):
	        house_city = house.get("city").lower().replace(",","")
	        if city == house_city:
	            prevhomesales = PrevHomeSales()
	            num_good_houses += 1
	            prevhomesales.address = house.get("address")
	            prevhomesales.zipcode = house.get("zipcode")
	            prevhomesales.baths = Decimal(house.get("baths").replace("&1/2",".5"))
	            prevhomesales.beds = house.get("beds")
	            prevhomesales.city = house_city
	            prevhomesales.state = house.get("state")
	            prevhomesales.sale_price = Decimal(house.get("price").replace("$","").replace(",",""))
	            prevhomesales.url = house.get("url")
	            
	            sqft = house.get("sqft")
	            if sqft:
	                sqft = sqft.replace(",","").replace(" sqft","").replace("-","")
	            if sqft:
	                prevhomesales.sqft = sqft
	            year_built = house.get("year")
	            if year_built:
	                year_built = year_built.replace(",","").replace("-","")
	            if year_built:
	                prevhomesales.year_built = year_built
	            image_url = house.get("image_url")
	            if image_url:
	                prevhomesales.image_url = image_url
	            lot_size = house.get("lot_size")
	            if lot_size:
	                lot_size = lot_size.replace(",","").replace("-","")
	            if lot_size:
		    	prevhomesales.lot_size = lot_size
                    description = house.get("description")
		    prevhomesales.latitude = house.get("latitude")
		    prevhomesales.longitude = house.get("longitude")
		    last_sale_date = house.get("last_sold_date")
                    if last_sale_date:
		    	prevhomesales.last_sale_date = datetime.datetime.strptime(last_sale_date,'%m/%d/%y').date()
		    if description:
			prevhomesales.remodeled = 1 if (("remodel" in description.lower()) or ("updated" in description.lower())) else 0
		    print prevhomesales
		    print str(prevhomesales.beds) + "\t" + str(prevhomesales.baths) + "\t" + str(prevhomesales.sqft) + "\t" + str(prevhomesales.year_built) + "\t" + str(prevhomesales.sale_price) + "\t" + str(prevhomesales.city) + "\t" + str(prevhomesales.image_url) + "\t" + str(prevhomesales.zipcode) + "\t" + str(prevhomesales.lot_size) + "\t" + str(prevhomesales.state) + "\t" + str(prevhomesales.remodeled)
		    prevhomesales.save()
	except InvalidOperation:
		num_houses_with_exceptions+=1
	
print "Number of good " + city + " houses: " + str(num_good_houses)
print "Number of exception " + city + " houses: " + str(num_houses_with_exceptions)
