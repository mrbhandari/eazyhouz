import json
import sys,os
import datetime
from decimal import *
import datetime
import re
your_djangoproject_home="/Applications/MAMP/htdocs/eazyhouz/mysite"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django
django.setup()
from search.models import PrevHomeSales

filename = sys.argv[1]
houses = []
houses.extend(json.load(open(filename)))

rating = {}
if len(sys.argv) > 2:
	filename = sys.argv[2]
	lines = [line.strip() for line in open(filename)]
	for l in lines:
		if not "N" in l.split("\t")[6].split(" ")[0]:
			rating[l.split("\t")[1]] = l.split("\t")[6].split(" ")[0]

def good_house(house):
    return bool(house.get("beds")) and bool(house.get("baths")) and bool(house.get("address")) and bool(house.get("zipcode")) and bool(house.get("state")) and bool(house.get("city")) and bool(house.get("price")) and bool(house.get("sqft")) and bool(house.get("last_sold_date")) and bool(house.get("latitude")) and bool(house.get("longitude"))

def get_property_type(house):
	ptype = "Single Family Residence"
	if house.get("description"):
		if re.match(r'.*condo.*|.*townhome.*|.*condominium.*|.*townhouse.*',house.get("description").lower()):
			return "Condo/Townhouse"
	if house.get("house_features"):
 		for k in house.get("house_features").keys():
			if re.match(r'.*condo.*|.*townhome.*|.*condominium.*|.*townhouse.*',house.get("house_features").get(k).lower()):
				return "Condo/Townhouse"
	if re.match(r'.*#[0-9].*',house.get("address")):
		return "Condo/Townhouse"
	return ptype

num_good_houses = 0
num_houses_with_exceptions = 0
for house in houses:
	try:
		if good_house(house):
			house_city = house.get("city").lower().replace(",","")
			if house_city:
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
				if prevhomesales.sqft is None:
					continue
				if prevhomesales.sqft == "0":
					continue
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
				if lot_size and re.match("^[0-9]*$",lot_size):
					prevhomesales.lot_size = lot_size
				description = house.get("description")
				prevhomesales.latitude = house.get("latitude")
				prevhomesales.longitude = house.get("longitude")
				last_sale_date = house.get("last_sold_date")
				if rating.get(house.get("url")):
					prevhomesales.interior_rating=rating[house.get("url")]
				if last_sale_date:
					if len(last_sale_date) == 8:
						prevhomesales.last_sale_date = datetime.datetime.strptime(last_sale_date,'%m/%d/%y').date()
				if len(last_sale_date) == 10:
					prevhomesales.last_sale_date = datetime.datetime.strptime(last_sale_date,'%m/%d/%Y').date()
				curr_status = house.get("status")
				prevhomesales.curr_status = "sold"
				if curr_status and "active" in curr_status.lower():
					prevhomesales.curr_status = "active"
				if description:
					prevhomesales.remodeled = 1 if (("remodel" in description.lower()) or ("updated" in description.lower())) else 0
				prevhomesales.property_type = get_property_type(house)
				print "GOOD HOME:" + str(prevhomesales)
				print str(prevhomesales.beds) + "\t" + str(prevhomesales.baths) + "\t" + str(prevhomesales.sqft) + "\t" + str(prevhomesales.year_built) + "\t" + str(prevhomesales.sale_price) + "\t" + str(prevhomesales.city) + "\t" + str(prevhomesales.image_url) + "\t" + str(prevhomesales.zipcode) + "\t" + str(prevhomesales.lot_size) + "\t" + str(prevhomesales.state) + "\t" + str(prevhomesales.remodeled) + "\t" + str(prevhomesales.latitude) + "\t" + str(prevhomesales.longitude),"\t",prevhomesales.interior_rating
				prevhomesales.save()
		else:
			print "BAD HOME:" + str(house)
	except (InvalidOperation,ValueError) as e:
		num_houses_with_exceptions+=1

print "Number of good houses: " + str(num_good_houses)
print "Number of exception  houses: " + str(num_houses_with_exceptions)
