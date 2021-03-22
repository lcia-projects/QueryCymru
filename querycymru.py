# Louisiana State Police / Louisiana Cyber Investigators Alliance
# QueryCymru: simple script that pulls indicators from text file and submits jobs to team cymru
#
# - Resources:
#   -- https://team-cymru.com/

import yaml
import argparse
from os import path
from Resources import libQueryCymru

def argsParse():
    # ArgParse Configuration
    parser = argparse.ArgumentParser(description='Query Cymru',usage='querycymru.py --filename <filename to process> ', add_help=False)
    parser.add_argument('--filename', help='single file to process')
    parser.add_argument('--ip', action="store_true", help='given input filename contains ip addresses', required=False)
    parser.add_argument('--url', action="store_true", help='given input filename contains domain names/web addresses', required=False)
    parser.add_argument('--hashset', action="store_true", help='given input filename contains md5/sha1', required=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    YAMLFILE = "./querycymru.yaml"  # System Configuration and Variables
    queryResults = {}

    if (path.exists(YAMLFILE)):
        # -- Loads Configuration File for LookOut --
        with open(YAMLFILE, "r") as file:
            lookout_config = yaml.load(file, Loader=yaml.FullLoader)
    else:
        print("ERROR: No config file, please refer to lookout.yml.example in root folder of script")
        exit()


    # Process and error check commandline arguments
    args = argsParse()
    cymruObj = libQueryCymru.queryCymru(lookout_config)
    if args['ip'] == False and args['url']==False and args['hashset']==False:
        print ("No Specifics Given, Scraping and Querying for IPs, URLs, and Hashes")
        cymruObj.readIP_file(args['filename'])
        cymruObj.readURL_file(args['filename'])
        cymruObj.readHash_file(args['filename'])

        cymruObj.queryIP_List()
        cymruObj.queryDomain_List()
        cymruObj.queryHash_List()

    if args['ip']==True:
        cymruObj.readIP_file(args['filename'])
        cymruObj.queryIP_List()

    if args['url']==True:
        cymruObj.readURL_file(args['filename'])
        cymruObj.queryDomain_List()

    if args['hashset']==True:
        cymruObj.readHash_file(args['filename'])
        cymruObj.queryHash_List()








