from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse
import datetime
import MySQLdb
from search.models import *
import json

    
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


def search(request):
    if 'q' in request.GET:
      query = request.GET.get('q','')
      address = query.split(',')
      
      result = PrevHomeSales.objects.filter(address__icontains=address[0])
      print result
      
      return render_to_response('search_results.html',
            {'results': result,
             'query': query,
             })
    else:
        error = ""
        return render_to_response('search_form.html',
                                  {'error':error})