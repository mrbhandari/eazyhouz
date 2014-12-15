import re
import urllib
import json
import requests
import sys

def normalize_address(address):
	return address.lower().replace(" apt ", " #").replace(" unit "," #").title()

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'
headers = {
	'User-Agent': ua,
}
lines = open(sys.argv[1]).readlines()
ind = 0
header_index = {}
for line in lines:
	line = line.strip()
	line1 = {}
	fields = line.split("\t")
	if ind == 0:
		for i in range(0,len(fields)):
			header_index[i] = fields[i]	
			ind += 1
		continue
	else:
		ind += 1
		for i in range(0,len(fields)):
			line1[header_index[i]] = fields[i]
	redfin_url = line1["URL"]

	id = redfin_url.split("/")[-1]
	if re.match(r'[a-z]+',id):
		id = redfin_url.split("/")[-2]
	schools = []
	url = "https://www.redfin.com/stingray/phantom/multicontroller?p=/stingray/&u=dataloader/property/" + id + "/schools"
	address = normalize_address(line1["ADDRESS"])
	r = requests.get(url, headers=headers)
 	d = json.loads(r.content[4:])
	try:
 		try:
 			for school in d['payload'][0]['payload']['__root']['__atts'][1]['__atts'][0]:
 				schools.append((school['__atts'][1], school['__atts'][-2]))
	 	except TypeError as e:
 			for school in d['payload'][0]['payload']['__root']['__atts'][0]['__atts'][0]:
 				schools.append((school['__atts'][1], school['__atts'][-2]))
	 	for school in schools:
 			print id,"\t",address,"\t",redfin_url,"\t", school[0],"\t", school[1]
	except:
 		pass
