# Full path and name to your csv file
csv_filepathname="/Applications/MAMP/htdocs/eazyhouz/mysite/past_sales_singlecolumn.txt"

# Full path to your django project directory
your_djangoproject_home="/Applications/MAMP/htdocs/eazyhouz/mysite/"

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from search.models import PrevHomeSales

import csv
#dataReader = csv.reader(open(csv_filepathname, 'rU'), dialect='excel-tab', quoting=csv.QUOTE_NONNUMERIC)
#dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')


import numpy as np
from pandas import DataFrame
df = DataFrame.from_csv(csv_filepathname, header=0, sep='\t', index_col=False, parse_dates=True, encoding=None, tupleize_cols=True, infer_datetime_format=True)
df.fillna(0, inplace=True)
array = df.as_matrix() # the array you are interested in
print array




#for x in np.nditer(array):
#     print x,

#for x in np.nditer(array, flags=['external_loop', 'refs_ok'], order='C'):
#     print x,


#DataFrame.from_csv(path, header=0, sep='\t', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)


for row in array:
    if row[0] != 'SALE TYPE': # Ignore the header row, import everything else
        prevhomesales = PrevHomeSales()
        prevhomesales.sale_type = row[0]
        prevhomesales.home_type = row[1]
        prevhomesales.address = row[2]
        prevhomesales.city = row[3]
        prevhomesales.statecode = row[4]
        prevhomesales.zipcode = (row[5])
        prevhomesales.list_price = round(row[6])
        prevhomesales.beds = round(row[7])
        #print 'xxxxxxx'
        #print ['baths', row[8]]
        #prevhomesales.baths = round(row[8], 1)
        #prevhomesales.location = row[9]
        #prevhomesales.sqft = round(row[10])
        #prevhomesales.lot_size = round(row[11])
        #prevhomesales.year_built = round(row[12])
        #prevhomesales.parking_spots = round(row[13])
        #prevhomesales.parking_type = row[14]
        #prevhomesales.days_on_market = round(row[15])
        #prevhomesales.status = row[16]
        #prevhomesales.next_open_house_date = row[17]
        #
        #
        #print prevhomesales.next_open_house_date
        #
        #
        #prevhomesales.next_open_house_start_time = row[18]
        #prevhomesales.next_open_house_end_time = row[19]
        #prevhomesales.recent_reduction_date = row[20]
        #prevhomesales.original_list_price = round(row[21])
        #prevhomesales.last_sale_date = row[22]
        #prevhomesales.last_sale_price = round(row[23])
        #prevhomesales.url = row[24]
        #prevhomesales.source = row[25]
        #prevhomesales.listing_id = row[26]
        #prevhomesales.original_source = row[27]
        #prevhomesales.favorite = row[28]
        #prevhomesales.interested = row[29]
        #prevhomesales.latitude = row[30]
        #prevhomesales.longitude = row[31]
        #prevhomesales.is_short_sale = row[32]
        print prevhomesales
        prevhomesales.save()