#简单测试程序，控制台
FROM python:latest
LABEL author="xuqinghan"
LABEL purpose = 'python-console'


ENV PYTHONIOENCODING=utf-8

#dont need apt update
#RUN apt update
RUN pip3 install setuptools

# Build folder
RUN mkdir -p /deploy/app
WORKDIR /deploy/app
#only copy requirements.txt.  othors will be mounted by -v
COPY app/requirements.txt /deploy/app/requirements.txt
RUN pip3 install -r /deploy/app/requirements.txt
CMD ["/bin/bash"]
