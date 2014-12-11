import hashlib

def normalize_address(address):
   return address.lower().replace(" apt ", " #").replace(" unit "," #").title()
def get_eazyhouz_hash(home):
   return hashlib.sha1(home.address + home.city).hexdigest()