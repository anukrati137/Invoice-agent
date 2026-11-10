import os, requests
from dotenv import load_dotenv

load_dotenv()
BASE = "https://api-m.sandbox.paypal.com"


def get_token():
    r = requests.post(
        f"{BASE}/v1/oauth2/token",
        auth=(os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_CLIENT_SECRET")),
        data={"grant_type": "client_credentials"},
    )
    r.raise_for_status()
    return r.json()["access_token"]

def term_for(days):
    for n in (10, 15, 30, 45, 60, 90):
        if days <= n:
            return f"NET_{n}"
    return "NET_90"

def create_invoice(token, client_name, client_email, items, due_days=10):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {
        "detail": {
            "currency_code": "USD",
            "payment_term": {"term_type": term_for(due_days)},
        },
        "primary_recipients": [
            {"billing_info": {
                "name": {"given_name": client_name},
                "email_address": client_email,
            }}
        ],
        "items": [
            {
                "name": it["name"],
                "quantity": "1",
                "unit_amount": {"currency_code": "USD", "value": f"{it['amount']:.2f}"},
            }
            for it in items
        ],
    }
    r = requests.post(f"{BASE}/v2/invoicing/invoices", json=body, headers=headers)
    print("create:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()["href"]  # URL of the new invoice


def send_invoice(token, invoice_url):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(
        f"{invoice_url}/send",
        json={"send_to_recipient": True, "send_to_invoicer": False},
        headers=headers,
    )
    print("send:", r.status_code, r.text)
    r.raise_for_status()


def get_status(token, invoice_url):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(invoice_url, headers=headers)
    r.raise_for_status()
    return r.json()["status"]


if __name__ == "__main__":
    token = get_token()
    url = create_invoice(
        token,
        client_name="Rahul",
        client_email="sb-f43h1o53757437@personal.example.com",
        items=[{"name": "Logo design", "amount": 50}],
    )
    send_invoice(token, url)
    print("status:", get_status(token, url))
    