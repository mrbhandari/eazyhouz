from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponseRedirect, HttpResponse
import datetime
import MySQLdb
from search.models import *
import json
from forms import *
from zillowrequest import return_zhome_attr
from django.forms.models import model_to_dict
from django.db.models import Q
import heapq
from decimal import *
from social_data import nearby_insta, nearby_yelp, nearby_twitter, nearby_foursquare, nearby_eventful, nearby_image
import django_tables2 as tables
from django_tables2 import RequestConfig
from django_tables2 import A
from django.template import RequestContext
from geolatlong import geolocate
import pprint
from django.db.models import Count
import math
import time

class FoursquareTable(tables.Table):
    name = tables.Column(verbose_name="Venue Name")
    category = tables.Column(verbose_name="Type")
    usersCount = tables.Column(verbose_name="Users")
    checkinsCount = tables.Column(verbose_name="Check-ins")
    repeatRatio = tables.Column(verbose_name="Loyalty Rating")
    url = tables.URLColumn(verbose_name="Website")
    
    
    class Meta:
      attrs = {"class": "table table-striped"}
      order_by_field = True
      order_by = '-repeatRatio'
      
class BestValueTable(tables.Table):
  home_address = tables.LinkColumn('home', args=[A('home.id')], verbose_name="Address", empty_values=()) #accessor="name.address" A('home.address')
  list_price = tables.Column()
  predicted_price = tables.Column()
  error = tables.Column(verbose_name="Value Score")
  
  class Meta:
    attrs = {"class": "table table-striped"}
    order_by_field = True
    order_by = '-error'
    
class RecentSalesTable(tables.Table):
   #home_type = tables.Column(verbose_name="Type")
   address = tables.Column(verbose_name="Address")
   #city = tables.Column(verbose_name="City")
   #zipcode = tables.Column(verbose_name="Zipcode")
   beds = tables.Column(verbose_name="Beds")
   #image_url | interior_rating |
   last_sale_date = tables.Column()
   distance = tables.Column(verbose_name="Distance (miles)")
   sale_price = tables.Column()
   sqft = tables.Column()
   year_built = tables.Column()
   interior_rating = tables.Column()
   reason_excluded = tables.Column()
   sim_score = tables.Column(verbose_name="Similarity Score")
   class Meta:
    attrs = {"class": "table table-striped"}
    order_by_field = True
    order_by = '-sim_score'


import json
import urllib
import ast



def gen_maps_page(request):
  #geocode_school = []
  #response = json.load(urllib.urlopen("https://www.kimonolabs.com/api/4ceghc6y?apikey=rVx4sgzRC30aoGzhQKMQVFMDR0Z3J1TD"))
  #print response
  #for i in response.get('results').get('school'):
  #  try:
  #    print i
  #    address = i.get('address') + " " + i.get('zip')
  #    print address
  #    loc = geolocate(address)
  #    
  #    print loc['latitude'] #throws exception if the geolocate fails
  #    print loc['longitude']
  #    i['location'] = loc
  #    geocode_school.append(i)
  #    print geocode_school      
  #  except KeyError:
  #    pass
  #  time.sleep(.25)
  #
  #with open('testfile1', 'wb') as outfile:
  #  json.dump(geocode_school, outfile)
  #
  school_ratings = {"Bishop Elementary": 4,
  "Braly Elementary": 5,
  "Cherry Chase Elementary": 10,
  "Chester W. Nimitz Elementary": 8,
  "Cumberland Elementary": 10,
  "Ellis Elementary": 7,
  "Fairwood Elementary": 7,
  "George Mayne Elementary": 7,
  "L. P. Collins Elementary": 10,
  "Lakewood Elementary": 4,
  "Ponderosa Elementary": 7,
  "San Miguel Elementary": 4,
  "Vargas Elementary": 4,
  "West Valley Elementary": 10}
  
  school_ratings_color = ["#a50026",
"#d73027",
"#f46d43",
"#fdae61",
"#fee08b",
"#d9ef8b",
"#a6d96a",
"#66bd63",
"#1a9850",
"#006837"]

  with open('testfile1') as json_data:
    bbb = json_data.read()
    bbblist =  ast.literal_eval(bbb)

  appended_bbblist = []
  
  for i in bbblist:
    school = i.get('school')
    if school != '':
      new_school = school.replace("School: ", "")
      print new_school
      print school_ratings[new_school]
      i['school_rating'] = school_ratings[new_school]
    #else:
    #  i['school_rating'] = 1
      print school_ratings_color[i['school_rating'] -1]
      i['school_rating_color'] = school_ratings_color[i['school_rating'] -1]
      appended_bbblist.append(i)
      
  
  
    
  #json.dumps(your_data)

  return render_to_response('maps.html',
                            {'results':appended_bbblist})


