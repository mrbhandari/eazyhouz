import sys,os
import hashlib
import copy
import re
import datetime
import requests
from decimal import *
from numpy import genfromtxt
from numpy import array_str
from django.db import transaction
from django.db.models import get_models, Model
import traceback
import json
your_djangoproject_home="/Users/pradeep/eazyhouz/eazyhouz/mysite/"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
getcontext().prec = 5
from search.models import PrevHomeSales
import django

def same_homes(home, existing_home):
    return home.beds == existing_home.beds and home.baths == existing_home.baths and home.sqft == existing_home.sqft and home.lot_size == existing_home.lot_size and home.zipcode == existing_home.zipcode and home.latitude == existing_home.latitude and home.longitude == existing_home.longitude and home.url == existing_home.url and home.last_sale_date == existing_home.last_sale_date and home.sale_price == existing_home.sale_price and home.address == existing_home.address and home.property_type == existing_home.property_type

def home_exists(existing_homes, home):
    key = home.address + "\t" + home.city
    existing_home = existing_homes.get(key)
    if existing_home:
        return True #same_homes(home,existing_home)
    return False

def get_eazyhouz_hash(home):
	return hashlib.sha1(home.address + home.city).hexdigest()


def normalize_address(address):
    return address.lower().replace(" apt ", " #").replace(" unit "," #").title()

def get_school_type(school_name):
    school_name = school_name.lower();
    if "elementary" in school_name:
        return "elementary"
    if "junior high" in school_name or "middle" in school_name or "intermediate" in school_name:
        return "middle"
    if "high" in school_name:
        return "high"
    return "other"

def good_home(home):
    if home.address and home.sqft and home.sale_price and home.url and home.property_type and home.beds and home.baths and home.city and home.zipcode and home.latitude and home.longitude:
        return True
    return False


def load_all_homes():
	return PrevHomeSales.objects.all()


def download_school_data(id):
	ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'
	headers = {
    	'User-Agent': ua,
	}
	schools = []
	url = "https://www.redfin.com/stingray/phantom/multicontroller?p=/stingray/&u=dataloader/property/" + id + "/schools"
	r = requests.get(url, headers=headers)
	d = json.loads(r.content[4:])
	try:
		try:
			for school in d['payload'][0]['payload']['__root']['__atts'][1]['__atts'][0]:
				schools.append((school['__atts'][1], school['__atts'][-2]))
		except TypeError as e:
			for school in d['payload'][0]['payload']['__root']['__atts'][0]['__atts'][0]:
				schools.append((school['__atts'][1], school['__atts'][-2]))
	except:
		return
	return schools

def get_school_type(school_name):
	school_name = school_name.lower();
	if "elementary" in school_name:
		return "elementary"
	if "junior high" in school_name or "middle" in school_name:
		return "middle"
	if "high" in school_name:
		return "high"
	return "other"

def normalize_property_type(property_type):
    return "Condo/Townhouse" if "condo" in property_type.lower() or "townho" in property_type.lower() else "Single Family Residence"

inserted_homes = {}

print "LOADING EXISTING HOMES"
all_existing_homes = load_all_homes()
for h in all_existing_homes:
	inserted_homes[h.address + "\t" + h.city] = h


print "LOADED ", len(inserted_homes), " homes!"

django.setup()
num_good_homes = 0
num_bad_homes = 0
num_exception_homes = 0
lines = open(sys.argv[1]).readlines()
header_index = {}
for ind in range(0,len(lines)):
	try:
		line1 = {}
		if ind == 0:
			line = lines[ind].split("\t")
			for i in range(0,len(line)):
				header_index[i] = line[i]
			continue
		else:
			line = lines[ind].split("\t")
			for i in range(0,len(line)):
				line1[header_index[i]] = line[i]
		 
		home = PrevHomeSales()
		prevhomesales = PrevHomeSales()
		if line1['ADDRESS']:
			prevhomesales.address = normalize_address(line1['ADDRESS'])
		if "undisclosed" in prevhomesales.address:
			continue
		if line1['BEDS']:
			prevhomesales.beds = line1['BEDS']
		if line1['BATHS']:
			prevhomesales.baths = Decimal(line1['BATHS'])
		if line1['SQFT']:
			prevhomesales.sqft = line1['SQFT']
		if line1['YEAR_BUILT']:
			prevhomesales.year_built = line1['YEAR_BUILT']
		prevhomesales.curr_status = "active" if "active" in line1['STATUS'].lower() else "sold"
		if prevhomesales.curr_status == "sold" and line1['LAST_SALE_PRICE']:
				prevhomesales.sale_price = Decimal(line1['LAST_SALE_PRICE'])
		if prevhomesales.curr_status == "active" and line1['LIST_PRICE']:
			prevhomesales.sale_price = Decimal(line1['LIST_PRICE'])
		if line1['URL']:
			prevhomesales.url = line1['URL']
		if line1['LATITUDE']:
			prevhomesales.latitude = Decimal(line1['LATITUDE'])
		if line1['LONGITUDE']:
			prevhomesales.longitude = Decimal(line1['LONGITUDE'])
		if line1['HOME_TYPE']:
			prevhomesales.property_type = normalize_property_type(line1['HOME_TYPE'])
		if line1['CITY']:
			prevhomesales.city = line1['CITY']
		if line1['STATE']:
			prevhomesales.state = line1['STATE']
		if line1['ZIP']:
			prevhomesales.zipcode = line1['ZIP']
		if line1['LOT_SIZE']:
			prevhomesales.lot_size = line1['LOT_SIZE']
		if prevhomesales.curr_status == "sold" and line1['LAST_SALE_DATE']:
			if '/' in line1['LAST_SALE_DATE']:
				prevhomesales.last_sale_date = datetime.datetime.strptime(line1['LAST_SALE_DATE'], '%m/%d/%y').date()
			else:
				prevhomesales.last_sale_date = datetime.datetime.strptime(line1['LAST_SALE_DATE'], '%Y-%m-%d').date()
		prevhomesales.user_input = False
		id = prevhomesales.url.split("/")[-1]
		if re.match(r'[a-z]+',id):
			id = prevhomesales.url.split("/")[-2]
		if good_home(prevhomesales):
			if not home_exists(inserted_homes, prevhomesales):
				schools = download_school_data(id)
				if schools:
					for school in schools:
						school_type = get_school_type(school[1])
						if school_type == "elementary":
							prevhomesales.elementary = school[0]
							prevhomesales.elem_school_name = school[1]
						if school_type == "middle":
							prevhomesales.middle = school[0]
							prevhomesales.middle_school_name = school[1]
						if school_type == "high":
							prevhomesales.high = school[0]
							prevhomesales.high_school_name = school[1]
						if school_type == "other":
							prevhomesales.other = school[0]
							prevhomesales.other_school_name = school[1]
				print "GOOD HOME:",prevhomesales
		 		num_good_homes += 1
				inserted_homes[prevhomesales.address + "\t" + prevhomesales.city] = prevhomesales
				prevhomesales.eazyhouz_hash = get_eazyhouz_hash(prevhomesales)
				prevhomesales.save()
			else:
				print "EXISTING GOOD HOME:",prevhomesales
		else:
			print "BAD HOME:",prevhomesales
			num_bad_homes += 1
	except Exception as e:
		print "Exception", traceback.format_exc()
		pass
print num_good_homes, num_bad_homes, num_exception_homes
