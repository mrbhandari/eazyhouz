import json
import sys,os
import datetime
from decimal import *
import django
import heapq
from django.forms.models import model_to_dict
import pprint
import math
from random import shuffle
from django.db.models import Count

your_djangoproject_home="/Users/pradeep/eazyhouz/eazyhouz/mysite"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
getcontext().prec = 5
from search.models import *
django.setup()

def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    cos = min(1,max(cos,-1))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return 3960*arc



def home_similarity(home,subject_home):
   distance = distance_on_unit_sphere(float(home.latitude), float(home.longitude), float(subject_home.latitude), float(home.longitude))
   return 10 * abs(home.sqft - subject_home.sqft) + 800 * abs(float(home.baths) - float(subject_home.baths)) + 50 * distance #+ 10 * abs(home.year_built - subject_home.year_built)

def gen_appraisal(subject_home):
  data = {}
  city = subject_home.city
  beds = subject_home.beds
  baths = subject_home.baths
  sqft = subject_home.sqft
  min_baths = baths - Decimal(0.5)
  max_baths = baths + Decimal(0.5)
  min_sqft = sqft * 0.8
  max_sqft = sqft * 1.2
  last_sale_date_threshold = "2014-01-01"
  #TODO make sure to not fetch the subject home itself.
  comp_candidates = PrevHomeSales.objects.filter(beds__exact=beds, baths__lte=max_baths, baths__gte=min_baths, sqft__lte=max_sqft,sqft__gte=min_sqft,city__exact=city,last_sale_date__gte=last_sale_date_threshold).exclude(user_input__exact=1).exclude(id__exact=subject_home.id)
  h = []
  if len(comp_candidates) < 3:
     return data
  for c in comp_candidates:
    sim_score = home_similarity(c,subject_home)
    heapq.heappush(h,(sim_score,c))
  k = 3
  avg_sqft_price = 0
  
  for i in range(1,k+1):
    sim_score,home = heapq.heappop(h)
    print i,home,home.id
    avg_sqft_price += home.sale_price/home.sqft
    dist = distance_on_unit_sphere(float(subject_home.latitude),float(subject_home.longitude),float(home.latitude),float(home.longitude))

    data['home' + str(i)] = model_to_dict(home)
    data['distance' + str(i)] = dist
  avg_sqft_price /= k
  data['estimated_price'] = avg_sqft_price * subject_home.sqft
  for i in range(1,k+1):
    adjustment = {}
    adjustment['sqft'] = avg_sqft_price * (subject_home.sqft - data['home'+str(i)]['sqft'])
    data['adjustment' + str(i)] = adjustment
  return data


def get_recent_sales(subject_home):
  city = subject_home.city
  beds = subject_home.beds
  baths = subject_home.baths
  sqft = subject_home.sqft
  min_baths = Decimal(baths) - Decimal(0.5)
  max_baths = Decimal(baths) + Decimal(0.5)
  min_sqft = sqft * 0.8
  max_sqft = sqft * 1.2
  last_sale_date_threshold = "2014-01-01"
  h = []
  comp_candidates = PrevHomeSales.objects.filter(beds__exact=beds, baths__lte=max_baths, baths__gte=min_baths, sqft__lte=max_sqft,sqft__gte=min_sqft,city__exact=city,last_sale_date__gte=last_sale_date_threshold).exclude(user_input__exact=1).exclude(id__exact=subject_home.id)[:20]
  for c in comp_candidates:
    sim_score = home_similarity(c,subject_home)
    comp_house = model_to_dict(c)
    comp_house["sim_score"] = sim_score
    print c.latitude,c.longitude
    dist = distance_on_unit_sphere(float(subject_home.latitude),float(subject_home.longitude),float(c.latitude),float(c.longitude))
    comp_house["distance"] = dist
    heapq.heappush(h,comp_house)
  comp_candidates_with_sim = []
  for i in range(0,len(comp_candidates)):
    comp_home = heapq.heappop(h)
    comp_candidates_with_sim.append(comp_home)
  return comp_candidates_with_sim

def get_best_value_homes(zipcode, low_percent, high_percent, multiplier=1):
	all_homes_in_zip = PrevHomeSales.objects.filter(curr_status__exact="active",zipcode__exact=zipcode)
	best_homes = []
	h = []
	ctr = 0
	for home in all_homes_in_zip:
		data = gen_appraisal(home)
		list_price = home.sale_price
		predicted_price = data.get("estimated_price")
		if not predicted_price:
			continue
		error = list_price/(predicted_price + 0.0) - 1
		if error >= low_percent and error <= high_percent:
			heapq.heappush(h,(multiplier*error,error, predicted_price,home))
			ctr += 1
	for i in range(0,ctr):
		error_key,error, predicted_price, home = heapq.heappop(h)
		d = {}
		d["home"] = home
		d["list_price"] = home.sale_price
		d["error"] = error
		d["predicted_price"] = predicted_price
		best_homes.append(d)
	return best_homes
#
#all_homes = PrevHomeSales.objects.filter(curr_status__exact="active")
#ctr = 0
#k=10000
#for home in all_homes:
#	data = gen_appraisal(home)
#	orig_price = home.sale_price
#	predicted_price=-1
#	if data.get('estimated_price'):
#		predicted_price=data.get('estimated_price')
#	if predicted_price == -1:
#		continue
#	error = orig_price/(predicted_price + 0.0) - 1
#	print home, "\t", orig_price, "\t", predicted_price,"\t", error, "\t", data.get("home1"), "\t", data.get("distance1"), "\t", data.get("home2"), "\t", data.get("distance2"), "\t", data.get("home3"), "\t", data.get("distance3")
#	ctr += 1
#	if ctr >= k:
#		break
#
def get_distinct_zipcodes():
	return PrevHomeSales.objects.filter(curr_status__exact="active").values('zipcode').annotate(total=Count('zipcode')).filter(total__gte=10)
			

print "distinct zipcodes"
print get_distinct_zipcodes()

print get_best_value_homes("94401", 0, 1, -1)
