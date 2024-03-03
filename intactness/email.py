from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
# from html import unescape

#TODO when attaching html AND text, email sends both (should send one or the other)

class Email:
    def __init__(self, receiver, subject, body):
        self.subject = subject
        self.receiver = ", ".join(receiver)
        self.sender = "clarkmu@unc.edu"
        self.server = "relay.unc.edu"
        self.port = 25
        self.attachments = []
        self.body_html = "Dear Primer ID user,</br></br>" + body.replace("\n", "</br>") + \
            "</br></br>If you have any questions, please feel free to <a href='https://primer-id.org/contact'>Contact Us</a>." + \
            "</br>TCS/DR team @UNC"
        # self.body_text = "Dear Primer ID user,\n\n" + unescape(body.replace("</br>", "\n")) + \
        #     "\n\nIf you have any questions, please feel free to contact us at https://primer-id.org/contact." + \
        #     "\nTCS/DR team @UNC"

    def add_attachment(self, file_path):
        self.attachments.append(file_path)

    def send(self):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = self.receiver
            msg['Subject'] = self.subject

            body_html = MIMEText(self.body_html.encode("utf-8"), "html", 'utf-8')
            msg.attach(body_html)
            # body_text = MIMEText(self.body_text.encode("utf-8"), "text", 'utf-8')
            # msg.attach(body_text)

            for file in self.attachments:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(file, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
                msg.attach(part)

            mailServer = smtplib.SMTP(self.server, self.port)
            mailServer.starttls()
            mailServer.sendmail(self.sender, self.receiver, msg.as_string())
            mailServer.close()
        except Exception as e:
            print(str(e))
            return False