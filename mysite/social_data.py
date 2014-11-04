from instagram.client import InstagramAPI
from yelpapi import YelpAPI
from twitter import *
import urllib, urllib2
import os, json
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
rdist = 1000
sanmateo= "37.561667,-122.318908"
bixby = "35.9608,-95.8783"


def nearby_insta(latitude, longitude):
    #https://github.com/Instagram/python-instagram
    api = InstagramAPI(client_id='e5caa7d1da134dd681db8fd39389f8e7', client_secret='468c71adce01482aa17ca24090c07a1f')
    local_media_search = api.media_search(count=30, lat=latitude, lng=longitude, distance=rdist)
    #other params: min_timestamp, max_timestamp, q
    photos = []
    for media in local_media_search:
        photos.append({'lri': media.images['low_resolution'].url,
                       'sri': media.images['standard_resolution'].url,
                       })
    return photos

def nearby_yelp(latitude, longitude):
    #from https://github.com/gfairchild/yelpapi
    #doc: http://www.yelp.com/developers/documentation/v2/search_api
    #Sort mode: 0=Best matched (default), 1=Distance, 2=Highest Rated
    
    yconsumer_key = '6IZDGF5Bck3MP6zU0lFgLQ'
    yconsumer_secret	= 'dZR4dJJpYUAETKH82yzv2nkXitM'
    ytoken = 'YtSoZfbmiWxfLg87GGoLUsC_wcx8wUtO'
    ytoken_secret = 'z9pDq7T0Pa_CwfQOMmF1XM4dhhQ'
    max_yelp_radius = 10000
    
    yelp_api = YelpAPI(yconsumer_key, yconsumer_secret, ytoken, ytoken_secret)
    llvar = str(latitude) + ',' + str(longitude)
    
    search_results = yelp_api.search_query(ll=llvar, limit=20, sort=0, radius_filter=rdist)
    
    #Make certain the farthest away places are still within your radius
    for i in search_results.get('businesses'):
        if i.get('distance') > max_yelp_radius:
            index = search_results.get('businesses').index(i) #find the index of it
            del search_results.get('businesses')[index]
            
    return search_results



consumer_key = "O5Z1KINSBaDEQgTBB3FA"
consumer_secret = "kf42pzVoDrmP4hoe9LNQW5t765J2zEspqdHQhotw"
access_key = "2172397754-TrCNJSgVarJIMnYb6uLXFzfI76zI7m8cfy5zIvL"
access_secret = "FNiDwwbgs0WiElgaJ2hVECnsyavUKIQ3IP7JNr4BkiOhx"# create twitter API object
auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
twitter = Twitter(auth = auth)
tradius = str(rdist/1000)+"km"

def nearby_twitter(latitude, longitude, radius=tradius):
    geocode = "%s,%s,%s" % (latitude, longitude, radius)
    query = twitter.search.tweets(geocode = geocode, count=100)
    tweets = []
    for result in query["statuses"]:
        tweets.append(result.get("text"))
    return tweets

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
