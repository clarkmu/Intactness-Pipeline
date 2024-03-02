import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class Email:
    def __init__(self, receiver, subject, body):
        self.subject = subject
        self.receiver = receiver
        self.sender = "clarkmu@unc.edu"
        self.server = "relay.unc.edu"
        self.port = 25
        self.attachments = []
        self.body = "Dear Primer ID user,\n\n" + body + \
            "\n\nIf you have any questions, please feel free to <a href='https://primer-id.org/contaact'>Contact Us</a>." + \
            "\nTCS/DR team @UNC"

    def add_attachment(self, file_path):
        self.attachments.append(file_path)

    def send(self):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = self.receiver
            msg['Subject'] = self.subject
            msg.attach(self.body)

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
            print(e)
            return False