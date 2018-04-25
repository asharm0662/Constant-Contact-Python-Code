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
        
        'Authorization': 'Bearer f90badda-4711-460b-983e-f6bb42c34150',
        'X-Originating-Ip': '71.192.175.181',
        'Content-Type': 'application/json',

        }

headers = {
        
        'Authorization': 'Bearer f90badda-4711-460b-983e-f6bb42c34150',
        'Content-Type': 'application/json',

        }



data1 = { "name": "Birthday_030720181100","status": "ACTIVE"}

r = requests.post('https://api.constantcontact.com/v2/lists?api_key=rc8yge9pst6vkzfwhnkumq9j', json = data1, headers = headers)

print(r)
print(r.text)


### GET List ID


headers = {
        
        'Authorization': 'Bearer f90badda-4711-460b-983e-f6bb42c34150',
        'X-Originating-Ip': '71.192.175.181'
        }


r1 = requests.get('https://api.constantcontact.com/v2/lists?api_key=rc8yge9pst6vkzfwhnkumq9j', headers=headers)
print(r1.text)
lists= pd.read_json(r1.text)
lists



### 2. Insert contacts into list

headers = {
        
        'Authorization': 'Bearer f90badda-4711-460b-983e-f6bb42c34150',
        'X-Originating-Ip': '71.192.175.181',
        'Content-Type': 'application/json',

        }



headers_mjf= {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-mjf-api-key': 'c80fe35a-f021-11e7-ae63-02d90dec2190',
        'x-mjf-organization-id': '184',
        'x-mjf-facility-id': '400',
        'x-mjf-user-id': '487',
    }
    

r_consumers = requests.get('https://partner-gateway.mjplatform.com/v1/consumers', headers=headers_mjf, verify=False)

df = pd.read_json(r_consumers.text)


df2 = df[['first_name', 'last_name', 'email_address']].copy()
df2.rename(columns={'email_address': 'email_addresses'}, inplace=True)
df2.columns = df2.columns.str.strip()
df2['email_addresses'][5] = 'test234@test234.com'
df2['email_addresses'] = df2['email_addresses'].apply(lambda x: [x])
update_contact = {"import_data" : df2.to_dict(orient='records'),  "lists" : ["1113541378"]}

a = json.dumps(update_contact,ensure_ascii=False).encode('utf8')

r = requests.post('https://api.constantcontact.com/v2/activities/addcontacts/?api_key=rc8yge9pst6vkzfwhnkumq9j', headers=headers ,data = a)

print(r.text)


##Email Sending

headers_scheduler = {
        
        'Authorization': 'Bearer f90badda-4711-460b-983e-f6bb42c34150',
        'X-Originating-Ip': '71.192.175.181',
        'Content-Type': 'application/json',

        }

b= {}

scheduler_test = requests.post('https://api.constantcontact.com/v2/emailmarketing/campaigns/1129884618032/schedules?api_key=rc8yge9pst6vkzfwhnkumq9j',headers=headers_scheduler ,json = b )

print(scheduler_test.text)






###Delete Contact list###
headers_deletelist = {
        
        'Authorization': 'Bearer f90badda-4711-460b-983e-f6bb42c34150',
        'X-Originating-Ip': '71.192.175.181',
    }

    
rsp = requests.get('https://api.constantcontact.com/v2/lists/1113541378?api_key=rc8yge9pst6vkzfwhnkumq9j', headers = headers_deletelist)
rsp.text


###Creates new list in Constant Contact, based on date and time variables##################

headers = {
        
        'Authorization': 'Bearer f90badda-4711-460b-983e-f6bb42c34150',
        'Content-Type': 'application/json',

        }

now = datetime.datetime.now().strftime("%m%d%Y%H%M")

data1 = '{ "name": "Birthday_%s","status": "ACTIVE"}'
data1 = (data1 % now)

r = requests.post('https://api.constantcontact.com/v2/lists?api_key=rc8yge9pst6vkzfwhnkumq9j', data = data1, headers = headers)

print(r)
print(r.text)

###GET list ID##############################################################################

headers = {
        
        'Authorization': 'Bearer f90badda-4711-460b-983e-f6bb42c34150',
        'X-Originating-Ip': '71.192.175.181'
        }


listid_staging_api_call = requests.get('https://api.constantcontact.com/v2/lists?api_key=rc8yge9pst6vkzfwhnkumq9j', headers=headers)

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
