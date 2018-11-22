#!/bin/sh
dropdb -U alumnodb -h localhost si1
createdb -U alumnodb -h localhost si1
gunzip -c ../../../p3/dump_v1.2.sql.gz | psql -U alumnodb -h localhost si1
 psql -h localhost -U alumnodb -d si1 -a -f actualizar.sql 
