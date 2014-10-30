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


#http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-ZWz1dyahf20tu3_634pb&address=222+8th+ave+Apt+320&citystatezip=San%20Mateo%2C+CA


def search(request):
#This takes a query as an input and searches the db and says if there was an exact match
  #case 1a - check if there is an exact match, if so return our data
    success_status = False
    if 'q' in request.GET:
      query = request.GET.get('q','')
      query2 = request.GET.get('q2','')
      address = query.split(',')
      DB_LOOKUP = 0
      #skips the db lookup for now since we use zillow
      result = PrevHomeSales.objects.filter(address__icontains=address[0])[:DB_LOOKUP]
      #TODO: Considers only exact match
      #TODO: Needs to consider both query parameters q and q2
      
      if result.count() > 0:
	result = result[0]
        print result
	print result.id
      
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
