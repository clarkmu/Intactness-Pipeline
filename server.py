from fastapi import FastAPI, Request, HTTPException
import subprocess
from os import path, makedirs, unlink, environ
from io import StringIO
from Bio.SeqIO import parse as SeqIO_parse
from fastapi.middleware.cors import CORSMiddleware
from shutil import rmtree

from intactness.email_confirmation import send_confirmation

app = FastAPI()

origins = [
    "https://primer-id.org",
    "http://localhost",
    "http://localhost:3000",
    f"http://localhost:{environ['PORT']}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_job_count():
    tsp=subprocess.run(["tsp"], stdout = subprocess.PIPE,universal_newlines = True)
    count=0
    for line in tsp.stdout.split('\n'):
        if "running" in line or "queued" in line:
            count += 1
    return count

def path_to_submission(job_id):
    return f"/app/jobs/{job_id}"

@app.get("/")
def read_root():
    return "Server Running ✅"

#
@app.post("/submit_sequence")
async def post_sequence(req: Request):
    try:
        data = await req.json()
    except HTTPException as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    for whitelist in ["email", "sequences", "_id"]:
        if not whitelist in data:
            raise HTTPException(status_code=400, detail=f"No {whitelist} in input")

    try:
        email = data["email"]
        sequences = data["sequences"]
        job_id = data["_id"]

        submission_path=path_to_submission(job_id)
        makedirs(submission_path, exist_ok=True)

        # save email for this.rerun
        with open(f'{submission_path}/.email', 'w') as f:
            f.write(email)

        file_path = f'{submission_path}/seqs.fasta'

        # fasta_io = StringIO(sequences)
        # records = SeqIO_parse(fasta_io, "fasta")

        # if not records[0].id:
        #     raise HTTPException(status_code=400, detail="No sequences in input")

        # contents = ""
        # for record in enumerate(records):
        #     contents += f">{record.id}\n{record.seq}\n"
        # with open(file_path, 'wb+') as f:
        #     f.write(contents)

        with open(file_path, 'wb+') as f:
            f.write(sequences.encode('utf-8'))

        job_count = get_job_count()

        more_content = "Your sequences have been submitted to the Intactness Pipeline." + \
            f"\nJob ID: {job_id}\nThere are currently {job_count} submissions ahead of yours.\n\n"
        send_confirmation(email, more_content)

        # tsp python3 -m intactness -in /app/sample/sample.fasta
        subprocess.run(["tsp", "python3", "-m", "intactness", "-in", file_path, "-email", email])

        return {"success": True, "job_count": job_count}
    except BaseException as e:
        rmtree(submission_path)
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/job_count')
def job_count():
    return {"job_count": get_job_count()}

@app.get('/rerun/{job_id}')
def rerun(job_id):
    file_path = f'/app/jobs/{job_id}/seqs.fasta'

    #get email from submission
    email=""
    email_path = f'{file_path}/.email'
    if path.exists(email_path):
        with open(f'{file_path}/.email', 'r') as f:
            email = f.read()

    if not path.exists(f'{file_path}/summary.csv'):
        raise HTTPException(status_code=400, detail="Job is still running")

    # remove old files
    rmtree(f'/app/jobs/{job_id}/intactness', ignore_errors=True)

    subprocess.run(["tsp", "python3", "-m", "intactness", "-in", file_path, "-email", email])
    return {"success": True}