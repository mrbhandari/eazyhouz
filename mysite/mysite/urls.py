from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mysite.views import search, autosuggest
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', search),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^search/$', search),
                       (r'^autosuggest/$', autosuggest),
                       (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
)

urlpatterns += staticfiles_urlpatterns()
