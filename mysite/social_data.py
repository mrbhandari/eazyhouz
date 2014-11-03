from instagram.client import InstagramAPI
from yelpapi import YelpAPI
import urllib, urllib2
import os, json
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'



def nearby_insta(latitude, longitude):    
    api = InstagramAPI(client_id='e5caa7d1da134dd681db8fd39389f8e7', client_secret='468c71adce01482aa17ca24090c07a1f')
    local_media_search = api.media_search(count=30, lat=latitude, lng=longitude, distance=1000) #min_timestamp, max_timestamp, q
    photos = []
    for media in local_media_search:
        photos.append({'lri': media.images['low_resolution'].url,
                       'sri': media.images['standard_resolution'].url,
                       })
    return photos


yconsumer_key = '6IZDGF5Bck3MP6zU0lFgLQ'
yconsumer_secret	= 'dZR4dJJpYUAETKH82yzv2nkXitM'
ytoken = 'YtSoZfbmiWxfLg87GGoLUsC_wcx8wUtO'
ytoken_secret = 'z9pDq7T0Pa_CwfQOMmF1XM4dhhQ'

yelp_api = YelpAPI(yconsumer_key, yconsumer_secret, ytoken, ytoken_secret)
search_results = yelp_api.search_query(ll="37.5542,-122.3131", limit=10)
json.dumps(search_results)
#business_results = yelp_api.business_query(id=business_id, other_args)

#https://api.instagram.com/v1/media/search?lat=48.858844&lng=2.294351&client_id=e5caa7d1da134dd681db8fd39389f8e7

#
#def instagram_request(lat, lon):
#    baseurl = 'https://api.instagram.com/v1/media/search'
#    values = {'client_id' : Instagram.client_id,
#              'lat' : lat,
#              'lng' : lon }
#    data = urllib.urlencode(values)
#    print data
#    url = baseurl + '?' +data
#    print url
#    return url
#
#def make_request(url):
#    response = urllib2.urlopen(url)
#    reponse_string = response.read()
#    return reponse_string
#
#
#insta_url = instagram_request(lat, lon)
#print insta_url
#
#
#print make_request(insta_url)
