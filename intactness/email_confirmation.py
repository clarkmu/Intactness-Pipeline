
from intactness.email import Email

def send_confirmation(email, more_content=""):
    body = "Thank you for using Primer ID.\n\n" + \
        "Your Intactness analysis has been submitted. " + \
        "You will receive an email with the results shortly.\n\n" + \
        more_content
    email = Email(email, "Intactness Confirmation", body)
    email.send()