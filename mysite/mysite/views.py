from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse
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
    if 'q' in request.GET:
      query = request.GET.get('q','')
      query2 = request.GET.get('q2','')
      address = query.split(',')
      
      result = PrevHomeSales.objects.filter(address__icontains=address[0])[:1]
      #TODO: Considers only exact match
      #TODO: Needs to consider both query parameters q and q2
      
      if result.count() > 0:
	result = result[0]
        print result
	
	return render_to_response('search_results.html',
	      {'result': result,
	       'query': query,
      	       })
      #case 1b = Doesn't exits in our DB as exact match, Try Zillow
      else:
	try:
	  print query, query2
	  result = return_zhome_attr(query, query2)
	  
	  print "XXXXXXXXX"
	  print result
	  return render_to_response('search_results.html',
	      {'result': result,
	       'query': query,
      	       })
	  
	#case 1c = if that doesn't work return a blank form
	except:
	  return render_to_response('enter_more_info.html',
		{'results': result,
		 'query': query,
		 'form': TargetHomeForm(),
		 })
    else:
	if 'q' in request.GET and request.GET.get('q','')=='':
	  error = "Please enter a search term."
	else:
	  error = ''
	return render_to_response('search_form.html',
				  {'error':error})