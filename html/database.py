# -*- coding: utf-8 -*-

import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select, func
from random import randint

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# cargar tabla imdb_movies
db_table_movies = Table('imdb_movies', db_meta, autoload=True, autoload_with=db_engine)
db_table_customers = Table('customers', db_meta, autoload=True, autoload_with=db_engine)

def db_listOfMovies1949():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las peliculas del anno 1949
        db_movies_1949 = select([db_table_movies]).where("year = '1949'")
        db_result = db_conn.execute(db_movies_1949)
        #db_result = db_conn.execute("Select * from imdb_movies where year = '1949'")
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getUserName(name):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las peliculas del anno 1949
        #db_name = select([db_table_customers]).where("username = '" + name + "'")

        stmt = "select firstname, lastname, email, phone from customers where username = '" + name + "'" # consulta
        db_name = sqlalchemy.text(stmt)

        print('-')
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getMovieInfo():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        stmt = """select distinct on (movietitle) movietitle as titulo, M.movieid as id, year as anno, P.price as precio, G.genre as genero 
                from imdb_movies as M, products as P, imdb_moviegenres as G
                where P.movieid = M.movieid and P.movieid = G.movieid  
               """
        db_name = sqlalchemy.text(stmt)

        print('-')
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getMovieInfoByName(titulo):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        stmt = """select distinct on (movietitle) movietitle as titulo, M.movieid as id, year as anno, P.price as precio, G.genre as genero 
                from imdb_movies as M, products as P, imdb_moviegenres as G
                where P.movieid = M.movieid and P.movieid = G.movieid and movietitle = '""" + titulo + "'"
        db_name = sqlalchemy.text(stmt)

        print('-')
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getCategories():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        stmt = """select distinct genre from imdb_moviegenres; 
               """
        db_name = sqlalchemy.text(stmt)

        print('-')
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getMoviesWithGenre(genre):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        stmt = """select distinct on (movietitle) movietitle as titulo, M.movieid as id, year as anno, P.price as precio, G.genre as genero 
                from imdb_movies as M, products as P, imdb_moviegenres as G
                where P.movieid = M.movieid and P.movieid = G.movieid  and G.genre = """ + "'" + genre + "'"
        db_name = sqlalchemy.text(stmt)

        print('-')
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getMovieById(id_peli):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        stmt = """select distinct on (movietitle) movietitle as titulo, M.movieid as id, year as anno, P.price as precio, G.genre as genero 
                from imdb_movies as M, products as P, imdb_moviegenres as G
                where P.movieid = M.movieid and P.movieid = G.movieid and M.movieid = """ + str(id_peli)
        db_name = sqlalchemy.text(stmt)

        print('-')
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getFilteredMovies(search):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        stmt = """select distinct on (movietitle) movietitle as titulo, M.movieid as id, year as anno, P.price as precio, G.genre as genero 
                from imdb_movies as M, products as P, imdb_moviegenres as G
                where P.movieid = M.movieid and P.movieid = G.movieid and M.movietitle LIKE '%""" + search + "%'"
        db_name = sqlalchemy.text(stmt)

        print('-')
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getTopVentas(anno):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        stmt = """ select * from getTopVentas(""" + str(anno) + ")"
        db_name = sqlalchemy.text(stmt)

        print('-')
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_anadirCarrito(id, customer_id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtencion ultimo id
        stmt = """select max(orderid) as maximo from orders;
        """
        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)
        max_id = (list(db_result))[0]

        nextid = max_id[0]+1
        tax = randint(10, 20)

        # Creacion order correspondiente
        stmt = "insert into orders values (" + str(nextid) + ", current_date, 0, " + str(tax) + ", 0, null)"
        db_name = sqlalchemy.text(stmt)

        print('-') 
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)

        # creacion orderedbyclient correspondiente
        stmt = "insert into orderedbyclient values (" + str(nextid) + ", " + str(customer_id) + ")"
        db_name = sqlalchemy.text(stmt)

        print('-') 
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)

        db_conn.close()

        return nextid
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_insertOrderDetail(order_id, prod_id, prod_price):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        stmt = "select count(*) from orderdetail where orderid = " + str(order_id) + " and prod_id = " + str(prod_id)
        db_name = sqlalchemy.text(stmt)

        print('y aquiiiiiiiiiiiiiiiiiiiiii')
        print(stmt)

        db_result = db_conn.execute(db_name)

        print('aquiiiiiiiiiiiiiiiiiiiiii ya no')

        cont = list(db_result)[0][0]
        print('coincide con otro producto (0 no): ')
        print(cont)

        if (cont == 0): # no hay coincidencias
            stmt = "insert into orderdetail values (" + str(order_id) + ", " + str(prod_id) + ", " + str(prod_price) + ", 1)"
            db_name = sqlalchemy.text(stmt)
            print('-') 
            print('La consulta realizada es:')
            print(db_name)
            print('-')
            db_result = db_conn.execute(db_name)
        else: # hay coincidencias
            stmt = "update orderdetail set quantity = quantity + 1 where orderid = " + str(order_id) + " and prod_id = " + str(prod_id) 
            db_name = sqlalchemy.text(stmt)
            print('-') 
            print('La consulta realizada es:')
            print(db_name)
            print('-')
            db_result = db_conn.execute(db_name)

        db_conn.close()

        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getUserIdByUsername(customer_name):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtencion ultimo id
        stmt = "select customerid from customers where username = '" + customer_name + "'"
        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'


