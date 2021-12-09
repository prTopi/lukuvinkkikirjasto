FROM postgres:latest
COPY ./database_structure.sql /docker-entrypoint-initdb.d/02-database_structure.sql
CMD ["docker-entrypoint.sh", "postgres"]