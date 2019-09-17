# our base image
from ubuntu:18.04

# System setup
run apt-get update && apt-get install --no-install-recommends -y \
    python3 \
    python3-pip \
    git \
    wget \
    openssh-client \
    sqlite3 \
    sqlitebrowser \
    vim

# Project requirements
run pip3 install django
run pip3 install django-crispy-forms

# Env
env PYTHONUNBUFFERED 1

# Paths
arg PROJECT_DIR=/var/www
arg PROJECT_FULL=${PROJECT_DIR}/psiweb

# Getting project
workdir $PROJECT_DIR
run git clone https://Czukuruku@bitbucket.org/Czukuruku/psiweb.git

# Server
expose 8000
stopsignal SIGINT
entrypoint ["python3", "psiweb/manage.py"]

# run the aplication
cmd ["runserver", "0.0.0.0:8000"]

