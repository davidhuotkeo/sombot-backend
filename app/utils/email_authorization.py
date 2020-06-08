import smtplib
from app.utils.global_vars import (sombot_email, sombot_password)

gmail_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
gmail_server.ehlo()
try:
    gmail_server.login(sombot_email, sombot_password)
except:
    pass
