import json
import sys,os
import datetime
from decimal import *
import django
import heapq
from django.forms.models import model_to_dict
import pprint

your_djangoproject_home="/Users/pradeep/eazyhouz/eazyhouz/mysite"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
getcontext().prec = 5
from search.models import *
django.setup()

def home_similarity(home,subject_home):
  return 10 * abs(home.sqft - subject_home.sqft) + 800 * abs(home.sqft - subject_home.sqft)

def gen_appraisal(subject_home):
  data = {}
  city = subject_home.city
  beds = subject_home.beds
  baths = subject_home.baths
  sqft = subject_home.sqft
  min_baths = baths - 0.5
  max_baths = baths + 0.5
  min_sqft = sqft * 0.8
  max_sqft = sqft * 1.2
  last_sale_date_threshold = "2014-01-01"
  #TODO make sure to not fetch the subject home itself.
  comp_candidates = PrevHomeSales.objects.filter(beds__exact=beds, baths__lte=max_baths, baths__gte=min_baths, sqft__lte=max_sqft,sqft__gte=min_sqft,city__exact=city,last_sale_date__gte=last_sale_date_threshold).exclude(user_input__exact=1)
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
    avg_sqft_price += home.sale_price/home.sqft
    data['home' + str(i)] = model_to_dict(home)
  avg_sqft_price /= k
  data['estimated_price'] = avg_sqft_price * subject_home.sqft
  for i in range(1,k+1):
    adjustment = {}
    print str(i) + "th home's sqft" +  str(data['home' + str(i)]['sqft'])
    adjustment['sqft'] = avg_sqft_price * (subject_home.sqft - data['home'+str(i)]['sqft'])
    data['adjustment' + str(i)] = adjustment
  return data


prevHome = PrevHomeSales()
prevHome.beds = 2
prevHome.city = "san mateo"
prevHome.baths = 2.0
prevHome.sqft=1693
data = gen_appraisal(prevHome)
pp = pprint.PrettyPrinter(indent=4)
print pp.pprint(data)

