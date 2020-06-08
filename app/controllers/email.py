from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from app.utils.global_vars import sombot_email
from app.controllers.qrcode_controller import qrcode_generation
from app.utils.email_authorization import gmail_server
from typing import List

class EmailAuthenticate(object):
    def __init__(self):
        self.sombot_email = sombot_email

class AudienceEmail(EmailAuthenticate):
    def __init__(self, identity, email):
        self.identity = identity
        self.email = email
        super().__init__()

    def construct_email(self, subject, message):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sombot_email
        msg['To'] = self.email

        body = MIMEText(message)
        msg.attach(body)

        qrcode_jpeg = qrcode_generation(self.identity)
        qrcode_image = MIMEImage(qrcode_jpeg, name="sombot_ticket_invitation_to_event.jpeg")
        msg.attach(qrcode_image)

        return msg.as_string()

def send_email(audiences: List[AudienceEmail], **detail):
    subject = detail.get("subject")
    msg = detail.get("message")
    from_email = audiences[0].sombot_email
    for audience in audiences:
        email_messages = audience.construct_email(subject, msg)
        gmail_server.sendmail(from_email, audience.email, email_messages)
