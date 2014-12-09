from instagram.client import InstagramAPI
from yelpapi import YelpAPI
from twitter import *
from foursquare import Foursquare
import urllib, urllib2, simplejson
import os, json
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
rdist = 1000
tradius = str(rdist/1000)+"km"
sanmateo= "37.561667,-122.318908"
bixby = "35.9608,-95.8783"
import eventful

def nearby_image(latitude,longitude):
    img_url = """https://maps.googleapis.com/maps/api/streetview?size=400x400&location=%s,%s8&key=AIzaSyBYVngMReah5qDa3j-ZZqpwkvxJ-7gYecs""" % (latitude, longitude)
    print "PRINTING IMG: %s" % img_url
    return img_url

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
    
    print YelpAPI(yconsumer_key, yconsumer_secret, ytoken, ytoken_secret)
    
    yelp_api = YelpAPI(yconsumer_key, yconsumer_secret, ytoken, ytoken_secret)
    llvar = str(latitude) + ',' + str(longitude)
    
    search_results = yelp_api.search_query(ll=llvar, limit=20, sort=0, radius_filter=rdist)
    
    #Make certain the farthest away places are still within your radius
    for i in search_results.get('businesses'):
        if i.get('distance') > max_yelp_radius:
            index = search_results.get('businesses').index(i) #find the index of it
            del search_results.get('businesses')[index]
            
    return search_results

def nearby_twitter(latitude, longitude, radius=tradius):
    consumer_key = "O5Z1KINSBaDEQgTBB3FA"
    consumer_secret = "kf42pzVoDrmP4hoe9LNQW5t765J2zEspqdHQhotw"
    access_key = "2172397754-TrCNJSgVarJIMnYb6uLXFzfI76zI7m8cfy5zIvL"
    access_secret = "FNiDwwbgs0WiElgaJ2hVECnsyavUKIQ3IP7JNr4BkiOhx"# create twitter API object
    auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
    twitter = Twitter(auth = auth)
    geocode = "%s,%s,%s" % (latitude, longitude, radius)
    query = twitter.search.tweets(geocode = geocode, count=8)
    tweets = []
    for result in query["statuses"]:
        tweets.append(result.get("text"))
    return tweets

def nearby_foursquare(latitude, longitude, radius=rdist):
    fsclient_id = 'LVMG0AY1BFF5AJFPS0GJEF2MD4G4PB4OYDRJVZ4NJDC3PSRK'
    fsclient_secret = 'M5A2YFXKFKWHAMRX10430ZWUOH5VFOGDBTL42H5WPYYVG5R5'
    client = Foursquare(client_id=fsclient_id,
            client_secret=fsclient_secret,)
    
    params = {
        'll': ('%s,%s' % (latitude, longitude)),
        #'categoryId': '4d4b7105d754a06378d81259',
        'limit': 50,
        'radius': radius,
    }
    response = client.venues.search(params)
    fscheckins = []

    #Filtering for high quality: make sure atleast 5% of users in area checked in here
    #percent_of_total = .05
    #totaluserCount = response.get('venues')[0].get('stats').get('usersCount')
    #totaluserCount = response.get('venues')[0]
    #print totaluserCount
    #actual_venues = response.get('venues')[2:len(response.get('venues'))]#skips the first response which is always meta data
    #print response
    for i in response.get('venues'): 
        fsvenue = {}
        userCount = i.get('stats').get('usersCount')
        if userCount > 30:
            #print i
            fsvenue['name'] = i.get('name')
            fsvenue['usersCount'] = userCount
            fsvenue['checkinsCount'] = i.get('stats').get('checkinsCount')
            fsvenue['repeatRatio'] = fsvenue['checkinsCount'] / fsvenue['usersCount']
            fsvenue['url'] = i.get('url')
            #print i.get('popular')
            #print i.get('hereNow')
            #print i.get('tips')
            #print i.get('tags')
            #print i.get('photos')
            try:
                index_value = i.get('categories')[0].get('shortName')
            except (ValueError, IndexError):
                index_value = None
            fsvenue['category'] = index_value
            fscheckins.append(fsvenue)
    return fscheckins
    
def nearby_eventful(latitude, longitude, radius=rdist):
    api = eventful.API('Jk6L9pr5QZfBz3Tb')
    geocode = "%s,%s" % (latitude, longitude)
    events = api.call('/events/search', location=geocode, within=(radius/1000), units="km")
    
    resultevents = []
    try:
        for event in events['events']['event']:
            i = {}
            i['title'] = event.get('title')
            i['start_time'] = event.get('start_time')
            i['description'] = event.get('description')
            i['venue_name'] = event.get('venue_name')
            i['comment_count'] = event.get('comment_count')
            i['calendar_count'] = event.get('calendar_count')
            try:
                index_value = event.get('image').get('url')
            except:
                index_value = None
            i['image_url'] = index_value
            resultevents.append(i)
    except TypeError:
        print "no events found in Eventful --- skipping"
            
    
    return resultevents

def nearby_seatgeek(latitude, longitude, radius=tradius):
    pass


#http://api.seatgeek.com/2/events?range=3mi&lat=37.561667&lon=-122.318908&sort=score.desc
    baseurl = 'http://api.seatgeek.com/2/events'
    values = {'sort' : "score.desc",
              'lat' : latitude,
              'lon' : longitude }
    data = urllib.urlencode(values)
    url = baseurl + '?' +data
    json = send_request(url)
    build_event_list(json)

def schoolandhousing(schooldata):
    baseurl = 'http://www.schoolandhousing.com/jsp/school_locator/findpublicschoolbyaddress.jsp?'
    data = urllib.urlencode(schooldata)
    url = baseurl +data
    return url

def build_event_list(json):
    loc_event = []
    try:
        for event in json.get('events'):
            event_items = []
            event_items['title'] = event.get('title')
            event_items['venue_name'] = event.get('venue_name')
            event_items['url'] = event.get('url')
            event_items['address'] = event['venue']['location']['street'] + ', ' + event['venue']['location']['city'] + ', ' + event['venue']['location']['country'] + ' ' + event['venue']['location']['postalcode']
            event_items['image'] =  event['images']['medium']
            loc_event.append(event_items)
    except KeyError:
        pass

    return loc_event

def send_request(string=None):
    if string != None:
        request_string = string
        request = urllib2.Request(request_string)
        opener = urllib2.build_opener()
        f = opener.open(request)
        json_result = simplejson.load(f)
        return json_result
    
#print nearby_seatgeek(37.561667,-122.318908, "30mi")
