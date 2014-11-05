from geopy.geocoders import GoogleV3

def geolocate(address):
    geolocator = GoogleV3(api_key='AIzaSyBYVngMReah5qDa3j-ZZqpwkvxJ-7gYecs')
    location = geolocator.geocode("73 Sumner St Apt 303 San Francisco, CA 94103")
    
    print(location.address)
    print(location.latitude, location.longitude)
    print(location.raw)
    
    return location