def autosuggest(request):
#Takes an autosuggest input and returns matching address line1s from the prevHomeSales model database
    query = request.GET.get('q','')
    if(len(query) > 0):
        results = PrevHomeSales.objects.filter(address__icontains=query)
        result_list = []
        for item in results:
            result_list.append(item.address)
            #item.city + ", " + item.state
    else:
        result_list = []

    response_text = json.dumps(result_list, separators=(',',':'))
    return HttpResponse(response_text, content_type="application/json")


def search(request):
#This takes a query as an input and searches the db and says if there was an
#exact match
#case 1a - check if there is an exact match, if so return our data
    success_status = False
    if 'q' in request.GET:
      query = request.GET.get('q','')
      query2 = request.GET.get('q2','')
      #address = query.split(',')
      DB_LOOKUP = 0
      #skips the db lookup for now since we use zillow
      result = PrevHomeSales.objects.filter(address__icontains=query)[:DB_LOOKUP]
      #TODO: Considers only exact match
      #TODO: Needs to consider both query parameters q and q2

      if result.count() > 0:
        result = result[0]
        #print result
        #print result.id

      else:
        try:

          result = return_zhome_attr(query, query2)

          print result.id
          success_status = True

        except:
          phrase = "** Found **"
          result.beds = phrase
          result.baths = phrase
          result.sqft = phrase
          result.year_built = phrase
          result.last_sale_date = phrase
          result.sale_price = phrase
          result.address = phrase
          result.city = phrase
          result.url = ''
          result.id = 0

      if request.method == 'POST':
        #add the property address the user has input in
        post_request = request.POST.copy()
        post_request.appendlist('property_address', request.META.get('QUERY_STRING'))
        post_request.appendlist('user_agent', request.META.get('HTTP_USER_AGENT'))

        #TODO: this doesn't seem to populate the ip address
        post_request.appendlist('remote_address', get_client_ip(request))
        post_request.appendlist('zestimate_found', success_status)
        post_request.appendlist('zestimate_link', result.url)

        form = LeadGenUserForm(post_request)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect('/gen_results/?prevHomeSalesId=' + str(result.id))
      else:

        form = LeadGenUserForm()


      return render_to_response('enter_more_info.html',
                    {'result': result,
                     'query': query,
                     'form': form,
                     })
      #case 1b = Doesn't exits in our DB as exact match, Try Zillow
        #case 1c = if that doesn't work return a blank form

    else:
        if 'q' in request.GET and request.GET.get('q','')=='':
          error = "Please enter a search term."
        else:
          error = ''
        return render_to_response('search_form.html',
                                  {'error':error})

def gen_results(request):

  if 'prevHomeSalesId' in request.GET:
    result = PrevHomeSales()
    prevHomeSalesId = int(request.GET.get('prevHomeSalesId',''))

    if prevHomeSalesId > 0:
      print "THIS HAPPENED"
      result = PrevHomeSales.objects.filter(id=prevHomeSalesId)[:1][0]
      result.last_zestimate = int(round(result.last_zestimate * 1.05, -2))
    else:
      result.last_zestimate = '...Will send in Email'

  return render_to_response('lead_gen_results.html',
                    {'result': result,
                     })

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


#NON LEAD GEN PORTION OF SITE

def gen_homepage(request):
  error = None
  if 'error' in request.GET:
    error = request.GET.get('error','')
  return render_to_response('search_form.html',
                            {'error':error})


def more_info_page(request):
  result, query, form =  [], [], PrevHomeSalesForm()
  
  if 'q' in request.GET and 'q2' in request.GET: #All correct vars exist load page
    query, query2 = request.GET.get('q',''), request.GET.get('q2','')
    return_request = update_prevhome(request, query, query2)
    return return_request

  else:
    return HttpResponseRedirect('/home?error=Please fill out the form completely') #Return homepage with error


