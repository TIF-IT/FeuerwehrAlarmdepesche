FROM python:3

ENV DB_PASSWORD ChangeMe

WORKDIR /usr/FeuerwehrAlarmdepesche

COPY ./dockerInternalStart.sh start.sh
RUN mkdir app
COPY python/alarmdepescheconfig.py app/
COPY python/parseAlarmMail.py app/
COPY python/restFullService.py app/
COPY python/requirements.txt app/
COPY vorlagen/Steinbachhallenberg.html app/
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libmysqlclient-dev screen && \
    pip install --no-cache-dir -U -r app/requirements.txt 
RUN export DEBIAN_FRONTEND=noninteractive ; \
    apt-get install -y mysql-server apache2

COPY dbinit.sql .

# Dev
RUN apt-get install -y vim 

CMD [ "sh", "/usr/FeuerwehrAlarmdepesche/start.sh" ]
