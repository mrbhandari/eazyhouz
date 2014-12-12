from django.contrib.sitemaps import Sitemap
from search.models import PrevHomeSales
from datetime import datetime
from django.core.urlresolvers import reverse

class HomesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    
    
    def items(self):
        return PrevHomeSales.objects.all()
    
    def lastmod(self, obj):
        return datetime.now()
    
    def location(self, obj):
        return obj.gen_url()
    
    
class SiteSitemap(Sitemap):
    def __int__(self, names):
        self.names = names
    
    def items(self):
        return self.names
    
    def changefreq(self, obj):
        return 'weekly'
    
    def lastmod(self, obj):
        return datetime.now()
    
    def location(self, obj):
        return reverse(obj)
        