FROM python:3

ENV DB_PASSWORD ChangeMe

WORKDIR /usr/FeuerwehrAlarmdepesche

COPY ./start.sh .
RUN mkdir app
COPY python/alarmdepescheconfig.py app/
COPY python/parseAlarmMail.py app/
COPY python/requirements.txt app/
COPY vorlagen/Steinbachhallenberg.html app/
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libmysqlclient-dev screen && \
    pip install --no-cache-dir -U -r app/requirements.txt 
RUN export DEBIAN_FRONTEND=noninteractive ; \
    apt-get install -y mysql-server
#RUN pip install --upgrade pip && \
#    pip install imaplib3 && \
#    pip install beautifulsoup4 && \
#    pip install HTMLParser && \
#    pip install bs4 && \
#    pip install lxml && \
#    pip install flask && \
#    pip install flask-cors && \
#    pip install MySQL-python

#RUN /usr/bin/mysqld_safe > /dev/null 2>&1 & 
COPY dbinit.sql .
#RUN mysqladmin -u root password $DB_PASSWORD && \
#RUN  sleep 6;  mysql -u root < dbinit.sql

# Dev
RUN apt-get install -y vim 

#COPY python/parseAlarmMail.py .

CMD [ "sh", "/usr/FeuerwehrAlarmdepesche/start.sh" ]
#CMD [ "sh", "/usr/FeuerwehrAlarmdepesche/app/parseAlarmMail.py" ]
