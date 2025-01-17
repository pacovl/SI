import os
import hashlib
import json
import functools
from flask import Flask, session, Response
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, current_app
)
from random import randint, sample
import datetime
import database

CUR_DIR = os.getcwd()
# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config.from_mapping(
    #SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
test_config = None
if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Aqui obtenemos el catalogo y las categorias
catalogo = {
    'peliculas': database.db_getMovieInfo()
}

def get_top_ventas():
    top10_raw = database.db_getTopVentas(2016)
    pelis = []
    for item in top10_raw:
        peli = database.db_getMovieInfoByName(item[1])[0]
        pelis.append(peli)
    return pelis

topVentas = get_top_ventas()
# Obtencion de los distintos generos
categorias = []
categorias_listado = database.db_getCategories()
categorias_listado = ["---"] + categorias_listado
for item in categorias_listado:
    categorias.append(item[0])

def getRandomText(init=0, end=200):
        # getParragraph returns a parragraph, useful for testing
        if end > 250:
            end = 250
        if init < 0:
            init = 0
        return """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
deserunt mollit anim id est laborum."""[init:end]

# Obtencion de un objeto pelicula a partir de su id
def getPeliculaById(id_peli):
    for peli in catalogo['peliculas']:
        if peli['id'] == id_peli:
            return peli
    return None

# Devuelve el nombre del usuario actual, none si no existe
def getUserName():
    if session.get("user"):
        return session['user']
    return None

def vaciar_carro():
    #session.pop('carro')
    database.delete_null_order()

# Devuelve un listado de objetos pelicula aleatoriamente obtenidos
def recomendacion_aletoria(num_pelis=3):
    peliculas = catalogo['peliculas']
    longitud = len(peliculas)
    indices = sample(range(longitud), num_pelis)
    recomendadas = []
    for i in indices:
        dict_movie = {
            'titulo': peliculas[i]['titulo'],
            'desc': getRandomText(),
            'id': peliculas[i]['id']
        }
        recomendadas.append(dict_movie)

    return recomendadas

# Definimos index.html
@app.route('/', methods=['POST', 'GET'])
def index():

    # Identificamos solicitudes post tras busqueda
    if request.method == 'POST':
        type = request.form.keys()

        if "seleccion" in type:
            search = request.form['seleccion']

            lista_filtrada = database.db_getMoviesWithGenre(search)

            return render_template('index.html', seleccion=lista_filtrada, cats=categorias, user_id=getUserName())

        if "username" in type:
            # Recibimos los campos de registro
            nombre = request.form['username']
            if not(not nombre or nombre == ""):
                password = hashlib.md5(
                    request.form['password'].encode('utf8')).hexdigest()

                #Comprobamos si existe usuario
                retorno = database.db_check_username(nombre)

                if retorno[0][0] == 0:
                    flash("El usuario no existe en la base de datos")
                else:
                    #Comprobamos la password
                    pass_md5 = database.db_username_get_password(nombre)[0][0]

                    if password != pass_md5:
                        flash("Contrasenia incorrecta")
                    else:
                        session['user'] = nombre
                        session.modified = True

                # Pasamos la lista de peliculas para obtener los datos en seleccion
                return render_template('index.html', seleccion=catalogo["peliculas"], top=topVentas, cats=categorias, user_id=getUserName())
            #return render_template('index.html', seleccion=catalogo["peliculas"], cats=categorias)

        if "fnombre" in type:
            # Recibimos los campos de registro
            nombre = request.form['fnombre']
            password = hashlib.md5(
                request.form['fpass'].encode('utf8')).hexdigest()
            email = request.form['femail']
            card = request.form['fcard']
            sex = request.form['fsex']
            saldo = randint(0, 100)

            #Ver si usuario esta insertado
            retorno = database.db_check_username(nombre)
            #Insertamos el usuario si no esta insertado
            if retorno[0][0] == 0:
                database.db_insert_user(nombre, password, email, card, sex, saldo)

            return render_template('index.html', seleccion=catalogo["peliculas"], top=topVentas, cats=categorias, user_id=getUserName())

        if "buscar" in type:
            search = request.form['buscar']
            #pelis = catalogo["peliculas"].filter(lambda x: x["titulo"] == filmname)
            #category = request.form['categoria']
            # print(category)

            #lista_filtrada = []
            #for pelicula in catalogo['peliculas']:
            #    if pelicula["titulo"].lower().find(search.lower()) != -1:
            #        lista_filtrada.append(pelicula)

            lista_filtrada = database.db_getFilteredMovies(search)

            return render_template('index.html', seleccion=lista_filtrada, cats=categorias, user_id=getUserName())

    # Pasamos la lista de peliculas para obtener los datos en seleccion
    return render_template('index.html', seleccion=catalogo["peliculas"], top=topVentas, cats=categorias, user_id=getUserName())


