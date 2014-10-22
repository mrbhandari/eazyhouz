from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse
import datetime
import MySQLdb
from search.models import *
import json
from forms import *
    
def autosuggest(request):
    query = request.GET.get('q','')
    if(len(query) > 0):
        results = PrevHomeSales.objects.filter(address__icontains=query)
        result_list = []
        for item in results:
            result_list.append(item.address + ", " + item.city + ", " + item.state)
    else:
        result_list = []

    response_text = json.dumps(result_list, separators=(',',':'))
    return HttpResponse(response_text, content_type="application/json")

#This takes a query as an input and searches the db and says if there was an exact match
#http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-ZWz1dyahf20tu3_634pb&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA


def search(request):
  #case 1a
    if 'q' in request.GET:
      query = request.GET.get('q','')
      address = query.split(',')
      
      result = PrevHomeSales.objects.filter(address__icontains=address[0])[:1]   
      if result.count() > 0:
        print result
      
	return render_to_response('search_results.html',
	      {'results': result,
	       'query': query,
	       })
      else:
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