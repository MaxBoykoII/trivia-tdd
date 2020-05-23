FROM postgres:12-alpine

COPY ./trivia.psql trivia.psql

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d