import sys,os
import copy
import re
import datetime
from decimal import *
from numpy import genfromtxt
from numpy import array_str
from django.db import transaction
from django.db.models import get_models, Model
import traceback
your_djangoproject_home="/Users/pradeep/eazyhouz/eazyhouz/mysite/"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
getcontext().prec = 5
from search.models import PrevHomeSales
import django


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

filename = sys.argv[1]

lines = open(filename).readlines()
school_names_data = {}
school_scores_data = {}

school_names = {}
school_scores = {}
previous_id = ""
previous_address = ""
for line in lines:
    line = line.strip()
    address = normalize_address(line.split("\t")[1])
    school_name = line.split("\t")[4]
    school_type = get_school_type(school_name)
    school_score = line.split("\t")[3]
    id = line.split("\t")[0].strip()
    
    if id != previous_id:
        school_names_data[previous_id] = copy.deepcopy(school_names)
        school_scores_data[previous_id] = copy.deepcopy(school_scores)
        previous_id = id
        previous_address = address
        school_names = {}
        school_scores = {}

    if not school_names.get(school_type) or school_scores.get(school_type) < school_score:
        school_names[school_type] = school_name
        school_scores[school_type] = school_score
if len(school_names) > 0:
    school_names_data[previous_id] = school_names
    school_scores_data[previous_id] = school_scores


print "SCHOOL DATA", len(school_names_data), len(school_scores_data)

def normalize_property_type(property_type):
    return "Condo/Townhouse" if "condo" in property_type.lower() or "townho" in property_type.lower() else "Single Family Residence"

django.setup()
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
         
        #line1 = lines[ind]
        home = PrevHomeSales()
        prevhomesales = PrevHomeSales()
        if line1['BEDS']:
            prevhomesales.beds = line1['BEDS']
        if line1['BATHS']:
            prevhomesales.baths = Decimal(line1['BATHS'])
        if line1['SQFT']:
            prevhomesales.sqft = line1['SQFT']
        if line1['YEAR_BUILT']:
            prevhomesales.year_built = line1['YEAR_BUILT']
        if line1['LIST_PRICE']:
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
        #if line1['LAST_SALE_DATE']:
        #    if '/' in line1['LAST_SALE_DATE']:
        #        prevhomesales.last_sale_date = datetime.datetime.strptime(line1['LAST_SALE_DATE'], '%m/%d/%y').date()
        #    else:
        #        prevhomesales.last_sale_date = datetime.datetime.strptime(line1['LAST_SALE_DATE'], '%Y-%m-%d').date()
        if line1['ADDRESS']:
            prevhomesales.address = normalize_address(line1['ADDRESS'])
        prevhomesales.user_input = False
        prevhomesales.curr_status="active"
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
        if good_home(prevhomesales):
            print "GOOD HOME:",prevhomesales
            num_good_homes += 1
            prevhomesales.save()
        else:
            print "BAD HOME:",prevhomesales
            num_bad_homes += 1
    except Exception as e:
        print "Exception", traceback.format_exc()
        pass
print num_good_homes, num_bad_homes, num_exception_homes
