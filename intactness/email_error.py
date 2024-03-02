
from intactness.email import Email

def send_error(email, error_msg):
    body = f"An error has occurred on this intactness run.\n\n{error_msg}\n\n"
    email = Email([email, "clarkmu@unc.edu"], "Intactness Error", body)
    email.send()