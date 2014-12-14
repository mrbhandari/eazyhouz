import math
import sys,os
import heapq
import time
import numpy
import django
import datetime
from django.db.models import Count
from django.db.models import Q
from django.forms.models import model_to_dict
import logging
from random import shuffle
from decimal import *
your_djangoproject_home="/Users/pradeep/eazyhouz/eazyhouz/mysite"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from search.models import *
from mysite.views import gen_appraisal
django.setup()

def get_homes_to_evaluate(k=1000,city="Monterey"):
	return PrevHomeSales.objects.filter(last_sale_date__gte="2014-09-01").exclude(curr_status__exact="active").filter(Q(city__exact=city))[:k]

def get_error_rates_for_city(city="Cupertino"):
	errors = []
	all_homes = get_homes_to_evaluate(10000,city)
	num_houses_lesser_than_20_error = 0
	num_houses_lesser_than_10_error = 0
	num_houses_lesser_than_5_error = 0
	print len(all_homes), " homes to evaluate on"

	for home in all_homes:
		data = gen_appraisal(home, False)
		print "\n\nSUBJECT_HOME", home.address, "\t", home.url, "\t", home.zipcode, "\t", home.property_type, "\t",home.city,"\t",home.interior_rating, "\t",data.get("estimated_price")
		orig_price = home.sale_price
		predicted_price=-1
		if data.get('estimated_price'):
			predicted_price=data.get('estimated_price')
		if predicted_price == -1:
			continue
		error = orig_price/(predicted_price + 0.0) - 1
		print "ERROR_RATE:","\t",error, "\t", orig_price, "\t", predicted_price, "\t", home.address, "\t", home.url, "\t", home.zipcode, "\t", home.property_type, "\t",home.city,"\t",data.get("use_low_sim_homes"),"\t",(0.0 + max(data["adjusted_home_value1"],data["adjusted_home_value2"],data["adjusted_home_value3"]))/min(data["adjusted_home_value1"],data["adjusted_home_value3"],data["adjusted_home_value3"]),"\t",home.interior_rating, "\t", max(data["similarity1"],data["similarity2"],data["similarity3"]), "\t", min(data["similarity1"],data["similarity2"],data["similarity3"]) 
		print data
		print data["home1"].get("address"), "\t", data["home1"].get("url"), "\t", data["home1"].get("zipcode"), "\t", data["home1"].get("property_type"),"\t",data["similarity1"]
		print data["home2"].get("address"), "\t", data["home2"].get("url"), "\t", data["home2"].get("zipcode"), "\t", data["home2"].get("property_type"),"\t",data["similarity2"]
		print data["home3"].get("address"), "\t", data["home3"].get("url"), "\t", data["home3"].get("zipcode"), "\t", data["home3"].get("property_type"),"\t",data["similarity3"]
		if abs(error) <= 0.2:
			num_houses_lesser_than_20_error += 1
		if abs(error) <= 0.1:
			num_houses_lesser_than_10_error += 1
		if abs(error) <= 0.05:
			num_houses_lesser_than_5_error += 1
		errors.append(abs(error))
    
	num_houses = len(errors)
	median_error_rate = numpy.median(numpy.array(errors))
	num_houses_20_percent_error_rate = num_houses_lesser_than_20_error/(0.0 + num_houses) 
	num_houses_10_percent_error_rate = num_houses_lesser_than_10_error/(0.0 + num_houses) 
	num_houses_5_percent_error_rate = num_houses_lesser_than_5_error/(0.0 + num_houses) 
	print "CITY ERROR\t", city, "\t", len(all_homes), "\t", num_houses, "\t", num_houses_20_percent_error_rate,"\t",num_houses_10_percent_error_rate, "\t", median_error_rate,"\t", num_houses_5_percent_error_rate, "\t", num_houses/(0.0 + len(all_homes))


def get_distinct_cities_with_k_active_houses(k=10):
	return PrevHomeSales.objects.filter(curr_status__exact="sold",last_sale_date__gte="2014-09-01").values('city').annotate(total=Count('city')).filter(total__gte=k)


def get_single_home_appraisal(id="1234"):
	return PrevHomeSales.objects.filter(id__exact=id)

cities = get_distinct_cities_with_k_active_houses()
cities = [{"city":"San carlos"}]
ctr = 0;
for city in cities:
	get_error_rates_for_city(city.get("city"))
	ctr += 1
	if ctr >= 10:
		break

#home = get_single_home_appraisal(id=2163622)

#print gen_appraisal(home[0], True)
