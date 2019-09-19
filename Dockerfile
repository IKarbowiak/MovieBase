FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for project in the container
RUN mkdir /movies_service

WORKDIR /movies_service
ADD . /movies_service/
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT"
