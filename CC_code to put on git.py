#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 10:28:12 2018

@author: adityasharma
"""

import pandas as pd
import requests
import json


## 1. Create Constant ContactList with a Date-Based Name(ie Dynamic)

headers1 = {
        
        'Authorization': 'x',
        'X-Originating-Ip': 'x',
        'Content-Type': 'application/json',

        }

headers = {
        
        'Authorization': 'x',
        'Content-Type': 'application/json',

        }



data1 = { "name": "Birthday_030720181100","status": "ACTIVE"}

r = requests.post('https://api.constantcontact.com/v2/lists?api_key=x', json = data1, headers = headers)

print(r)
print(r.text)


### GET List ID


headers = {
        
        'Authorization': 'x',
        'X-Originating-Ip': 'x'
        }


r1 = requests.get('https://api.constantcontact.com/v2/lists?api_key=x', headers=headers)
print(r1.text)
lists= pd.read_json(r1.text)
lists






##Email Sending

headers_scheduler = {
        
        'Authorization': 'x',
        'X-Originating-Ip': 'x',
        'Content-Type': 'application/json',

        }

b= {}

scheduler_test = requests.post('https://api.constantcontact.com/v2/emailmarketing/campaigns/1129884618032/schedules?api_key=x',headers=headers_scheduler ,json = b )

print(scheduler_test.text)






###Delete Contact list###
headers_deletelist = {
        
        'Authorization': 'x',
        'X-Originating-Ip': 'x',
    }

    
rsp = requests.get('https://api.constantcontact.com/v2/lists/1113541378?api_key=x', headers = headers_deletelist)
rsp.text


###Creates new list in Constant Contact, based on date and time variables##################

headers = {
        
        'Authorization': 'x',
        'Content-Type': 'application/json',

        }

now = datetime.datetime.now().strftime("%m%d%Y%H%M")

data1 = '{ "name": "Birthday_%s","status": "ACTIVE"}'
data1 = (data1 % now)

r = requests.post('https://api.constantcontact.com/v2/lists?api_key=x', data = data1, headers = headers)

print(r)
print(r.text)

###GET list ID##############################################################################

headers = {
        
        'Authorization': 'x',
        'X-Originating-Ip': 'x'
        }


listid_staging_api_call = requests.get('https://api.constantcontact.com/v2/lists?api_key=x', headers=headers)

listid_staging= pd.read_json(listid_staging_api_call.text)
listid_staging.created_date = listid_staging.created_date.astype(str)
listid_staging.id = listid_staging.id.astype(str)
listid_staging.modified_date = listid_staging.modified_date.astype(str)
listid_staging.name = listid_staging.name.astype(str)
listid_staging.status = listid_staging.status.astype(str)


listid_staging_converted = pd.DataFrame(listid_staging)
listid_staging_converted['created_date'] = pd.to_datetime(listid_staging_converted['created_date'])
listid_staging_converted['modified_date'] = pd.to_datetime(listid_staging_converted['modified_date'])

listid_permanent = pd.DataFrame(listid_staging_converted)


###API Call to Import email addresses into List#######################################
listid_permanent = listid_permanent[listid_permanent['name'].str.contains('Birthday_03', na = False)]
listid_permanent = listid_permanent.reset_index()
ids = listid_permanent.at[0,'id']
