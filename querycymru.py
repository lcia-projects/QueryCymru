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
    parser.add_argument('--dns', action="store_true", help='given input filename contains domain names/web addresses', required=False)
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
    if args['ip'] == False and args['dns']==False and args['hashset']==False:
        print ("Error, you must select one type of data to process ip, dns, hashset")
        exit()

    cymruObj=libQueryCymru.queryCymru(lookout_config)
    cymruObj.read_file(args['filename'])

    if args['ip']==True:
        cymruObj.queryIP_List()
    elif args['dns']==True:
        cymruObj.queryDomain_List()
    elif args['hashset']==True:
        cymruObj.queryHash_List()