@app.route('/detalle', methods=['POST', 'GET'])
def detalle():

    if request.method == 'POST':
        type = request.form.keys()
        if "username" in type:

            #Recibimos los campos de registro
            nombre = request.form['username']
            password = hashlib.md5(request.form['password'].encode('utf8')).hexdigest()
            pelicula = request.form['peli']

            #Comprobamos si existe usuario
            retorno = database.db_check_username(nombre)

            if retorno[0][0] == 0:
                flash("El usuario no existe en la base de datos")
            else:
                #Comprobamos la password
                pass_md5 = database.db_username_get_password(nombre)[0][0]

                if password != pass_md5:
                    flash("Contrasenia incorrecta")
                else:
                    session['user'] = nombre
                    session.modified = True
                    
        movies = database.db_getMovieById(pelicula)
        movie = movies[0]
        movie_dict = {
            'titulo': movie['titulo'],
            'anno': movie['anno'],
            'precio': movie['precio'],
            'id': movie['id'],
            'desc': getRandomText(),
            'genero': movie['genero']
        }

        resp = make_response(render_template('detalle.html', seleccion = movie_dict, recomendadas = recomendacion_aletoria(), cats = categorias, user_id=getUserName()))
        return resp

    pelicula = request.args.get('pelicula')

    movies = database.db_getMovieById(pelicula)
    movie = movies[0]
    movie_dict = {
        'titulo': movie['titulo'],
        'anno': movie['anno'],
        'precio': movie['precio'],
        'id': movie['id'],
        'desc': getRandomText(),
        'genero': movie['genero']
    }

    return render_template('detalle.html', seleccion=movie_dict, recomendadas=recomendacion_aletoria(), cats=categorias, user_id=getUserName())

    return "No se ha encontrado la pelicula"

@app.route('/adicion', methods=['GET'])
def adicion():
    id_peli = request.args.get('id')
    id_peli = int(id_peli)
    peli = database.db_getMovieById(id_peli)
    peli_ = peli[0]

    nombre = getUserName()

    if nombre == None: # Sesion no iniciada
        if session.get('carro'):
            session['carro'].append(id_peli)
            session.modified = True
        else:
            session['carro'] = []
            session['carro'].append(id_peli)
    else: # Sesion iniciada
        num_ = database.db_getNumOrdersNull()
        num = num_[0][0]
        #print('# nulls:')
        #print(num)

        if num == 0: # Primera adicion
            customerid = database.db_getUserIdByUsername(nombre)
            customer_id = customerid[0]

            order_id = database.db_anadirCarrito(id_peli, customer_id[0])
        else: # El resto
            order_id = database.db_getNullOrder()[0]
            #print('El pedido con status null es:')
            #print(order_id)
        ret = database.db_getProdIdFromMovieId(id_peli)
        prod_id = ret[0]
        prod_price = ret[1]
        #print('prod_id obtenido:')
        #print(order_id)
        #print(prod_id)
        #print(prod_price)
        database.db_insertOrderDetail(order_id, prod_id, prod_price)

    return redirect(url_for('detalle', pelicula=peli_['id']))

@app.route('/registro', methods=['POST', 'GET'])
def registro():
    return render_template('register.html')