def update_prevhome(request, query, query2):
      if request.method== 'POST':
        try:     
          print "XXXXXXX XXXXXXX Getting id"
          print request.POST.get('id')
          u = PrevHomeSales.objects.get(id=request.POST.get('id')) #TODO figure out a unique key
          form = PrevHomeSalesForm(request.POST, instance=u)
        except: #TODO FIX blanket except clause PrevHomeSales.DoesNotExist, AttributeError:
          form = PrevHomeSalesForm(request.POST)
          #print form
          form.id = -1
        if form.is_valid():
          requesthome = form.save(commit=False)
          requesthome.save()
          return HttpResponseRedirect('/home/genappraisal/?pid=' + str(requesthome.id))
        else:
          print form.errors
          return render_to_response('detailed_more_info.html', #Render normal page
                  {'form': form,
                   })
      else:
        try:
          print "Not a post request"
          result = return_zhome_attr(query, query2) #try to get Zillow data
          if result == None:
	    raise AttributeError
          form = PrevHomeSalesForm(instance=result)
          #print form
        except AttributeError: #catches if Zillow Fails
          try:
            loc = geolocate(query + ' ' +query2)
            print loc['latitude'] #throws exception if the geolocate fails
            #print pprint.pprint(loc)
            form = PrevHomeSalesForm( initial={'address': loc.get('firstline'),
                                               'city': loc.get('city'),
                                               'zipcode': loc.get('zipcode'),
                                               'state':  loc.get('state'), 
                                               'id': -1,
                                               'user_input': True,
                                               'latitude': loc.get('latitude'),
                                               'longitude': loc.get('longitude')}) #create blank result
          except KeyError, e: #catches a failed geolocate
            print "%s not found" % (e)
	    return HttpResponseRedirect('/home?error=Please enter a valid address')#Return homepage with error
	return render_to_response('detailed_more_info.html', #Render normal page
		  {'form': form,
		   })
      


def gen_appraisal_page(request):
  result = []
  if 'pid' in request.GET: #All correct vars exist load page
    pid = request.GET.get('pid','')  
    r = PrevHomeSales.objects.get(id=pid)
    subject_interior_rating_display = "Unknown"
    if r.interior_rating == 1 or r.interior_rating == 2:
        subject_interior_rating_display = "Poor"
    if r.interior_rating == 3:
        subject_interior_rating_display = "Average"
    if r.interior_rating == 4 or r.interior_rating == 5:
        subject_interior_rating_display = "Excellent"
    print "Target home image url as exists in DB: %s" % (r.image_url)
    if r.image_url == None or r.image_url == '':
      r.image_url = nearby_image(r.latitude, r.longitude)

    app_data = gen_appraisal(r)
    
    print app_data
    
    
    recent_sales = get_recent_sales(r)

    try:    
      psft = 'na'
      for i in recent_sales:
	total_sale_price = i.get('sale_price') 
	total_sqft = i.get('sqft')
	psft = int(total_sale_price / total_sqft)
	indexof = recent_sales.index(i)
	recent_sales[indexof]['psft'] = psft
    except ZeroDivisionError:
      pass
    
    
    recent_sales_table = RecentSalesTable(recent_sales)
    RequestConfig(request).configure(recent_sales_table)
    
    #print app_data
    
    try:
      result_objects= [app_data['home1'], app_data['home2'], app_data['home3']]
      for h in result_objects:
	if h['image_url'] == None or h['image_url'] == '':
	  h['image_url'] = nearby_image(h.get('latitude'), h.get('longitude'))
    except KeyError, e:
      print "%s does not exist" % (e)
    eventful_r, instagram_r, yelp_r, foursquare_r, twitter_r = {}, {}, {}, {}, {}
    
    instagram_r = nearby_insta(r.latitude, r.longitude)
    try:
      yelp_r = nearby_yelp(r.latitude, r.longitude)
    except:
      pass
      
    twitter_r = nearby_twitter(r.latitude, r.longitude)
    foursquare_r = nearby_foursquare(r.latitude, r.longitude)
    foursquare_table = FoursquareTable(foursquare_r)
    RequestConfig(request).configure(foursquare_table)
    
    try:
      eventful_r = nearby_eventful(r.latitude, r.longitude)
    except: #TODO remove general except clause (Rahul)
      print "Could not get eventful"
      
    
    return render_to_response(
		  'search_results.html',
		  {'result': app_data,
		   'subject_home': r,
           'subject_home_interior_rating': subject_interior_rating_display,
		   'instagram_r': instagram_r,
		   'yelp_r': yelp_r,
		   'twitter_r': twitter_r,
		   'foursquare_r': foursquare_r,
		   'table': foursquare_table,
		   'recent_sales_table': recent_sales_table,
		   'recent_sales': recent_sales,
		   'eventful_r': eventful_r,
		   },
		  RequestContext(request))

