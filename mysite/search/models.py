from django.db import models


class LeadGenUser(models.Model):
    full_name = models.CharField(max_length=512,null=False, blank=False)
    email_address = models.EmailField(max_length=512,null=False, blank=False)
    inquiry_reason = models.CharField(max_length=1024,null=False, blank=False, default="Select")
    property_address = models.CharField(max_length=1024,null=True, blank=True)
    phone_number = models.CharField(max_length=10,null=True, blank=False)
    user_agent = models.CharField(max_length=1024,null=True, blank=True)
    remote_address = models.IPAddressField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now = True, null=True)
    zestimate_found = models.NullBooleanField()
    zestimate_link = models.URLField(null=True, blank=True)
                            
class PrevHomeSales(models.Model):
    #sale_type = models.CharField(max_length=512,null=True, blank=True)
    home_type = models.CharField(max_length=512,null=True, blank=True)
    address = models.CharField(max_length=2000,null=True, blank=True)
    city = models.CharField(max_length=500,null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    zipcode = models.CharField(max_length=10,null=True, blank=True)
    sale_price = models.IntegerField(null=True, blank=True)
    beds = models.IntegerField(null=True, blank=True)
    baths = models.DecimalField(max_digits=4, decimal_places=1,null=True, blank=True)
    sqft = models.IntegerField(null=True, blank=True)
    lot_size = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(max_length=4,null=True, blank=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=9,null=True, blank=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=9,null=True, blank=True)
    interior_rating = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    exterior_rating = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    view_rating = models.DecimalField(max_digits=5,decimal_places=5,null=True,blank=True)
    url = models.CharField(max_length=2000,null=True,blank=True)
    image_url = models.CharField(max_length=2000,null=True,blank=True)
    elementary = models.IntegerField(null=True,blank=True)
    middle = models.IntegerField(null=True,blank=True)
    high = models.IntegerField(null=True,blank=True)
    other_school_rating = models.IntegerField(null=True,blank=True)
    remodeled = models.NullBooleanField()
    last_sale_date = models.DateField(null=True, blank=True)
    user_input = models.NullBooleanField()
    last_zestimate = models.IntegerField(null=True, blank=True)
    curr_status = models.CharField(max_length=512,null=True, blank=True)
    property_type = models.CharField(max_length=512,null=True, blank=True)
    elem_school_name = models.CharField(max_length=2000,null=True,blank=True)
    middle_school_name = models.CharField(max_length=2000,null=True,blank=True)
    high_school_name = models.CharField(max_length=2000,null=True,blank=True)
    other_school_name = models.CharField(max_length=2000,null=True,blank=True)
    outlier = models.NullBooleanField()
    eazyhouz_hash = models.CharField(max_length=512,null=True,blank=True)	

    def __unicode__(self):
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (self.address, self.city, self.state, self.zipcode, self.last_sale_date, self.sale_price, self.property_type, self.beds, self.baths, self.sqft)
    
    #def save(self, *args, **kwargs):
    #     try:
    #         existing = PrevHomeSales.objects.get(user=self.user)
    #         self.id = existing.id #force update instead of insert
    #     except PrevHomeSales.DoesNotExist:
    #         pass 
    #     models.Model.save(self, *args, **kwargs)
