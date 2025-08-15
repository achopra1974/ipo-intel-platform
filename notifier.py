import smtplib
import ssl
from email.message import EmailMessage
import telegram
import yaml

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

def send_email(subject: str, body: str):
    em_cfg = cfg["email"]
    msg = EmailMessage()
    msg["From"] = em_cfg["username"]
    msg["To"] = ", ".join(em_cfg["recipients"])
    msg["Subject"] = subject
    msg.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP(em_cfg["smtp_server"], em_cfg["smtp_port"]) as smtp:
        smtp.starttls(context=context)
        smtp.login(em_cfg["username"], em_cfg["password"])
        smtp.send_message(msg)

def send_telegram(message: str):
    tg = cfg["telegram"]
    bot = telegram.Bot(token=tg["bot_token"])
    bot.send_message(chat_id=tg["chat_id"], text=message)