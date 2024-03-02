FROM ubuntu:18.04

MAINTAINER Michael Clark <clakrmu@unc.edu>

ENV PORT=8080

LABEL maintainer="Michael Clark <clakrmu@unc.edu>" \
    io.k8s.description="Processes intactness pipeline for https://primer-id.org" \
    io.k8s.display-name="Intactness Pipeline Server" \
    io.openshift.expose-services="${PORT}:http"

# set Miniconda3 in path

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# update Ubuntu
RUN apt update && apt upgrade -y

# gcc for biopython
RUN apt install software-properties-common \
    wget curl libcurl4 git gcc task-spooler vim -y

# install conda
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir -p /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

RUN conda init bash
RUN conda config --env --set always_yes true
RUN conda update conda

# intactness pipeline dependencies
RUN conda install python=3.8
RUN conda install bioconda::blast=2.12.0
RUN conda install bioconda::muscle=5.1
RUN pip3 install biopython==1.79 reportlab==4.1.0 lxml==5.1.0 \
                    PyPDF2==1.26.0 scipy==1.10.1

# install a webserver
RUN pip3 install fastapi starlette uvicorn python-multipart

#PORT
EXPOSE $PORT

WORKDIR /app

WORKDIR /app
COPY . .
RUN chmod -R 777 /app
RUN chmod -R 777 /root
USER 1001

# CMD sleep infinity
# CMD uvicorn server:app --reload --host 0.0.0.0 --port $PORT
ENTRYPOINT ["sh", "/app/entrypoint.sh"]