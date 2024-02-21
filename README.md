# Docker Installation

Docker is used for creating compute environments that exactly match where they were created.  This aleviates a lot of the hassle of running code written by others.

Follow [this link](#https://docs.docker.com/get-docker/) to install. <small>If link is outdated, search "How to install docker"</small>

This Docker image uses `port 8181` to operate.  If your port 8181 is in use, edit `/docker.sh` and `/Dockerfile` to any available port (example, `3001`)

<i>If you are not running an Apple Silicon machine (M-series), see line 6-9 of /docker.sh</i>

# Pipeline Installation

Create a Docker image using the commands below. Installs dependencies with correct versions.

```
cd /path/to/this/directory
sh docker.sh build
sh docker.sh start
```

# Running instruction

Place your sequence file somewhere in this directory (ex: `./data/sample.fasta`)

```
cd /path/to/this/directory
sh docker.sh bash
cd /app
python3 -m intactness -in /app/data/sample.fasta
```

Point the `-in` flag to your sequence file.

Result summary will be found at `-in/intactness/summary.csv`

Genome diagrams will be found at `-in/intactness/Alignment_Views/*`

Note: /app is the working directory for this Docker environment.  It links and updates this code on your computer to that location.