FROM python:3

ENV DB_PASSWORD ChangeMe

WORKDIR /usr/FeuerwehrAlarmdepesche

COPY ./dockerInternalStart.sh start.sh
RUN mkdir -p python/modules
#COPY python/main.py python/
#COPY python/core.py python/
#COPY python/registry.py python/
#COPY python/modules/email_module.py python/modules
#COPY python/modules/html_module.py python/modules
#COPY python/alarmdepescheconfig.py python/
#COPY python/requirements.txt python/
COPY Alarmdepesche /
COPY vorlagen/Steinbachhallenberg.html /
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libmysqlclient-dev screen && \
    pip install --no-cache-dir -U -r python/requirements.txt
RUN export DEBIAN_FRONTEND=noninteractive ; \
    apt-get install -y mysql-server apache2

COPY dbinit.sql .

# Dev
RUN apt-get install -y vim

RUN chmod +x /usr/FeuerwehrAlarmdepesche/start.sh
ENTRYPOINT [ "/usr/FeuerwehrAlarmdepesche/start.sh" ]
