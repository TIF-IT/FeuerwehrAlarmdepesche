FROM python:3

ENV DB_PASSWORD ChangeMe

WORKDIR /usr/FeuerwehrAlarmdepesche

COPY ./dockerInternalStart.sh start.sh
COPY Alarmdepesche /usr/FeuerwehrAlarmdepesche/Alarmdepesche
#COPY vorlagen/Steinbachhallenberg.html /usr/FeuerwehrAlarmdepesche/
COPY html/ /var/www/html/
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libmysqlclient-dev screen && \
    pip install -U -r /usr/FeuerwehrAlarmdepesche/Alarmdepesche/requirements.txt

RUN export DEBIAN_FRONTEND=noninteractive ; \
    apt-get install -y mysql-server apache2

# Dev
RUN apt-get install -y vim

#COPY ./dockerInternalStart.sh start.sh
#COPY Alarmdepesche/ Alarmdepesche/
#COPY Alarmdepesche/alarmdepescheconfig.py Alarmdepesche/
#COPY vorlagen vorlagen

COPY dbinit.sql .

RUN chmod +x /usr/FeuerwehrAlarmdepesche/start.sh
#ENTRYPOINT [ "/usr/FeuerwehrAlarmdepesche/start.sh" ]
CMD /usr/FeuerwehrAlarmdepesche/start.sh
