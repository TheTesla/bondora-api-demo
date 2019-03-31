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
r = requests.get('https://api.bondora.com/api/v1/account/investments', headers=headers)
invests = r.json()

startBonus = 5.00

try:
    issued = sum([e['PurchasePrice'] for i, e in enumerate(invests['Payload']) if e['LoanStatusCode'] not in [3]])
    outstandingPrincipal = sum([e['PrincipalRemaining'] for i, e in enumerate(invests['Payload']) if e['LoanStatusCode'] in [2,5,100]])
    overduePrincipal = sum([e['PrincipalLateAmount'] for i, e in enumerate(invests['Payload'])])
    earnings = sum([e['NoteLoanTransfersEarningsAmount'] for i, e in enumerate(invests['Payload'])])
    print("Loans Issued (price)     {: 10.2f}".format(issued))
    print("                                  ")
    print("Account Value:           {: 10.2f}".format(outstandingPrincipal-overduePrincipal))
    print("  Outstanding Principal: {: 10.2f}".format(outstandingPrincipal))
    print("  Overdue Principal:     {: 10.2f}".format(-overduePrincipal))
    print("                                  ")
    print("Profit:                  {: 10.2f}".format(earnings+startBonus-overduePrincipal))
    print("  Start Bonus:           {: 10.2f}".format(startBonus))
    print("  Gross Profit:          {: 10.2f}".format(earnings-overduePrincipal))
    print("    Interest Paid        {: 10.2f}".format(earnings))
    print("    Overdue Principal:   {: 10.2f}".format(-overduePrincipal))
except:
    print(invests)



