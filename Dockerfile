# syntax=docker/dockerfile:experimental

FROM centos:7

# NOTE(crag): NB_USER ARG for mybinder.org compat:
#             https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html
ARG NB_USER=notebook-user
ARG NB_UID=1000
ARG PIP_VERSION
ARG PIPELINE_PACKAGE

RUN yum -y update
RUN yum -y install gcc openssl-devel bzip2-devel libffi-devel make git sqlite-devel mesa-libGL xz-devel perl wget poppler-utils zlib-devel
#RUN wget https://www.openssl.org/source/openssl-1.1.1g.tar.gz 
RUN wget https://www.python.org/ftp/python/3.8.16/Python-3.8.16.tgz
# RUN mkdir openssl-1.1.1g Python-3.8.16
RUN tar -xzf Python-3.8.16.tgz

#RUN cd openssl-1.1.1g && ./config --prefix=/root/openssl --openssldir=/root/openssl no-ssl2 && make -j 6 && make install
#RUN export PATH=/root/openssl/bin:$PATH && export LD_LIBRARY_PATH=/root/openssl/lib 
#RUN export LDFLAGS="-L /root/openssl/lib -Wl,-rpath,/root/openssl/lib" && . ~/.bash_profile && cd ..

RUN cd Python-3.8.16 && mkdir ~/.localpython && ./configure --enable-optimizations --prefix=/root/.localpython 
RUN cd Python-3.8.16 && make -j 6 altinstall
RUN /root/.localpython/bin/python3.8 -m pip install --upgrade pip
RUN export PATH=/root/.localpython/bin:$PATH && export LD_LIBRARY_PATH=/root/openssl/lib &&export LDFLAGS="-L /root/openssl/lib -Wl,-rpath,/root/openssl/lib" && . ~/.bashrc
# RUN curl -O https://www.python.org/ftp/python/3.8.15/Python-3.8.15.tgz && tar -xzf Python-3.8.15.tgz && \
#   cd Python-3.8.15/ && ./configure --enable-optimizations && make altinstall && \
#   cd .. && ln -s /usr/local/bin/python3.8 /usr/local/bin/python3
#&& rm -rf Python-3.8.15* && \

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
RUN yum -y install which
COPY requirements/dev.txt requirements-dev.txt
COPY requirements/base.txt requirements-base.txt
COPY prepline_document_layout prepline_document_layout
COPY exploration-notebooks exploration-notebooks
COPY pipeline-notebooks pipeline-notebooks
COPY sample-docs sample-docs
RUN echo ${PATH}
RUN echo $LD_LIBRARY_PATH
RUN echo ${LDFLAGS}
RUN echo which pip3.8
RUN pip3.8 install --no-cache -r requirements-base.txt 
RUN pip3.8 install --no-cache -r requirements-dev.txt 

# CMD [ "/bin/bash" ]
#WORKDIR ${HOME}
#ENV PYTHONPATH="${PYTHONPATH}:${HOME}"
#ENV PATH="/home/${NB_USER}/.local/bin:${PATH}"
#ENTRYPOINT [ "uvicorn","prepline_document_layout.api.app:app" ]
RUN pip3.8 install ninja
RUN yum -y install bzip2
RUN yum -y install centos-release-scl
RUN yum -y install devtoolset-7-gcc*
SHELL [ "/usr/bin/scl", "enable", "devtoolset-7"]
RUN pip install "detectron2@git+https://github.com/facebookresearch/detectron2.git@78d5b4f335005091fe0364ce4775d711ec93566e"
CMD [ "uvicorn","prepline_document_layout.api.app:app" ]
