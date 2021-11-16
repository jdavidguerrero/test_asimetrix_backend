FROM python:3.8.9
ENV DATABASE_URL="postgresql+psycopg2://tsdbadmin:dm4mztd0jv0uvjla@plo7lhif44.h6oblrgc5x.tsdb.cloud.timescale.com:35696/tsdb"
ENV APP_SETTINGS="config.DevelopmentConfig"
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
CMD python3 app.py