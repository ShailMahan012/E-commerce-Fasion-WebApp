import smtplib
import ssl
from base64 import b64decode as decode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(receiver_email, subject, content):
    smtp_server = "premium297.web-hosting.com"
    sender_email = "noreply@grabaltyofficial.com"
    password = "noreply012"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    
    part = MIMEText(content, "html")

    message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
