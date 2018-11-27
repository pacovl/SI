#!/bin/sh
dropdb -U alumnodb -h localhost si1
createdb -U alumnodb -h localhost si1
gunzip -c dump_v1.2.sql.gz | psql -U alumnodb -h localhost si1
psql -h localhost -U alumnodb -d si1 -a -f actualizar.sql
psql -h localhost -U alumnodb -d si1 -a -f setPrice.sql
psql -h localhost -U alumnodb -d si1 -a -f setOrderAmount.sql
psql -h localhost -U alumnodb -d si1 -a -f setOrderAmountArg.sql
psql -h localhost -U alumnodb -d si1 -a -f getTopVentas.sql
psql -h localhost -U alumnodb -d si1 -a -f getTopMonths.sql
psql -h localhost -U alumnodb -d si1 -a -f updOrders.sql
