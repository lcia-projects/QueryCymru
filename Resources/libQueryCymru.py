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
    def readFile(self, fileWithPath):
        with open(fileWithPath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                self.scrapeIPs(line)
                self.scrapeURL(line)
                self.scrapeHashes(line)

                line = fp.readline()
                cnt += 1

            self.ipList=self.removeListDuplicates(self.ipList)
            self.urlList=self.removeListDuplicates(self.urlList)
            self.hashList=self.removeListDuplicates(self.hashList)

    # pulls URLs from file
    def scrapeURL(self, line):
        extractor = URLExtract()
        urls = extractor.find_urls(line)

        print ("# of URLS:", len(urls))
        if len(urls) > 0:
            for item in urls:
                ipTest = str(item)
                ipTest = ipTest.replace(".", "")
                print ("Line:", line)
                # This is some UGLY code, but i havent found a better way, urlextract pulls IP addresses too, i need
                # IP addresses in a seperate list.. so to test if its an ip address, i pull the urlextracted string
                # remove any "." from it.. and try to convert it to an integer.. if it works.. its an ip address
                # if it fails its a URL.
                try:
                    ipTest = int(ipTest)
                except:
                    print("URL:", item)
                    self.urlList.append(item)

    def scrapeIPs(self,line):
        addresses=[]
        filteredAddresses=[]

        addresses += re.findall(
            r'(\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b)',
            line)

        for address in addresses:
            if not (re.match(
                    r'^0.\d{1,3}.\d{1,3}.\d{1,3}$|^127.\d{1,3}.\d{1,3}.\d{1,3}$|^169.254.\d{1,3}.\d{1,3}$|^10.\d{1,3}.\d{1,3}.\d{1,3}$|^172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}$|^192.168.\d{1,3}.\d{1,3}$',
                    address)):
                filteredAddresses.append(address)

        for item in filteredAddresses:
            self.ipList.append(item)

        print ("IPs Scraped:", len(self.ipList))

    def scrapeHashes(self,line):
        hashList = []

        # look for md5's
        md5 = re.findall(r"([a-fA-F\d]{32})", line)
        for item in md5:
            hashList.append(item)

        # look for sha1's
        sha1 = re.findall(r"(\b[0-9a-f]{40}\b)", line)
        for item in sha1:
            hashList.append(item)

        for item in hashList:
            self.hashList.append(item)

    def removeListDuplicates(self, list2dedupe):
        #removes duplicates
        before=len(list2dedupe)
        list2dedupe=list(set(list2dedupe))
        after=len(list2dedupe)
        print ("Before:", before, ":", "After", after)
        return list2dedupe.copy()

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