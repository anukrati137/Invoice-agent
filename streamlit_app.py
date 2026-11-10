import os
import streamlit as st
from dotenv import load_dotenv
from app import get_token, create_invoice, send_invoice, get_status

load_dotenv()
st.set_page_config(page_title="Invoice Agent", page_icon="🧾")
st.title("🧾 AI Invoice Agent")
st.caption("Describe the invoice in plain English. Review it, then send via PayPal (sandbox).")

if "invoices" not in st.session_state:
    st.session_state.invoices = []
if "draft" not in st.session_state:
    st.session_state.draft = None

client_email = st.text_input(
    "Client email (your US sandbox personal account)",
    value=os.getenv("CLIENT_EMAIL", ""),
)
request = st.text_input(
    "Invoice request", placeholder="Invoice Rahul $50 for logo design, due in 7 days"
)

if st.button("Parse request") and request:
    with st.spinner("Loading Gemini and parsing (first time can take a minute)..."):
        try:
            from parser import parse_request
            st.session_state.draft = parse_request(request)
        except Exception as e:
            st.error(f"Could not parse that request: {e}")

draft = st.session_state.draft
if draft:
    st.subheader("Confirm before sending")
    total = sum(i["amount"] for i in draft["items"])
    st.write(f"**Client:** {draft['client_name']}")
    for i in draft["items"]:
        st.write(f"- {i['name']}: ${i['amount']:.2f}")
    st.write(f"**Total:** ${total:.2f} · due in {draft['due_days']} days")

    c1, c2 = st.columns(2)
    if c1.button("✅ Send invoice"):
        try:
            token = get_token()
            url = create_invoice(
                token, draft["client_name"], client_email,
                draft["items"], draft["due_days"],
            )
            send_invoice(token, url)
            st.session_state.invoices.append(
                {"client": draft["client_name"], "total": total, "url": url}
            )
            st.session_state.draft = None
            st.success("Invoice sent!")
        except Exception as e:
            st.error(f"PayPal error: {e}")
    if c2.button("Cancel"):
        st.session_state.draft = None
        st.rerun()

st.subheader("Invoices")
if st.button("🔄 Refresh statuses"):
    token = get_token()
    for inv in st.session_state.invoices:
        inv["status"] = get_status(token, inv["url"])
for inv in st.session_state.invoices:
    st.write(f"{inv['client']} · ${inv['total']:.2f} · **{inv.get('status', 'SENT')}**")