from geopy.geocoders import GoogleV3
from address import AddressParser, Address


def geolocate(address):
    geolocator = GoogleV3(api_key='AIzaSyBYVngMReah5qDa3j-ZZqpwkvxJ-7gYecs')
    location = geolocator.geocode(address)
    loc = {}
    try:
        print(location.latitude, location.longitude)
        
        formatted_address = location.address
        print formatted_address

        alist = formatted_address.split(",")
        
        print alist
        
        loc['firstline'] = alist[0].strip()
        loc['city'] = alist[1].strip()
        loc['state'] = alist[2].split(" ")[1].strip()
        loc['zipcode'] = alist[2].split(" ")[2].strip()
        loc['latitude'] = location.latitude
        loc['longitude'] = location.longitude
        
        print loc.get('firstline'), loc.get('city'), loc.get('state'), loc.get('zipcode')

    except (AttributeError, IndexError) as e: #catches if Geolocation fails
        pass
    
    return loc