class queryCymru:
    ipList=[]
    def __init__(self, cymru_config):
        self.cymru_config=cymru_config

    def read_file(self, fileWithPath):
        with open(fileWithPath) as f:
            line = f.read().strip()
            self.ipList.append(line)

    def queryIP_List(self):
        print ("Submitting IP Job to Team Cymru")
        print ("Flows will be a seperate Job, they are large")

    def queryDomain_List(self):
        print("Submitting DNS to Team Cymru")

    def queryHash_List(self):
        print("Submitting Hashes to Team Cymru")


