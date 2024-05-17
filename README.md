# Docker Installation

Docker is used for creating compute environments that exactly match where they were created.  This aleviates a lot of the hassle of running code written by others.

Follow [this link](#https://docs.docker.com/get-docker/) to install. <small>If link is outdated, search "How to install docker"</small>

This Docker image uses `port 8181` to operate.  If your port 8181 is in use, edit `/docker-compose.yml:line18` to any available port (example, `8182`)

<i>If you are not running an Apple Silicon machine (M-series), see line 4-11 of `/docker-compose.yml`</i>

# Pipeline Installation

Create a Docker image using the commands below. Installs dependencies with correct versions.

```
cd /path/to/this/directory
docker-compose up -d
```

This will download large amounts of data and might take a while.

# Running instruction

Place your sequence file somewhere in this directory (ex: `./data/sample.fasta`)

```
cd /path/to/this/directory
docker exec -it intactness bash
python3 -m intactness -in /app/data/sample.fasta
```

Point the `-in` flag to your sequence file.

Result summary will be found at `-in/intactness/summary.csv`

Genome diagrams will be found at `-in/intactness/Alignment_Views/*`

Note: /app is the working directory for this Docker environment.  It links and updates this code on your computer to that location.

## Troubleshooting

### Docker

Ensure your Docker client is running.
