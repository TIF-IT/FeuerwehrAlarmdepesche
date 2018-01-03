FROM python:3

ENV DB_PASSWORD ChangeMe

WORKDIR /usr/FeuerwehrAlarmdepesche

COPY ./dockerInternalStart.sh start.sh
RUN mkdir -p app/modules
COPY python/main.py app/
COPY python/core.py app/
COPY python/registry.py app/
COPY python/modules/email_module.py app/modules
COPY python/modules/html_module.py app/modules
COPY python/alarmdepescheconfig.py app/
COPY python/requirements.txt app/
COPY vorlagen/Steinbachhallenberg.html app/
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libmysqlclient-dev screen && \
    pip install --no-cache-dir -U -r app/requirements.txt
RUN export DEBIAN_FRONTEND=noninteractive ; \
    apt-get install -y mysql-server

COPY dbinit.sql .

# Dev
RUN apt-get install -y vim

RUN chmod +x /usr/FeuerwehrAlarmdepesche/start.sh
ENTRYPOINT [ "/usr/FeuerwehrAlarmdepesche/start.sh" ]
