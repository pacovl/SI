#!/bin/sh
dropdb -U alumnodb -h localhost si1_p4
createdb -U alumnodb -h localhost si1_p4
gunzip -c dump_v1.0-P4.sql.gz | psql -U alumnodb -h localhost si1_p4
