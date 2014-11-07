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
import heapq
from decimal import *
from social_data import nearby_insta, nearby_yelp, nearby_twitter, nearby_foursquare, nearby_eventful, nearby_image
import django_tables2 as tables
from django.template import RequestContext
from django_tables2 import RequestConfig
from geolatlong import geolocate
import pprint

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


    print "Target home image url as exists in DB: %s" % (r.image_url)
    if r.image_url == None or r.image_url == '':
      r.image_url = nearby_image(r.latitude, r.longitude)

    app_data = gen_appraisal(r)
    
    #print "XXXXXX"
    #print app_data
    
    try:
      result_objects= [app_data['home1'], app_data['home2'], app_data['home3']]
      for h in result_objects:
	if h['image_url'] == None or h['image_url'] == '':
	  h['image_url'] = nearby_image(h.get('latitude'), h.get('longitude'))
    except KeyError, e:
      print "%s does not exist" % (e)

    #print r.latitude, r.longitude
    instagram_r = nearby_insta(r.latitude, r.longitude)
    #print instagram_r
    
    yelp_r = nearby_yelp(r.latitude, r.longitude)
    
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
		   'instagram_r': instagram_r,
		   'yelp_r': yelp_r,
		   'twitter_r': twitter_r,
		   'foursquare_r': foursquare_r,
		   'table': foursquare_table,
		   'eventful_r': eventful_r,
		   },
		  RequestContext(request))

def home_similarity(home, subject_home):
  return 10 * abs(home.sqft - subject_home.sqft) + 800 * abs(float(home.baths) - float(subject_home.baths)) #+ 10 * abs(home.year_built - subject_home.year_built)


def gen_appraisal(subject_home):
  data = {}

  city = subject_home.city
  beds = subject_home.beds
  baths = subject_home.baths
  sqft = subject_home.sqft
  min_baths = Decimal(baths) - Decimal(0.5)
  max_baths = Decimal(baths) + Decimal(0.5)
  min_sqft = sqft * 0.8
  max_sqft = sqft * 1.2
  last_sale_date_threshold = "2014-01-01"
  #TODO make sure to not fetch the subject home itself.
  comp_candidates = PrevHomeSales.objects.filter(beds__exact=beds, baths__lte=max_baths, baths__gte=min_baths, sqft__lte=max_sqft,sqft__gte=min_sqft,city__exact=city,last_sale_date__gte=last_sale_date_threshold).exclude(user_input__exact=1).exclude(id__exact=subject_home.id)
  
  #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  #print comp_candidates
  
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
    try: #RAHUL: I added this
      avg_sqft_price += (home.sale_price + 0.0)/home.sqft
    except TypeError:
      pass
    data['home' + str(i)] = model_to_dict(home)
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
    heapq.heappush(h,(sim_score,c))
  comp_candidates_with_sim = []
  for i in range(0,len(comp_candidates)):
    sim_score,home = heapq.heappop(h)
    comp_candidates_with_sim.append((sim_score,home))
  return comp_candidates_with_sim

