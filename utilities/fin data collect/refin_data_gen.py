

#read input zipcode file
zipcodes = []
with open("zipcodes.txt", "rb") as infile:
    for i in infile.readlines():
        zipcodes.append(i.strip())
print zipcodes

urls = []
with open("urls.txt", "rb") as infile:
    for i in infile.readlines():
        urls.append(i.strip())
print urls

outputtxt = ""

for i in zipcodes:
    for n in urls:
        outputtxt += "%s,%s\n" % (i,n)

print outputtxt

with open("mturk_result.csv", "wb") as outfile:
    outfile.write("zipcode,url\n")
    outfile.write(outputtxt)


#output a list of zip codes
#read url list file
#output a list of URLs
#create text that outputs csv of zipcode, URL type with header
#saves this files