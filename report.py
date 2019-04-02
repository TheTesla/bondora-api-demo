#!/usr/bin/env python


# curl https://api.bondora.com/api/v1/account/investments -H "Content-type: application/json" -H "Accept: application/json" -H "Authorization: Bearer H0kFRXrr8xHQQZzm99CxEGU0S2JwyIzTue6U3GUHIRAmP8g7" | jq .




import requests
import re

bearer = ''
with open('bearer.conf', 'r') as f:
    bearer = f.read()
    f.close()

bearer = re.sub('[^a-zA-Z0-9]' , '', bearer)

headers = { 'Authorization': 'Bearer {}'.format(bearer),
            'Content-Type':  'application/json',
            'Accept':        'application/json' }
r = requests.get('https://api.bondora.com/api/v1/report/1d257abb-8048-41bb-86eb-aa220020228f', headers=headers)
repayments = r.json()


try:
    prep = sum([e['PrincipalRepayment'] for i, e in enumerate(repayments['Payload']['Result'])])
    irep = sum([e['InterestRepayment'] for i, e in enumerate(repayments['Payload']['Result'])])
    lfrep = sum([e['LateFeesRepayment'] for i, e in enumerate(repayments['Payload']['Result'])])
    print("Principal Repayments:   {: 10.2f}".format(prep))
    print("Interest Repayments:    {: 10.2f}".format(irep))
    print("Late Fees Repayments:   {: 10.2f}".format(lfrep))
except:
    print(repayments)



