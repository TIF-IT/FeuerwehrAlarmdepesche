FROM python:3

WORKDIR /usr/FeuerwehrAlarmdepesche

COPY ./start.sh .
RUN mkdir app
COPY python/alarmdepescheconfig.py app/
COPY python/parseAlarmMail.py app/
COPY python/requirements.txt app/
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libmysqlclient-dev && \
    pip install --no-cache-dir -U -r app/requirements.txt
#RUN pip install --upgrade pip && \
#    pip install imaplib3 && \
#    pip install beautifulsoup4 && \
#    pip install HTMLParser && \
#    pip install bs4 && \
#    pip install lxml && \
#    pip install flask && \
#    pip install flask-cors && \
#    pip install MySQL-python

#COPY python/parseAlarmMail.py .

#CMD [ "sh", "/usr/FeuerwehrAlarmdepesche/start.sh" ]
CMD [ "sh", "/usr/FeuerwehrAlarmdepesche/app/parseAlarmMail.py" ]
