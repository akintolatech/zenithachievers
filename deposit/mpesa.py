import base64, requests, datetime
from django.conf import settings

def _base_url():
    return "https://sandbox.safaricom.co.ke" if settings.MPESA_ENV == "sandbox" else "https://api.safaricom.co.ke"

def get_access_token():
    r = requests.get(
        _base_url() + "/oauth/v1/generate?grant_type=client_credentials",
        auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET)
    )
    r.raise_for_status()
    return r.json()["access_token"]

def lipa_na_mpesa_online(amount, phone, account_ref, description):
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{ts}".encode()
    ).decode()
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": ts,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_ref,
        "TransactionDesc": description[:13],
    }
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(
        _base_url() + "/mpesa/stkpush/v1/processrequest",
        json=payload, headers=headers, timeout=30
    )
    r.raise_for_status()
    return r.json()