@app.route('/carrito', methods=['POST', 'GET'])
def carrito():
    if request.method == 'POST':
        type = request.form.keys()
        if "username" in type:

            #Recibimos los campos de registro
            nombre = request.form['username']
            password = hashlib.md5(request.form['password'].encode('utf8')).hexdigest()

            #Comprobamos si existe usuario
            retorno = database.db_check_username(nombre)

            if retorno[0][0] == 0:
                flash("El usuario no existe en la base de datos")
            else:
                #Comprobamos la password
                pass_md5 = database.db_username_get_password(nombre)[0][0]

                if password != pass_md5:
                    flash("Contrasenia incorrecta")
                else:
                    session['user'] = nombre
                    session.modified = True

            #resp = make_response(render_template('carrito.html', seleccion = catalogo["peliculas"], cats = categorias, user_id = datos_usuario["nombre"]))

    nombre = getUserName()
    if nombre == None: # sin inicio de sesion
        if not session.get('carro'):
            return render_template('carrito.html', seleccion=None, user_id=nombre)
        else:
            ids = session['carro']

            total = 0
            pelis_dict = {}

            for peli_id in ids:
                peli = database.db_getMovieById(peli_id)[0]

                if peli_id in pelis_dict:
                    pelis_dict[peli_id]["cant"] += 1
                else:
                    pelis_dict[peli_id] = {"peli": peli, "cant": 1}

                total += peli['precio']

            return render_template('carrito.html', seleccion = pelis_dict, precio = total, user_id=nombre)

    else: # usuario logueado
        if database.db_getNumOrdersNull()[0][0] == 0:
            return render_template('carrito.html', seleccion=None, user_id=nombre)
        else:
            ids_ = database.db_getIdsCarrito()
            ids = []
            for item in ids_:
                #print('id, cant:')
                #print(item[0])
                #print(item[1])
                ids.append({'id':item[0], 'q':item[1]})

            total = 0
            pelis_dict = {}

            for peli_id in ids:
                peli = database.db_getMovieById(peli_id['id'])[0]
                #print('peli carrito: ---')
                #print(peli)
                #print(peli['anno'])
                #print(peli['precio'])

                pelis_dict[peli_id['id']] = {"peli": peli, "cant": peli_id['q']}

                total += peli['precio']*peli_id['q']

            total_imp = database.db_getTotal()[0][0]

            return render_template('carrito.html', seleccion = pelis_dict, precio = total, precio_imp = total_imp, user_id=nombre)


@app.route('/tramitar', methods=['GET'])
def tramitar():
    nombre = getUserName()
    if (nombre):
        #coste, dict_pelis = procesar_carro()
        coste = database.db_getCartTotalAmount()[0][0]
        
        # Comprobar si hay saldo
        saldo = database.db_get_balance(nombre)[0][0]
        if saldo >= coste:
            # Descontamos coste
            database.db_sustract_cost(nombre, coste)

            # Ponemos la compra como pagada
            database.db_set_paid_order()

            flash("Tu compra ha sido pagada existosamente")

        else:
            flash("No tienes suficiente saldo")

    else:
        flash("Necesitas haber iniciado sesion para tramitar el pedido")
    return render_template("index.html", seleccion=catalogo["peliculas"], cats=categorias, user_id=getUserName())

@app.route('/eliminar', methods=['GET'])
def eliminar():
    nombre = getUserName()
    id_peli = request.args.get('pelicula')
    id_peli = int(id_peli)
    if nombre == None:
        if session.get('carro'):
            session['carro'].remove(id_peli)
            session.modified = True
    else:
        database.db_removeMovie(id_peli)

    return redirect(url_for("carrito"))


@app.route('/aumentar_saldo', methods=['GET'])
def aumentar_saldo():
    database.db_addSaldo(getUserName())

    return redirect(url_for("historial"))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    vaciar_carro()
    return redirect(url_for("index"))

@app.route('/visitas', methods=['GET', 'POST'])
def visitas():
    x = randint(0, 10000)
    rv = make_response(
        Response(str(x), headers={'Content-Type': 'text/html'}),
        200)
    return rv

@app.route('/historial', methods=['GET', 'POST'])
def historial():
    nombre = getUserName()
    compras = []

    orders = database.db_getUserOrders(nombre)
    for item in orders:
        pelis = {}
        info_pelis = database.getInfoPelisFromOrder(item[0])

        for info_peli in info_pelis:
            pelis[info_peli['id']] = {
                'peli': info_peli,
                'cant': info_peli['cant']
            }
        compra = {
            'peliculas': pelis,
            'fecha': item[1],
            'coste': item[2],
            'status': item[3]
        }
        compras.append(compra)

    saldo = database.db_get_balance(nombre)[0][0]
    return(render_template('historico.html', saldo = saldo, compras = compras, user_id=nombre))

if __name__ == '__main__':
    app.run()
