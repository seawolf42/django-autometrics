FROM quay.io/travisci/travis-python

WORKDIR /root
RUN git clone https://github.com/seawolf42/django-autometrics.git
WORKDIR /root/django-autometrics
RUN git checkout fix/test-command

RUN mkdir -p /root/virtualenv
RUN virtualenv /root/virtualenv/python2.7

RUN /bin/bash -c "source .env/bin/activate && pip install . && pip install flake8"

WORKDIR /root
RUN apt-get -qq install -y wget
RUN wget -O google-cloud-sdk.tgz https://storage.googleapis.com/cloud-sdk-release/google-cloud-sdk-137.0.1-linux-x86_64.tar.gz && tar -zxpvf google-cloud-sdk.tgz && rm google-cloud-sdk.tgz
RUN google-cloud-sdk/install.sh --usage-reporting=true --path-update=true --bash-completion=true --rc-path=/.bashrc --additional-components app-engine-python
ENV PATH /root/google-cloud-sdk/bin:$PATH

WORKDIR /root/django-autometrics
