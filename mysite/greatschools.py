import re
import urllib2
from bs4 import BeautifulSoup
import sys,os
import django
import datetime
from django.db.models import Count
your_djangoproject_home="/Users/pradeep/eazyhouz/eazyhouz/mysite"
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from search.models import *

django.setup()

def get_school_data(url):
	school_data = []
	data = urllib2.urlopen(url).read()
	soup = BeautifulSoup(data)
	elements = soup.findAll("div",{"class":"mod standard_1-1"})
	for e in elements:
		if e.find("div",{"class":"js-school-search-result-name"}):
			school_name = e.find("div",{"class":"js-school-search-result-name"}).text
			school_rating = e.findAll("span",{"class": re.compile(r'rating*')})[0].get("class")[1].split("-")[-1]
			school_data.append((school_name,school_rating))
	return school_data

def insert_school_data(url, school_type, city):
	school_data = get_school_data(url)
	for s in school_data:
		if s[1].isdigit():
			school = School()
			school.city = city
			school.state = "CA"
			school.school_name = s[0]
			school.school_rating = s[1]
			school.school_type = school_type
			print school.city,school.state,school.school_name,school.school_rating,school.school_type
			school.save()

def get_distinct_cities():
	return PrevHomeSales.objects.all().values('city').annotate(total=Count('city'))

#print "hi"
cities = get_distinct_cities()
#cities=[]
	
for c in cities:
	city = c.get("city")
	elem_url="http://www.greatschools.org/california/" + city.replace(" ","-") + "/schools/?st=public&gradeLevels=e&pageSize=100"
	middle_url="http://www.greatschools.org/california/" + city.replace(" ","-") + "/schools/?st=public&gradeLevels=m&pageSize=100"
	high_url="http://www.greatschools.org/california/" + city.replace(" ","-") + "/schools/?st=public&gradeLevels=h&pageSize=100"
	insert_school_data(elem_url,"elementary",city)
	insert_school_data(middle_url,"middle",city)
	insert_school_data(high_url,"high",city)




