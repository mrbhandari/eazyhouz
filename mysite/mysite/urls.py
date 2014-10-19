from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mysite.views import search, autosuggest

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', search),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^search/$', search),
                       (r'^autosuggest/$', autosuggest),
)

urlpatterns += staticfiles_urlpatterns()
