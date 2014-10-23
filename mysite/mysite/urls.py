from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mysite.views import search, autosuggest
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', search),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^search/$', search),
                       (r'^autosuggest/$', autosuggest),
                       (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow:", content_type="text/plain"))
)

urlpatterns += staticfiles_urlpatterns()
