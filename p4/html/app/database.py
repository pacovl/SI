# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine, text

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1_p4", echo=False, execution_options={"autocommit":False})

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare, break0, niter):
    
    # Array con resultados de la consulta para cada umbral
    dbr=[]

    if (use_prepare):
        # sentencia prepare
        stmt = """
        prepare listaClientes (numeric, int, int) as
        select count(*) as cc from (
            select distinct c.customerid
            from customers as c, orders as o
            where c.customerid = o.customerid and o.totalamount > $1 
                and DATE_PART('year', O.orderdate) = $2 and DATE_PART('month', O.orderdate) = $3
        ) as clients;
        """
        db_res = text(stmt)
        res = db_conn.execute(db_res)

    for ii in range(niter):
        
        if (use_prepare):
            # ejecucion sentencia preparada
            consulta = """
                execute listaClientes("""+ str(iumbral) +""", """+ str(anio) +""", """+ str(mes) +""");
            """
        else:
            # ejecucion consulta directamente
            consulta = """
                select count(*) as cc from (
                    select distinct c.customerid
                    from customers as c, orders as o
                    where c.customerid = o.customerid and o.totalamount > """+ str(iumbral) +""" 
                        and DATE_PART('year', O.orderdate) = """+ str(anio) +""" and DATE_PART('month', O.orderdate) = """+ str(mes) +"""
                ) as clients;
            """

        res = db_conn.execute(consulta)
        for resultado in res:
            # Detencion si no hay mas clientes
            if break0 and resultado[0] == 0:
                niter = 0
                break
            dbr.append({"umbral":iumbral,"contador":resultado[0]})

        # Detencion por numero de entradas o no mas clientes
        if niter == 0:
            break
        niter = niter + 1

        # Actualizacion de umbral
        iumbral = iumbral + iintervalo
    
    if (use_prepare):
        stmt = """deallocate listaClientes;"""
        db_conn.execute(stmt)
                
    return dbr

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)
        
    resultproxy.close()  
    
    db_conn.close()  
    
    return a
    
def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()
    
    db_conn.close()  

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}
    
def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):
    
    # Array de trazas a mostrar en la página
    dbr=[]

    # TODO: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()
    
    try:
        # TODO: ejecutar consultas
        pass

    except Exception as e:
        # TODO: deshacer en caso de error
        pass

    else:
        # TODO: confirmar cambios si todo va bien
        pass

        
    return dbr