def biggest_dissimilarity_factor(home, subject_home):
	distance = distance_on_unit_sphere(float(home.latitude), float(home.longitude), float(subject_home.latitude), float(home.longitude))
 	factors = [5 * abs(home.sqft - subject_home.sqft), 80 * abs(float(home.baths) - float(subject_home.baths)), 200 * distance]
	factor_names = ["Difference in Sqft","Difference in number of baths","Distance from subject property"]
	return factor_names[factors.index(max(factors))]



def home_similarity(home, subject_home):
  use_lot_size = False
  use_year_built = False
  if (subject_home.city == "cupertino" or subject_home.city == "sunnyvale") and subject_home.property_type == "Single Family Residence" and subject_home.lot_size:
    use_lot_size = True
  if (subject_home.city == "cupertino" or subject_home.city == "sunnyvale") and subject_home.year_built:
    use_year_built = True
  distance = distance_on_unit_sphere(float(home.latitude), float(home.longitude), float(subject_home.latitude), float(home.longitude))
  similarity_score = 80 * abs(float(home.baths) - float(subject_home.baths)) + 1600 * distance #+ 10 * abs(home.year_built - subject_home.year_built)
  if use_year_built:
    similarity_score += abs(home.year_built - subject_home.year_built)
  if use_lot_size:
    similarity_score += 0.1 * abs(home.lot_size - subject_home.lot_size)
  return similarity_score

def get_candidates(subject_home):
  use_lot_size = False
  use_year_built = False
  if (subject_home.city == "cupertino" or subject_home.city == "sunnyvale") and subject_home.property_type == "Single Family Residence" and subject_home.lot_size:
    use_lot_size = True
  if (subject_home.city == "cupertino" or subject_home.city == "sunnyvale") and subject_home.year_built:
    use_year_built = True
  use_interior_rating = False
  if subject_home.interior_rating:
    use_interior_rating = True
  city = subject_home.city
  beds = subject_home.beds
  baths = subject_home.baths
  sqft = subject_home.sqft
  min_baths = Decimal(baths) - Decimal(0.5)
  max_baths = Decimal(baths) + Decimal(0.5)
  min_sqft = sqft * 0.7
  max_sqft = sqft * 1.3
  last_sale_date_threshold = "2014-01-01"
  
  last_sale_date_max_threshold = datetime.datetime.now()
  min_lot_size = subject_home.lot_size * 0.6
  max_lot_size = subject_home.lot_size * 1.4
  min_year_built = subject_home.year_built - 20
  max_year_built = subject_home.year_built + 20
  if use_interior_rating:
    if subject_home.interior_rating == 3:
      comp_candidates = PrevHomeSales.objects.filter(beds__exact=beds,
      baths__lte=max_baths, baths__gte=min_baths,
      sqft__lte=max_sqft,sqft__gte=min_sqft,city__exact=city,last_sale_date__gte=last_sale_date_threshold,last_sale_date__lt=last_sale_date_max_threshold,property_type__exact=subject_home.property_type,remodeled__exact=subject_home.remodeled,interior_rating__exact=subject_home.interior_rating).exclude(user_input__exact=1).exclude(id__exact=subject_home.id).exclude(address__iexact=subject_home.address,zipcode__exact=subject_home.zipcode).exclude(curr_status__exact="active").exclude(interior_rating__isnull=True)
    if subject_home.interior_rating == 1 or subject_home.interior_rating == 2:
      comp_candidates = PrevHomeSales.objects.filter(beds__exact=beds,
      baths__lte=max_baths, baths__gte=min_baths,
      sqft__lte=max_sqft,sqft__gte=min_sqft,city__exact=city,last_sale_date__gte=last_sale_date_threshold,last_sale_date__lt=last_sale_date_max_threshold,property_type__exact=subject_home.property_type,remodeled__exact=subject_home.remodeled).filter(Q(interior_rating__exact=1) | Q(interior_rating__exact=2)).exclude(user_input__exact=1).exclude(id__exact=subject_home.id).exclude(address__iexact=subject_home.address,zipcode__exact=subject_home.zipcode).exclude(curr_status__exact="active").exclude(interior_rating__isnull=True)
    if subject_home.interior_rating == 4 or subject_home.interior_rating == 5:
      comp_candidates = PrevHomeSales.objects.filter(beds__exact=beds,
      baths__lte=max_baths, baths__gte=min_baths,
      sqft__lte=max_sqft,sqft__gte=min_sqft,city__exact=city,last_sale_date__gte=last_sale_date_threshold,last_sale_date__lt=last_sale_date_max_threshold,property_type__exact=subject_home.property_type,remodeled__exact=subject_home.remodeled).filter(Q(interior_rating__exact=4) | Q(interior_rating__exact=5)).exclude(user_input__exact=1).exclude(id__exact=subject_home.id).exclude(address__iexact=subject_home.address,zipcode__exact=subject_home.zipcode).exclude(curr_status__exact="active").exclude(interior_rating__isnull=True)

  else:
    comp_candidates = PrevHomeSales.objects.filter(beds__exact=beds,
    baths__lte=max_baths, baths__gte=min_baths,
    sqft__lte=max_sqft,sqft__gte=min_sqft,city__exact=city,last_sale_date__gte=last_sale_date_threshold,last_sale_date__lt=last_sale_date_max_threshold,property_type__exact=subject_home.property_type).exclude(user_input__exact=1).exclude(id__exact=subject_home.id).exclude(address__iexact=subject_home.address,zipcode__exact=subject_home.zipcode).exclude(curr_status__exact="active")
  if use_lot_size:
    comp_candidates = comp_candidates.filter(lot_size__lt=max_lot_size,lot_size__gt=min_lot_size)
  if use_year_built:
    comp_candidates = comp_candidates.filter(year_built__lt=max_year_built,year_built__gt=min_year_built)
  return comp_candidates


