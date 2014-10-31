#Import data for a given address and citystatzip from zillow

import urllib, urllib2, xmltodict
from decimal import *
import datetime
import os
from address import AddressParser, Address

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from search.models import PrevHomeSales

#forms the URL request for Zillow
def zformrequest(raw_address, raw_citystatezip):
    baseurl = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm'
    values = {'zws-id' : 'X1-ZWz1dyahf20tu3_634pb',
              'address' : raw_address,
              'citystatezip' : raw_citystatezip }
    data = urllib.urlencode(values)
    url = urllib2.Request(baseurl, data)
    return url

#takes a url, returns XML string
def request(url):
    response = urllib2.urlopen(url)
    url_xml_string = response.read()
    return url_xml_string


#takes xml_string and returns a prevHomeSales model-like object which can be passed into the
def parse_zhome_attr(url_xml_string):
    testd = xmltodict.parse(url_xml_string)
    parsed_home_attr = testd
    return parsed_home_attr

#pulls all the fuctions together
def return_zhome_attr(raw_address, raw_citystatezip):
    
    url = zformrequest(raw_address, raw_citystatezip)
    url_xml_string = request(url)
    
    output = parse_zhome_attr(url_xml_string)
    print output
    
    #TODO this needs to be its own function
    
    result = output['SearchResults:searchresults']['response']['results']['result']
    print result
    prevhomesales = PrevHomeSales()
    prevhomesales.beds = result.get('bedroom', None)
    print prevhomesales.beds
    
    print "DID THIS EXECUTE"
    
    prevhomesales.baths = result.get('bathrooms', None)
    print prevhomesales.baths
    
    prevhomesales.sqft =result.get('finishedSqFt', None)
    print prevhomesales.sqft
    
    prevhomesales.year_built =result.get('yearBuilt', None)
    print prevhomesales.year_built
    
    prevhomesales.sale_price = Decimal(result.get('lastSoldPrice', None).get('#text', None))
    print prevhomesales.sale_price
    
    prevhomesales.url = result.get('links', None).get('homedetails', None)
    print prevhomesales.url
    
    prevhomesales.image_url = None
    
    prevhomesales.latitude = Decimal(result.get('address', None).get('latitude', None))
    print prevhomesales.latitude
    
    prevhomesales.longitude = Decimal(result.get('address', None).get('longitude', None))
    print prevhomesales.longitude
    
    prevhomesales.city = result['address']['city']
    print prevhomesales.city
    
    prevhomesales.state = result['address']['state']
    print prevhomesales.state
    
    prevhomesales.zipcode = result['address']['zipcode']
    print prevhomesales.zipcode
    
    prevhomesales.address = result['address']['street']
    print prevhomesales.address
    
    prevhomesales.home_type = result.get('useCose', None)
    print prevhomesales.home_type
    
    #TODO
    #prevhomesales.remodeled
    #prevhomesales.interior_rating
    #prevhomesales.interior_rating
    #prevhomesales.elementary
    #prevhomesales.middle
    #prevhomesales.high
    
    prevhomesales.lot_size = result.get('lotSizeSqFt', None)
    print prevhomesales.lot_size
    
    lastSoldDate = result.get('lastSoldDate', None)
    if len(lastSoldDate) > 0:
        prevhomesales.last_sale_date = datetime.datetime.strptime(lastSoldDate, '%m/%d/%Y').date()
        print prevhomesales.last_sale_date
    
    prevhomesales.user_input = True
    
    
    
    prevhomesales.last_zestimate = Decimal(result.get('zestimate', None).get('amount', None).get('#text', None))
    print prevhomesales.last_zestimate
    
    
    from django.core.exceptions import ValidationError
    try:
        prevhomesales.full_clean()
    except ValidationError as e:
        print e
        pass
    
    
    print "TEST1"
    prevhomesales.save()
    print "TEST2"
    #TODO: does not check if this record already exists just saves it
    return prevhomesales
    


#places: https://graph.facebook.com/search?q=&type=place&center=37.56166,-122.318908&distance=100&access_token=CAACEdEose0cBACopUWkMgy2d3JgFbPmZCP2u5A4vn9rmhhJKpbsXgdRfuM41SBj2JRHrcD6gY3Mw0aQoRFqpfL0eOEBx9o3t99EWJohpZBEr3S58wV73vvdwM0m7yZAR9ue24ZAZCBsZAdp6A1GG9OeKCLkD6RYRwv6ROiobr5s8UUqMWhSWGJXjyeLtZC1DZCCK9V7NHLmejDSqoZAhhCU3g
    
#raw_address = raw_input("Please enter something: ")
#raw_citystatezip = raw_input("Please enter something: ")
#
#ap = AddressParser()
#address = ap.parse_address(raw_address)
#input_street_address = "{0} {1} {2} {3}".format(address.house_number, address.street_prefix, address.street, address.street_suffix)
#input_citystatezip = "{0} {1} {2}".format(address.city, address.state, address.zip)
#print input_street_address
#print input_citystatezip
#print address.full_address()