def db_getNumOrdersNull():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtencion ultimo id
        stmt = "select count(*) from orders where status is null"
        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

        
def db_getProdIdFromMovieId(id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtencion ultimo id
        stmt = "select prod_id, price from products where movieid = " + str(id)
        db_name = sqlalchemy.text(stmt)

        print('-') 
        print('La consulta realizada es:')
        print(db_name)
        print('-')

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return list(db_result)[0]
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

        
def db_getNullOrder():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtencion ultimo id
        stmt = "select orderid from orders where status is null"
        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return list(db_result)[0]
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_getIdsCarrito():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtencion ultimo id
        stmt = """select M.movieid as id 
                from imdb_movies as M, products as P, orderdetail as O, orders as Os
                where M.movieid = P.movieid and P.prod_id = O.prod_id and O.orderid = Os.orderid and Os.status is null
        """
        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)
        db_conn.close()

        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_insert_user(nombre, password, email, card, sex, saldo):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtenemos nuevo id
        stmt = """select max(customerid) as maximo from customers;
        """
        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)
        max_id = (list(db_result))[0][0]

        next_id = max_id+1
        # Insertamos en customer
        stmt = """ INSERT INTO customers
                       (customerid, username, password, email, gender)
                       VALUES (""" + str(next_id) + """, '""" + nombre + """', '""" + password + """', '""" + email + """', '""" + sex + """');
            """
        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)

        db_conn.close()

        #Insertamos en creditcard si no está insertada

        db_result = db_check_creditcard(card)

        db_conn = db_engine.connect()

        if db_result[0][0] == 0:
            stmt = """ INSERT INTO creditcard
                       (creditcard, balance)
                       VALUES ('""" + card + """', """ + str(saldo) + """);
            """
            db_name = sqlalchemy.text(stmt)

            db_result = db_conn.execute(db_name)
        

        #Insertamos en creditcard_client
        stmt = """ INSERT INTO client_creditcard
                       (creditcard, customerid)
                       VALUES ('""" + card + """', """ + str(next_id) + """);
            """
        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)

        db_conn.close()

        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_check_username(username):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        print("HEY HEY HEY")
        # Vemos si está en la BBDD
        stmt = """ SELECT COUNT(username)
                   FROM customers
                   WHERE username = '""" + username + """';"""

        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)

        db_conn.close()

        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_check_creditcard(username):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Vemos si está en la BBDD
        stmt = """ SELECT COUNT(creditcard)
                   FROM creditcard
                   WHERE username = '""" + creditcard + """';"""


        db_name = sqlalchemy.text(stmt)

        db_result = db_conn.execute(db_name)

        db_conn.close()

        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'