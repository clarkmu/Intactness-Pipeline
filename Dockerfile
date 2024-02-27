FROM ubuntu:18.04

# set Miniconda3 in path
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# update Ubuntu
RUN apt update && apt upgrade -y
RUN apt install software-properties-common \
    wget curl libcurl4 git gcc task-spooler -y

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

# RUN git clone https://github.com/BWH-Lichterfeld-Lab/Intactness-Pipeline.git /app/intactness

#PORT
EXPOSE 8181

#WORKDIR /app

CMD ["sleep","infinity"]