def diff_month(d1, d2):
  return (d1.year - d2.year)*12 + d1.month - d2.month

def gen_appraisal(subject_home):
  data = {}
  #TODO make sure to not fetch the subject home itself.
  interior_rating_display_map = {} 
  interior_rating_display_map[1] = "Poor"
  interior_rating_display_map[2] = "Poor"
  interior_rating_display_map[3] = "Average"
  interior_rating_display_map[4] = "Excellent"
  interior_rating_display_map[5] = "Excellent"
  h = []

  comp_candidates = get_candidates(subject_home)
  if len(comp_candidates) < 3:
     return data
  data["number_of_homes_used"] = len(comp_candidates)
  for c in comp_candidates:
    sim_score = home_similarity(c,subject_home)
    heapq.heappush(h,(sim_score,c))
  k = 3
  avg_sqft_price = 0
  use_low_sim_homes = False
  num_low_sim_homes = 0
  low_sim_score_threshold = 10
  for i in range(1,k+1):
    sim_score,home = heapq.heappop(h)
    if sim_score <= low_sim_score_threshold:
      avg_sqft_price = avg_sqft_price + (home.sale_price + 0.0)/home.sqft if use_low_sim_homes else (home.sale_price + 0.0)/home.sqft
      num_low_sim_homes += 1
      use_low_sim_homes = True
    try: #RAHUL: I added this
      if not use_low_sim_homes:
        avg_sqft_price += (home.sale_price + 0.0)/home.sqft
    except TypeError:
      pass
    data['home' + str(i)] = model_to_dict(home)
    if home.interior_rating:
      data['home' + str(i)]['display_interior_rating'] = interior_rating_display_map.get(home.interior_rating)
    else:
      data['home' + str(i)]['display_interior_rating'] = "Unknown"

    data['similarity' + str(i)] = 100/(1.0+sim_score/100)
    dist = distance_on_unit_sphere(float(subject_home.latitude),float(subject_home.longitude),float(home.latitude),float(home.longitude))
    dist = "{0:.2f}".format(round(dist,2))
    data["distance" + str(i)] = dist
  if use_low_sim_homes:
    avg_sqft_price /= num_low_sim_homes
    data["use_low_sim_homes"] = True
  else:
    avg_sqft_price /= k
  avg_sqft_price /= 2
  #data['estimated_price'] = avg_sqft_price * subject_home.sqft
  estimated_price = 0
  for i in range(1,k+1):
    adjustment = {}
    sqft_adjustment = avg_sqft_price * (subject_home.sqft - data['home'+str(i)]['sqft'])
    adjustment['sqft'] = sqft_adjustment
    home_sale_date = data['home' + str(i)]['last_sale_date']
    num_months = diff_month(datetime.datetime.now(), home_sale_date)
    adjusted_home_value = data["home" + str(i)].get("sale_price") + sqft_adjustment
    time_adjustment = adjusted_home_value * (1.01)**num_months - adjusted_home_value
    adjustment['market_adjustment'] = time_adjustment
    data['adjusted_home_value' + str(i)] = adjusted_home_value + time_adjustment
    print num_months
    data['adjustment' + str(i)] = adjustment
    if use_low_sim_homes:
      if 1.1 * data['similarity' + str(i)] >= 100:
        data["home" + str(i)]["comp_used"] = True
        estimated_price += (adjusted_home_value + time_adjustment)
    else:
      data["home" + str(i)]["comp_used"] = True
      estimated_price += (adjusted_home_value + time_adjustment)
    data["similarity" + str(i)] =  "{0:.2f}".format(round(data["similarity" + str(i)],2))
  
  if use_low_sim_homes:
    estimated_price /= num_low_sim_homes
  else:
    estimated_price /= k

  data["estimated_price"] = estimated_price
  return data

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
def get_recent_sales(subject_home):
  h = []
  comp_candidates = get_candidates(subject_home)
  for c in comp_candidates:
    sim_score = home_similarity(c,subject_home)
    comp_house = model_to_dict(c)
    comp_house["sim_score"] = int(100/(1.0 + sim_score/100))
    #sim_score = "{0:.2f}".format(round(sim_score,2))
    dist = distance_on_unit_sphere(float(subject_home.latitude),float(subject_home.longitude),float(c.latitude),float(c.longitude))
    dist = "{0:.2f}".format(round(dist,2))
    comp_house["distance"] = dist
    comp_house["reason_excluded"] = biggest_dissimilarity_factor(c,subject_home)
    heapq.heappush(h,(sim_score,comp_house))
  comp_candidates_with_sim = []
  for i in range(0,min(20,len(comp_candidates))):
    sim_score,comp_home = heapq.heappop(h)
    comp_candidates_with_sim.append(comp_home)
  return comp_candidates_with_sim


