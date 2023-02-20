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

RUN cd Python-3.8.16 && mkdir ~/.localpython && \
    ./configure --enable-optimizations --prefix=/root/.localpython && \
    make -j 6 altinstall
#RUN /root/.localpython/bin/python3.8 -m pip install --upgrade pip
RUN export PATH=/root/.localpython/bin:$PATH && \
    export LD_LIBRARY_PATH=/root/openssl/lib && \
    export LDFLAGS="-L /root/openssl/lib -Wl,-rpath,/root/openssl/lib" && \
    . ~/.bashrc

# create user with a home directory
ENV USER ${NB_USER}
ENV HOME /root
#/home/${NB_USER}
ENV PATH $HOME/openssl/bin:$HOME/.localpython/bin:$PATH
ENV LD_LIBRARY_PATH $HOME/openssl/lib 
ENV LDFLAGS "-L /root/openssl/lib -Wl,-rpath,/root/openssl/lib"

RUN groupadd --gid ${NB_UID} ${NB_USER}
RUN useradd --uid ${NB_UID}  --gid ${NB_UID} ${NB_USER}
#USER ${NB_USER}
COPY requirements/dev.txt requirements-dev.txt
COPY requirements/base.txt requirements-base.txt
COPY prepline_document_layout prepline_document_layout
COPY pipeline-notebooks pipeline-notebooks

RUN pip3.8 install --no-cache -r requirements-base.txt
RUN pip3.8 install --no-cache -r requirements-dev.txt 
RUN pip3.8 install ninja

RUN pip install "detectron2@git+https://github.com/facebookresearch/detectron2.git@78d5b4f335005091fe0364ce4775d711ec93566e"
EXPOSE 8000
CMD [ "uvicorn","prepline_document_layout.api.app:app" ]
