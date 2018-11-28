DROP TABLE IF EXISTS shipping_address CASCADE;
DROP TABLE IF EXISTS creditcard CASCADE;
DROP TABLE IF EXISTS client_creditcard;
DROP TABLE IF EXISTS orderedbyclient;

-- Creamos las tablas auxiliares
CREATE TABLE shipping_address AS
    SELECT customerid, address1, address2, city, state, zip, country, region
    FROM customers
    ORDER BY customerid;

CREATE TABLE creditcard AS
    SELECT creditcard, creditcardexpiration, creditcardtype
    FROM customers;

-- Añadimos constraints
ALTER TABLE creditcard
	ADD CONSTRAINT creditcard_pk PRIMARY KEY (creditcard);

ALTER TABLE shipping_address
	ADD CONSTRAINT shipping_address_customerid_pk PRIMARY KEY (customerid);

ALTER TABLE imdb_actormovies
	ADD CONSTRAINT actormovies_actorid_fk FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid),
	ADD CONSTRAINT actormovies_movieid_fk FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

-- Añadimos relaciones
CREATE TABLE client_creditcard AS
	SELECT customerid, creditcard
	FROM customers;

ALTER TABLE client_creditcard
	ADD CONSTRAINT client_creditcard_pk PRIMARY KEY (customerid, creditcard),
	ADD CONSTRAINT creditcard_customer_fk FOREIGN KEY (customerid) REFERENCES customers(customerid) ON DELETE CASCADE,
	ADD CONSTRAINT creditcard_addrid_fk FOREIGN KEY (creditcard) REFERENCES creditcard(creditcard);

CREATE TABLE orderedbyclient AS
    SELECT orderid, customerid
    FROM orders;

ALTER TABLE orderedbyclient
	ADD CONSTRAINT orderedbyclient_pk PRIMARY KEY (orderid, customerid),
	ADD CONSTRAINT orderedbyclient_orderid_fk FOREIGN KEY (orderid) REFERENCES orders(orderid),
	ADD CONSTRAINT orderedbyclient_customerid_fk FOREIGN KEY (customerid) REFERENCES customers(customerid) ON DELETE CASCADE;

-- Eliminamos las columnas que hemos cambiado

ALTER TABLE customers
    ADD COLUMN rownum int;

UPDATE customers
SET rownum = valor
FROM (SELECT username, COUNT(username) as valor
      FROM customers
      GROUP BY username) as aux
WHERE aux.username= customers.username;

DELETE FROM customers
WHERE customers.rownum > 1;

ALTER TABLE customers
    DROP COLUMN address1,
    DROP COLUMN address2,
    DROP COLUMN city,
    DROP COLUMN state,
    DROP COLUMN zip,
    DROP COLUMN country,
    DROP COLUMN region,
    DROP COLUMN creditcard,
    DROP COLUMN creditcardexpiration,
    DROP COLUMN creditcardtype,
    ADD CONSTRAINT unique_name UNIQUE(username);

ALTER TABLE orders
    DROP COLUMN customerid;
