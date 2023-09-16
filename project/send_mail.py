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

def sub_letter(receiver_email):
    content = """<html>
    <head>
        <title>Thanks For Subscribing</title>
        <style>
            body, html {
                width: 100%;
                margin: 0;
                padding: 0;
                background-color: #d1d1d1;
            }
            #container {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 50px;
            }
            .line {
                background-color: #c8c8c8;
                height: 1px;
                width: 100%;
                border: none;
                outline: none;
            }
            .icon {
                width: 130px;
            }
            a {
                text-decoration: underline;
                color: black;
            }
            .letter {
                text-align: center;
                margin: 8px 0px;
                color: black;
            }
            .image {
                text-align: center;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <main id="container">
            <div class="image">
                <a href="https://grabaltyofficial.com"><img class="icon" src="http://grabaltyofficial.com/static/GRABALTY-final.png" alt="GRABALTY"></a>
            </div>
            <hr class="line">
            <p class="letter">
                We thank you for subscribing to our newsletter and for your interest in Grabalty. You will no be able to follow our exclusive offers, novelties and news.
            </p>
            <p class="letter">
                We hope to see you again on <a target="_blank" href="https://grabaltyofficial.com">grabaltyofficial.com</a>.
            </p>
        </main>
    </body>
</html>
"""
    send_mail(receiver_email, "Thanks For Subscribing", content)

