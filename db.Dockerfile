FROM postgres:latest
COPY ./database_structure.sql /docker-entrypoint-initdb.d/database_structure.sql
RUN chmod -R 755 /docker-entrypoint-initdb.d/database_structure.sql
CMD ["docker-entrypoint.sh", "postgres"]