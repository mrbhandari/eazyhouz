import sys,os
import datetime
from decimal import *
from numpy import genfromtxt
from numpy import array_str
from django.db import transaction
from django.db.models import get_models, Model
import traceback
your_djangoproject_home="/Users/pradeep/eazyhouz/eazyhouz/mysite/"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
getcontext().prec = 5
from search.models import PrevHomeSales
import django

@transaction.commit_on_success
def merge_model_objects(primary_object, alias_objects=[], keep_old=False):
    """
    Use this function to merge model objects (i.e. Users, Organizations, Polls,
    etc.) and migrate all of the related fields from the alias objects to the
    primary object.
    
    Usage:
    from django.contrib.auth.models import User
    primary_user = User.objects.get(email='good_email@example.com')
    duplicate_user = User.objects.get(email='good_email+duplicate@example.com')
    merge_model_objects(primary_user, duplicate_user)
    """
    if not isinstance(alias_objects, list):
        alias_objects = [alias_objects]
    
    # check that all aliases are the same class as primary one and that
    # they are subclass of model
    primary_class = primary_object.__class__
    
    if not issubclass(primary_class, Model):
        raise TypeError('Only django.db.models.Model subclasses can be merged')
    
    for alias_object in alias_objects:
        if not isinstance(alias_object, primary_class):
            raise TypeError('Only models of same class can be merged')
    
    blank_local_fields = set([field.attname for field in primary_object._meta.local_fields if getattr(primary_object, field.attname) in [None, '']])
    override_fields = ['sale_price']

    # Loop through all alias objects and migrate their data to the primary object.
    for alias_object in alias_objects:
        # Migrate all foreign key references from alias object to primary object.
        for related_object in alias_object._meta.get_all_related_objects():
            # The variable name on the alias_object model.
            alias_varname = related_object.get_accessor_name()
            # The variable name on the related model.
            obj_varname = related_object.field.name
            related_objects = getattr(alias_object, alias_varname)
            for obj in related_objects.all():
                setattr(obj, obj_varname, primary_object)
                obj.save()

        # Migrate all many to many references from alias object to primary object.
        for related_many_object in alias_object._meta.get_all_related_many_to_many_objects():
            alias_varname = related_many_object.get_accessor_name()
            obj_varname = related_many_object.field.name
            
            if alias_varname is not None:
                # standard case
                related_many_objects = getattr(alias_object, alias_varname).all()
            else:
                # special case, symmetrical relation, no reverse accessor
                related_many_objects = getattr(alias_object, obj_varname).all()
            for obj in related_many_objects.all():
                getattr(obj, obj_varname).remove(alias_object)
                getattr(obj, obj_varname).add(primary_object)

        # Try to fill all missing values in primary object by values of duplicates
        filled_up = set()
        for field_name in blank_local_fields:
            val = getattr(alias_object, field_name) 
            if val not in [None, '']:
                setattr(primary_object, field_name, val)
                filled_up.add(field_name)
        blank_local_fields -= filled_up
            
        for field_name in override_fields:
            val = getattr(alias_object,field_name)
            setattr(primary_object,field_name,val)

        if not keep_old:
            alias_object.delete()
    primary_object.save()
    return primary_object


def normalize_address(address):
    return address.lower().replace(" apt ", " #").replace(" unit "," #").title()

def normalize_property_type(property_type):
    return "Condo/Townhouse" if "condo" in property_type.lower() or "townho" in property_type.lower() else "Single Family Residence"

def update_home(new_home):
    print "HERE"
    old_home = PrevHomeSales.objects.filter(address__iexact=new_home.address)
    if len(old_home) == 1:
        merge_model_objects(old_home[0],[new_home],True)
        print "Merging with existing home"
    else:
        new_home.save()
        print "New home being saved"

django.setup()
lines = open(sys.argv[1]).readlines()
header_index = {}
for ind in range(0,len(lines)):
    try:
        line1 = {}
        if ind == 0:
            line = lines[ind].split("\t")
            for i in range(0,len(line)):
                header_index[i] = line[i]
            continue
        else:
            line = lines[ind].split("\t")
            for i in range(0,len(line)):
                line1[header_index[i]] = line[i]
         
        #line1 = lines[ind]
        home = PrevHomeSales()
        prevhomesales = PrevHomeSales()
        if line1['BEDS']:
            prevhomesales.beds = line1['BEDS']
        if line1['BATHS']:
            prevhomesales.baths = Decimal(line1['BATHS'])
        if line1['SQFT']:
            prevhomesales.sqft = line1['SQFT']
        if line1['YEAR_BUILT']:
            prevhomesales.year_built = line1['YEAR_BUILT']
        if line1['LAST_SALE_PRICE']:
            prevhomesales.sale_price = Decimal(line1['LAST_SALE_PRICE'])
        if line1['URL']:
            prevhomesales.url = line1['URL']
        if line1['LATITUDE']:
            prevhomesales.latitude = Decimal(line1['LATITUDE'])
        if line1['LONGITUDE']:
            prevhomesales.longitude = Decimal(line1['LONGITUDE'])
        if line1['HOME_TYPE']:
            prevhomesales.property_type = normalize_property_type(line1['HOME_TYPE'])
        if line1['CITY']:
            prevhomesales.city = line1['CITY']
        if line1['STATE']:
            prevhomesales.state = line1['STATE']
        if line1['ZIP']:
            prevhomesales.zipcode = line1['ZIP']
        if line1['LOT_SIZE']:
            prevhomesales.lot_size = line1['LOT_SIZE']
        if line1['LAST_SALE_DATE']:
            if '/' in line1['LAST_SALE_DATE']:
                prevhomesales.last_sale_date = datetime.datetime.strptime(line1['LAST_SALE_DATE'], '%m/%d/%y').date()
            else:
                prevhomesales.last_sale_date = datetime.datetime.strptime(line1['LAST_SALE_DATE'], '%Y-%m-%d').date()
        if line1['ADDRESS']:
            prevhomesales.address = normalize_address(line1['ADDRESS'])
        prevhomesales.user_input = False
        prevhomesales.curr_status="sold"
        print prevhomesales
        update_home(prevhomesales)
        #prevhomesales.save()
    except Exception as e:
        print "Exception", traceback.format_exc()
        pass
