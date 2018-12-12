FROM ubuntu:16.04
ADD . /app
RUN apt-get update
RUN apt-get install -y python2.7 libmysqlclient-dev python-pip  
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r /app/requirements.txt
EXPOSE 8000
USER nobody
WORKDIR /app
CMD ./manage.py runserver
