import os
import requests
import smtplib
import xml.etree.ElementTree as ET

from email.mime.text import MIMEText
from google import genai

from datetime import datetime

today = datetime.now().strftime("%d %b %Y")


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
You are a world-class football journalist.

Using the news below, create an engaging daily FIFA World Cup briefing.

Structure:

🏆 Tournament Headlines

🔥 Biggest Story

📊 Yesterday's Results
- Mention scores if available
- Mention goalscorers if available
- State whether the result was expected or an upset

⭐ Players to Watch
- Mention club team

📅 Today's Key Matches

🎯 Prediction of the Day

Write in a professional sports-journalism style.

News:

{news_text}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

summary = response.text

msg = MIMEText(summary)

msg["Subject"] = f"⚽ FIFA World Cup Briefing | {today}"
msg["From"] = EMAIL_USER
msg["To"] = "amanbaweja007@gmail.com"

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
