import sys,os
import datetime
from decimal import *
from numpy import genfromtxt 
from numpy import array_str

# Full path to your django project directory
your_djangoproject_home="/Applications/MAMP/htdocs/eazyhouz/mysite/"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
getcontext().prec = 5
from search.models import PrevHomeSales
dt=[('ID','<i4'),('BEDS', '<i4'),('BATHS', '<f8'),('SQFT', '<i8'),('YEAR','<i4'),('LAST_SALE_PRICE','<f8'),('URL','S20000'),('LATITUDE','<f8'),('LONGITUDE','<f8'),('ELEMENTARY','<i4'),('MIDDLE','<i4'),('HIGH','<i4'),('HOME_TYPE','<i2'), ('REMODELED','<i2'),('IRATING','<f8'),('ERATING','<f8'),('ADDRESS','S20000'),('CITY','S200'),('STATE','S200'),('ZIP','S10'),('LOT_SIZE','<i8'),('LAST_SALE_DATE','S1000'),('IMAGE_URL','S2000')]
lines = genfromtxt(sys.argv[1], dtype=dt,comments="#", delimiter="\t", names=True, missing_values='',filling_values=0, unpack=False)

for ind in range(1,len(lines)):
	line1 = lines[ind]
	home = PrevHomeSales()
        prevhomesales = PrevHomeSales()
        prevhomesales.beds = line1['BEDS']
        prevhomesales.baths = Decimal(line1['BATHS'])
	prevhomesales.sqft =line1['SQFT']
	prevhomesales.year_built = line1['YEAR']
	prevhomesales.sale_price = Decimal(line1['LAST_SALE_PRICE'])
	prevhomesales.url = line1['URL']
	prevhomesales.image_url = line1['IMAGE_URL']
	prevhomesales.latitude = Decimal(line1['LATITUDE'])
	prevhomesales.longitude = Decimal(line1['LONGITUDE'])
	prevhomesales.elementary = line1['ELEMENTARY']
	prevhomesales.middle = line1['MIDDLE']
	prevhomesales.high = line1['HIGH']
	prevhomesales.home_type = line1['HOME_TYPE']
	prevhomesales.remodeled = line1['REMODELED']
	prevhomesales.interior_rating = Decimal(line1['IRATING'])
	prevhomesales.exterior_rating = Decimal(line1['ERATING'])
	prevhomesales.city = line1['CITY']
	prevhomesales.state = line1['STATE']
	prevhomesales.zipcode = line1['ZIP_CODE']
        prevhomesales.lot_size = line1['LOT_SIZE']
        prevhomesales.last_sale_date = datetime.datetime.strptime(line1['LAST_SALE_DATE'], '%m/%d/%y').date()
	prevhomesales.address = line1['ADDRESS'] 
	#prevhomesales.view_rating = line1['VIEW']

	
        print prevhomesales
        prevhomesales.save()

