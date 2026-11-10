import os, json, time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT = """Extract an invoice from the request below. Return ONLY JSON:
{{"client_name": string, "items": [{{"name": string, "amount": number}}], "due_days": integer}}
Amounts are in USD. If no due date is given, use 10 for due_days.
Request: {text}"""

MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest",
    "gemini-3.5-flash",
]


def parse_request(text):
    last_error = None
    for model in MODELS:
        for attempt in range(2):
            try:
                resp = client.models.generate_content(
                    model=model,
                    contents=PROMPT.format(text=text),
                    config={"response_mime_type": "application/json"},
                )
                return json.loads(resp.text)
            except Exception as e:
                last_error = e
                time.sleep(2)
    raise last_error


if __name__ == "__main__":
    print(parse_request("invoice Rahul $50 for logo design, due in 7 days"))