def gen_best_value_search(request):
  list_of_cities = get_distinct_cities_with_k_active_houses()
  print list_of_cities
  #error = None
  #if 'error' in request.GET:
  #  error = request.GET.get('error','')
  return render_to_response('best_value_homes.html',
                            {'cities':  list_of_cities})
  


def gen_best_value_res(request, city):
  best_homes = get_best_value_homes(city, -10000, 10000)
  
  #print "XXXXXXXXXXXXX Best Homes"
  #print best_homes
  
  best_homes_table = BestValueTable(best_homes)
  RequestConfig(request).configure(best_homes_table)
  return render_to_response('best_value_homes_res.html',
                            {'best_homes_table':  best_homes_table,
			     'best_homes': best_homes,},
			    RequestContext(request))

def get_distinct_cities():
	return PrevHomeSales.objects.values_list('city', flat=True).distinct()


def get_distinct_cities_with_k_active_houses(k=3):
	return PrevHomeSales.objects.filter(curr_status__exact="active").values('city').annotate(total=Count('city')).filter(total__gte=k)


def get_best_value_homes(city, low_percent, high_percent, multiplier = 1):
	all_homes_in_city = PrevHomeSales.objects.filter(curr_status__exact="active",city__exact=city)
	best_homes = []
	h = []
	ctr = 0
	for home in all_homes_in_city:
		data = gen_appraisal(home)
		list_price = home.sale_price
		predicted_price = data.get("estimated_price")
		if not predicted_price:
			continue
		error = list_price/(predicted_price + 0.0) - 1
		if error >= low_percent and error <= high_percent:
			heapq.heappush(h,(multiplier*error, error, predicted_price,home))
			ctr += 1
	for i in range(0,ctr):
		error_key, error, predicted_price, home = heapq.heappop(h)
		d = {}
		
		if home.image_url == None or home.image_url == '':
			home.image_url = nearby_image(home.latitude, home.longitude)
		d["home"] = home
		d["list_price"] = home.sale_price
		d["error"] = error
		d["predicted_price"] = predicted_price
		best_homes.append(d)
	return best_homes
