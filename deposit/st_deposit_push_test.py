import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

# Credentials
consumer_key = 'jf92GGsWmG1WONs9fGrRbmMYfA5aaOkP2SsJdJoHkEMSflWb'
consumer_secret = 'HQPakSn7b2gQy3TfGDT2cOxBi7A9Q5Pr0q2gXSu0GglLCo30CZXliR8WoFkTGWW4'
shortcode = '174379'
passkey = 'bfb279f9aa9bdbcf15e97dd71a467cd2c2c8f84e8a01b1a248a56b9f7c5d2f52'
phone = '254708374149'  # Customer phone
amount = 100  # Amount to charge

# Get access token
token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
response = requests.get(token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
access_token = response.json()['access_token']

# Timestamp and password
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
password = base64.b64encode(f'{shortcode}{passkey}{timestamp}'.encode()).decode()

# STK Push
stk_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
payload = {
    "BusinessShortCode": shortcode,
    "Password": password,
    "Timestamp": timestamp,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": amount,
    "PartyA": phone,
    "PartyB": shortcode,
    "PhoneNumber": phone,
    "CallBackURL": "https://zenithachievers.com/make_deposit",
    "AccountReference": "YourRef001",
    "TransactionDesc": "Deposit"
}

res = requests.post(stk_url, json=payload, headers=headers)
print(res.json())
