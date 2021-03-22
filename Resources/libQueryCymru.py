import sys
import re
from urlextract import URLExtract

# regex md5: re.findall(r"([a-fA-F\d]{32})", data)
# regex sha1: re.findall(r"(\b[0-9a-f]{5,40}\b, data)

class queryCymru:
    ipList=[]
    urlList=[]
    hashList=[]

    def __init__(self, cymru_config):
        self.cymru_config=cymru_config

### Reading Files Line By Line and looking for IP addresses, URLs, hash values
    ## this is NOT super efficient, i will clean it up into one method eventually
    ## the reason i dont read in the entire fire then process it is we get VERY large log files, reading line by line
    ## is slower but allows me not to have to worry about how large the file is, its not trying to fit the data into
    ## ram, its only putting one line of data in ram at a time.

    # pulls ip addresses from text file
    def readIP_file(self, fileWithPath):
        addresses = []
        filteredAddresses = []
        # Open each specified file for processing
        try:
            f = open(fileWithPath, 'r', encoding='ISO-8859-1')
        except IOError:
            print('Could not find the specified file:', fileWithPath)
            sys.exit(1)

        # Parse file for valid IPv4 addresses via RegEx
        addresses += re.findall(
            r'(\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b)',
            f.read())
        f.close()

        # Count number of occurrences for each IP address
        from collections import Counter
        addressCounts = Counter(addresses)

        # Remove duplicates from list
        addresses = set(addresses)

        # Filter list to eliminate bogon addresses, the loopback network, link local addresses, and RFC 1918 ranges; add results to new list
        for address in addresses:
            if not (re.match(
                    r'^0.\d{1,3}.\d{1,3}.\d{1,3}$|^127.\d{1,3}.\d{1,3}.\d{1,3}$|^169.254.\d{1,3}.\d{1,3}$|^10.\d{1,3}.\d{1,3}.\d{1,3}$|^172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}$|^192.168.\d{1,3}.\d{1,3}$',
                    address)):
                filteredAddresses.append(address)

        total = len(filteredAddresses)
        i = 0
        self.ipList = filteredAddresses

    # pulls URLs from file
    def readURL_file(self, fileWithPath):
        urlList = []
        extractor = URLExtract()

        f = open(fileWithPath, 'r')

        # reads file, finds URLs adds all urls to python list
        line = f.readline()
        while line:
            urls=extractor.find_urls(line)
            for item in urls:
                ipTest=str(item)
                ipTest=ipTest.replace(".","")

                # This is some UGLY code, but i havent found a better way, urlextract pulls IP addresses too, i need
                # IP addresses in a seperate list.. so to test if its an ip address, i pull the urlextracted string
                # remove any "." from it.. and try to convert it to an integer.. if it works.. its an ip address
                # if it fails its a URL.
                try:
                    ipTest=int(ipTest)
                except:
                    print ("URL:", item)
                    urlList.append(item)
            line = f.readline()
        f.close()

        # removes duplicates
        urlList=list(set(urlList))
        self.urlList=urlList.copy()

    def readHash_file(self, fileWithPath):
        # regex md5: re.findall(r"([a-fA-F\d]{32})", data)
        # regex sha1: re.findall(r"(\b[0-9a-f]{5,40}\b, data)

        hashList=[]

        f = open(fileWithPath, 'r')

        # reads file, finds URLs adds all urls to python list
        line = f.readline()
        while line:
            # look for md5's
            md5=re.findall(r"([a-fA-F\d]{32})", line)
            for item in md5:
                hashList.append(item)

            # look for sha1's
            sha1 = re.findall(r"(\b[0-9a-f]{40}\b)", line)
            for item in sha1:
                hashList.append(item)

            line = f.readline()
        f.close()

        # removes duplicates
        hashList = list(set(hashList))
        self.hashList=hashList.copy()

    def queryIP_List(self):
        print ("Submitting IP Job to Team Cymru")
        print ("Flows will be a seperate Job, they are large")
        print ("IP Addresses Found:", len(self.ipList))

    def queryIP_List_Flows(self):
        print ("Get Flows")

    def queryDomain_List(self):
        print("Submitting DNS to Team Cymru")
        print ("URLs Found:", len(self.urlList))
        print (self.urlList)

    def queryHash_List(self):
        print("Submitting Hashes to Team Cymru")
        print ("Hashes Found:", len(self.hashList))