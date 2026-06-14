import os
import requests
import smtplib
import xml.etree.ElementTree as ET

from email.mime.text import MIMEText
from google import genai

EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

# Google News RSS
rss_url = (
    "https://news.google.com/rss/search?"
    "q=FIFA+World+Cup"
)

rss = requests.get(rss_url)

root = ET.fromstring(rss.content)

items = root.findall(".//item")

news_text = ""

for item in items[:10]:

    title = item.find("title")

    if title is not None:
        news_text += f"- {title.text}\n"

prompt = f"""
You are a football analyst.

Here are the latest FIFA World Cup headlines:

{news_text}

Create a daily email containing:

1. Key developments
2. Important match results if mentioned
3. Upcoming storylines
4. Players or teams to watch

Keep it under 250 words.

Use bullet points.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

summary = response.text

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

print("Email sent successfully")
