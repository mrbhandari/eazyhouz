from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mysite.views import search, autosuggest, gen_results, gen_homepage, more_info_page, gen_appraisal_page, gen_best_value_search, gen_best_value_res, gen_maps_page, gen_accuracy_for_city, gen_accuracy_search
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap, index
from sitemaps import HomesSitemap, SiteSitemap


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#http://www.redfin.com/CA/Saint-Helena/917-Allison-Ave-94574/home/12193743

sitemaps = {
    'homes': HomesSitemap,
    #'pages' : SiteSitemap,
}

urlpatterns = patterns('',
                       (r'^$', gen_homepage), #search to go to landing page
                       (r'^admin/', include(admin.site.urls)),
                       (r'^search/$', more_info_page), #search to go to landing page search
                       #(r'^autosuggest/$', autosuggest),
                       (r'^gen_results/$', gen_appraisal_page), # to gen_results for landing page search
                       (r'^home/$', gen_homepage),
                       (r'^home/search/$', more_info_page),
                       (r'^best-value-homes/$', gen_best_value_search),
                       (r'^accuracy-recent-sales/$', gen_accuracy_search),
                       (r'^best-value-homes/search/(?P<city>.*)', gen_best_value_res),
                       (r'^accuracy-recent-sales/search/(?P<city>.*)', gen_accuracy_for_city),
                       (r'^home/genappraisal/(\w{2})/(\w)+/home/(?P<pid>[a-zA-Z0-9_-]+)', gen_appraisal_page),
                       (r'^maps/$', gen_maps_page),
                       (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")),
                       
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
