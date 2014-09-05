#!/usr/bin/env
# Filename : 
#
# This file searches bing for twitter accounts of tv shows

import requests
import csv
import codecs
import sys
import time
from os.path import expanduser

streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)

home = expanduser("~")
showsfile = open(home+'XXXX.csv', 'rb') 
bingWriter = csv.writer(open(home+'XXXX.csv', 'wb'), delimiter=',')
t2 = []
t1 = time.time()

for show in showsfile:
    rbing = []
    t2 = time.time() - t1
    if t2 < 1:
        time.sleep(1 - t2)
    print t2, show
    querylink = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web?Query=%27' + show + '%20site%3Aimdb.com%27&Market=%27en-US%27&Adult=%27Off%27&$top=1&$format=JSON'
    # print querylink
    rbing = requests.get(querylink, auth=("XXXX", "XXXX")).json
    t1 = time.time()
    try:
        for i in rbing()['d']['results']:
            bingWriter.writerow([show, str(i['Url'].encode('ascii', 'ignore')), str(i['Title'].encode('ascii', 'ignore')), str(i['Description'].encode('ascii', 'ignore'))])
    except:
        bingWriter.writerow([show])
        continue