import math
import sys,os
import simplejson as json
import django
import datetime
import logging
from decimal import *
from django.db.models import Q
your_djangoproject_home="/Users/pradeep/eazyhouz/eazyhouz/mysite"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from search.models import *
django.setup()

from mysite.views import gen_appraisal

from django.db.models.base import ModelState

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
       if hasattr(obj, 'isoformat'):
           return obj.isoformat()
       elif isinstance(obj, decimal.Decimal):
           return float(obj)
       elif isinstance(obj, ModelState):
           return None
       else:
           return json.JSONEncoder.default(self, obj)

def get_homes():
	return PrevHomeSales.objects.filter(Q(last_sale_date__gte="2014-09-01") | Q(curr_status="active"))

homes = get_homes()
ctr = 0
for home in homes:
	cma = CMA()
	cma.eazyhouz_hash_source = home.eazyhouz_hash
	today = True if home.curr_status == "active" else False
	data = gen_appraisal(home, today)
	cma.cma_dict = json.dumps(data, cls=DateTimeEncoder)
	cma.todays_prediction = today
	cma.save()
	ctr += 1
	if ctr %10 == 0:
		print ctr, " homes processed"
