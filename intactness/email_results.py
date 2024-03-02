from os import path, remove
from tarfile import open

from .email import Email

def send_results(email, path_dat):
    zipped_results=f'{path_dat}/results.tar.gz'

    title="Intactness Results"
    body = "Attached are the results from your Intactness analysis."

    job_finished=path.exists(zipped_results)

    if not job_finished:
        title="Intactness Failed"
        body="Failed to run Intactness analysis."
    else:
        # tar path_dat
        with open(zipped_results, 'w:gz') as tar:
            tar.add(path_dat, arcname=path.basename(path_dat))

    # setup email, attach tar

    email = Email(email, title, body)
    if job_finished:
        email.add_attachment(zipped_results)
    email.send()

    # os.remove(zipped_results)

    return "OK"