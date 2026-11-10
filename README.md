# AI Invoice Agent

Describe an invoice in plain English, review it, and send it through PayPal. Built for the PayPal AI Hackathon.

"Invoice Rahul $50 for logo design, due in 7 days"

Freelancers lose time chasing payments and filling in invoice forms. This agent turns one sentence into a real PayPal invoice, asks you to confirm it, sends it, and tracks whether it has been paid.

## How it works
You type a request in everyday language.
Gemini parses it into structured data: client name, line items, amounts (USD), and due days.
You confirm the parsed invoice on a review card. Nothing is sent until you approve.
PayPal's Invoicing API (sandbox) creates and sends the invoice.
Refresh statuses to see whether it is SENT or PAID.

Due dates are rounded up to PayPal's standard payment terms (10, 15, 30, 45, 60 or 90 days), so "due in 7 days" becomes Net 10.

Tech stack
Python and Streamlit (UI)
Google Gemini API (natural-language parsing, with retry and model fallback)
PayPal Invoicing REST API (sandbox)
Setup

Requirements: Python 3.10 or newer, a free PayPal Developer account, and a Gemini API key.

### 1. Clone and install
bash
git clone https://github.com/anukrati137/Invoice-agent.git
cd Invoice-agent
pip install -r requirements.txt

 ### 2. Create PayPal sandbox accounts
Log in at developer.paypal.com and open Testing Tools → Sandbox Accounts.
You need two sandbox accounts:
a Business account (the freelancer who sends invoices), and
a Personal account (the client who pays).
Set the Personal (client) account's country to United States. PayPal blocks sending invoices to customers in India, so an India-based test client causes a send error.
Under Apps & Credentials (Sandbox), create an app linked to the Business account and make sure Invoicing is enabled. Copy the Client ID and Secret.

### 3. Add your keys to .env and fill in the values:

PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_secret
GEMINI_API_KEY=your_gemini_key
CLIENT_EMAIL=your_us_sandbox_personal_email

.env is git-ignored, so your keys are never committed.

### 4. Run
bash
streamlit run streamlit_app.py

The first click on Parse request can take a moment while the Gemini library loads.

Try it
Enter the sandbox Personal account's email as the client email.
Type: Invoice Rahul $50 for logo design, due in 7 days and click Parse request.
Check the confirmation card and click Send invoice.
Log into sandbox.paypal.com with the Personal account and pay the invoice.
Back in the app, click Refresh statuses and watch it change to PAID.
Project structure
File	Purpose
streamlit_app.py	Web UI: request box, confirmation card, invoice list
parser.py	Gemini parsing of the request into JSON, with retries and fallback models
app.py	PayPal sandbox calls: token, create invoice, send, status
requirements.txt	Python dependencies
Limitations
Sandbox only: no real money moves.
Invoices are listed in memory for the current session, so the list resets when the page is refreshed.
Invoices are in USD.
AI tools used
Google Gemini API: parses natural-language requests into structured invoice data.
Coding assistants used - Claude: used for code help and debugging during development.
License

MIT. See LICENSE.
