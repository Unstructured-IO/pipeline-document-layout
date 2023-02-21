# syntax=docker/dockerfile:experimental

FROM centos:7

# NOTE(crag): NB_USER ARG for mybinder.org compat:
#             https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html
ARG NB_USER=notebook-user
ARG NB_UID=1000
ARG PIP_VERSION
ARG PIPELINE_PACKAGE

RUN yum -y update
RUN yum -y install gcc openssl-devel bzip2 bzip2-devel libffi-devel make git sqlite-devel \
    mesa-libGL xz-devel perl wget poppler-utils zlib-devel which centos-release-scl
RUN yum -y install devtoolset-7-gcc*
SHELL [ "/usr/bin/scl", "enable", "devtoolset-7"]
RUN wget https://www.python.org/ftp/python/3.8.16/Python-3.8.16.tgz && \
    tar -xzf Python-3.8.16.tgz

RUN cd Python-3.8.16 && \
    ./configure --enable-optimizations && \
    make -j 6 altinstall && cd .. && rm -rf Python-3*

RUN ln -s /usr/local/bin/python3.8 /usr/local/bin/python3
RUN export PATH=/usr/local/bin:$PATH 

# create user with a home directory
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}
ENV PATH $HOME/usr/local/bin/:$PATH

RUN groupadd --gid ${NB_UID} ${NB_USER}
RUN useradd --uid ${NB_UID}  --gid ${NB_UID} ${NB_USER}
USER ${NB_USER}
COPY requirements/dev.txt requirements-dev.txt
COPY requirements/base.txt requirements-base.txt
COPY prepline_document_layout prepline_document_layout
COPY pipeline-notebooks pipeline-notebooks

RUN python3 -m pip install --no-cache -r requirements-base.txt
RUN python3 -m pip install --no-cache -r requirements-dev.txt 
RUN python3 -m pip install ninja

RUN python3 -m pip install "detectron2@git+https://github.com/facebookresearch/detectron2.git@78d5b4f335005091fe0364ce4775d711ec93566e"
EXPOSE 8000
#CMD [ "python3","-m","uvicorn","prepline_document_layout.api.app:app","--host","0.0.0.0"]
