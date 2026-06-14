import os
import requests
import smtplib

from email.mime.text import MIMEText
from google import genai

EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

LEAGUE_ID = "4843"

url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={LEAGUE_ID}"

response = requests.get(url)

print(response.text)

events = response.json().

match_text = ""

for event in events[:10]:
    match_text += (
        f"{event['dateEvent']} - "
        f"{event['strHomeTeam']} vs "
        f"{event['strAwayTeam']}\n"
    )

prompt = f"""
You are a football analyst.

Upcoming FIFA World Cup matches:

{match_text}

Create a short email containing:
1. Tournament overview
2. Today's most important matches
3. Teams to watch
4. Latest score

Keep it under 200 words.
"""

result = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

summary = result.text

msg = MIMEText(summary)

msg["Subject"] = "⚽ FIFA World Cup Daily Digest"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_USER

with smtplib.SMTP_SSL(
    "smtp.gmail.com",
    465
) as server:

    server.login(
        EMAIL_USER,
        EMAIL_PASSWORD
    )

    server.send_message(msg)

print("Email sent")
