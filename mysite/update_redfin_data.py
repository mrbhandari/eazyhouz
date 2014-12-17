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
django.setup()

def same_homes(home, existing_home):
	return home.beds == existing_home.beds and home.baths == existing_home.baths and home.sqft == existing_home.sqft and home.lot_size == existing_home.lot_size and home.zipcode == existing_home.zipcode and home.latitude == existing_home.latitude and home.longitude == existing_home.longitude and home.url == existing_home.url and home.last_sale_date == existing_home.last_sale_date and home.sale_price == existing_home.sale_price and home.address == existing_home.address and home.property_type == existing_home.property_type


def update_existing_home(existing_home, home):
	updated = False
	if home.curr_status and not (existing_home.curr_status and existing_home.curr_status == home.curr_status):
		existing_home.curr_status = home.curr_status
		updated = True
	if home.sale_price and not (existing_home.sale_price and existing_home.sale_price == home.sale_price):
		existing_home.sale_price = home.sale_price
		updated = True
	if home.last_sale_date and not (existing_home.last_sale_date and existing_home.last_sale_date == home.last_sale_date):
		existing_home.last_sale_date =  home.last_sale_date
		updated = True
	if updated:
		print "UPDATED EXISTING HOME:", existing_home.address, existing_home.last_sale_date, existing_home.sale_price, existing_home.curr_status
		existing_home.save()
	else:
		print "NO CHANGE IN EXISTING HOME:", existing_home.address

def home_exists(existing_homes, home):
	key = home.address + "\t" + home.city
	existing_home = existing_homes.get(key)
	if existing_home:
		return existing_home #same_homes(home,existing_home)
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


def load_all_active_homes():
	return PrevHomeSales.objects.all()

lines = open(sys.argv[1]).readlines()
school_names_data = {}
school_scores_data = {}

school_names = {}
school_scores = {}
previous_id = ""
for line in lines:
	line = line.strip()
	school_name = line.split("\t")[4]
	school_type = get_school_type(school_name)
	school_score = line.split("\t")[3]
	id = line.split("\t")[0].strip()
	
	if id != previous_id:
		school_names_data[previous_id] = copy.deepcopy(school_names)
		school_scores_data[previous_id] = copy.deepcopy(school_scores)
		previous_id = id
		school_names = {}
		school_scores = {}

	if not school_names.get(school_type) or school_scores.get(school_type) < school_score:
		school_names[school_type] = school_name
		school_scores[school_type] = school_score
if len(school_names) > 0:
	school_names_data[previous_id] = school_names
	school_scores_data[previous_id] = school_scores

print "SCHOOL DATA", len(school_names_data), len(school_scores_data)

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
all_existing_homes = load_all_active_homes()
for h in all_existing_homes:
	inserted_homes[h.address + "\t" + h.city] = (h, "existing")

print "LOADED ", len(inserted_homes), " homes!"

num_good_homes = 0
num_bad_homes = 0
num_exception_homes = 0
lines = open(sys.argv[2]).readlines()
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
		prevhomesales.curr_status = line1['STATUS'].lower()
		if not prevhomesales.curr_status and line1['LAST_SALE_PRICE']:
			prevhomesales.curr_status = "sold"
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
		if school_names_data.get(id):
			school_names = school_names_data.get(id)
			school_scores = school_scores_data.get(id)
			for k in school_names.keys():
				if k == "elementary":
					prevhomesales.elementary = school_scores[k]
					prevhomesales.elem_school_name = school_names[k]
				if k == "middle":
					prevhomesales.middle = school_scores[k]
					prevhomesales.middle_school_name = school_names[k]
				if k == "high":
					prevhomesales.high = school_scores[k]
					prevhomesales.high_school_name = school_names[k]
				if k == "other":
					prevhomesales.other_school_rating = school_scores[k]
					prevhomesales.other_school_name = school_names[k]
		existing_home_data = home_exists(inserted_homes, prevhomesales)
		if existing_home_data == False:
			if good_home(prevhomesales):
				print "GOOD NEW HOME:",prevhomesales
		 		num_good_homes += 1
				prevhomesales.eazyhouz_hash = get_eazyhouz_hash(prevhomesales)
				prevhomesales.save()
				inserted_homes[prevhomesales.address + "\t" + prevhomesales.city] = (prevhomesales, "new")
			else:
				print "NEW BAD HOME:",prevhomesales
				num_bad_homes += 1
		else:
			update_existing_home(existing_home_data[0], prevhomesales)
	except Exception as e:
		print "Exception", traceback.format_exc()
		pass
print num_good_homes, num_bad_homes, num_exception_homes
