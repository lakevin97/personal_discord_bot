FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_USER=discord_interface
ENV MYSQL_PASSWORD=supersecurepassword

WORKDIR /database

COPY init.sql /docker-entrypoint-initdb.d/