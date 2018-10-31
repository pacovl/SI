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


def create_app(test_config=None):

    CUR_DIR = os.getcwd()
    print(CUR_DIR)
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config.from_mapping(
        #SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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
    with open('catalogo.json') as f:
        catalogo = json.load(f)
        categorias = ["--"]
        for peli in catalogo["peliculas"]:
            for cat in peli["etiquetas"]:
                if(cat and (cat not in categorias)):
                    categorias.append(cat)

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

    # Devuleve el importe total correspondiente a los items del carrito y un diccionario
    # con las peliculas compradas con sus respectivas cantidades
    def procesar_carro():
        ids = session['carro']

        total = 0
        pelis_dict = {}

        for peli_id in ids:
            peli = getPeliculaById(peli_id)

            if peli_id in pelis_dict:
                pelis_dict[peli_id]["cant"] += 1
            else:
                pelis_dict[peli_id] = {"peli": peli, "cant": 1}

            total += peli['precio']

        return total, pelis_dict

    def vaciar_carro():
        session.pop('carro')

    # Devuelve un listado de objetos pelicula aleatoriamente obtenidos
    def recomendacion_aletoria(num_pelis=3, mantener=False):
        # if mantener:
        #     return global_recomendadas
        # else:
        longitud = len(catalogo['peliculas'])
        indices = sample(range(longitud), num_pelis)
        recomendadas = []
        for i in indices:
            recomendadas.append(catalogo['peliculas'][i])

        return recomendadas

    # Definimos index.html
    @app.route('/', methods=['POST', 'GET'])
    def index():

        # Identificamos solicitudes post tras busqueda
        if request.method == 'POST':
            type = request.form.keys()

            if "seleccion" in type:
                search = request.form['seleccion']

                lista_filtrada = []
                for pelicula in catalogo['peliculas']:
                    if search in pelicula["etiquetas"]:
                        lista_filtrada.append(pelicula)

                return render_template('index.html', seleccion=lista_filtrada, cats=categorias, user_id=getUserName())

            if "username" in type:
                # Recibimos los campos de registro
                nombre = request.form['username']
                if not(not nombre or nombre == ""):
                    password = hashlib.md5(
                        request.form['password'].encode('utf8')).hexdigest()

                    # Comprobamos si existe una carpeta con el mismo nombre
                    dir_name = CUR_DIR + '/usuarios/' + nombre
                    if (not os.path.isdir(dir_name)):
                        flash("No existe ese usuario")
                    else:

                        with open(dir_name + '/datos.json', 'r') as outfile:
                            datos_usuario = json.load(outfile)

                        if password != datos_usuario["password"]:
                            flash("Contrasenia incorrecta")
                            #return "Contrasenia incorrecta"
                            #return render_template('index.html', seleccion=catalogo["peliculas"], cats=categorias)
                        else:
                            session['user'] = datos_usuario["nombre"]
                            session.modified = True

                    # Pasamos la lista de peliculas para obtener los datos en seleccion
                    return render_template('index.html', seleccion=catalogo["peliculas"], cats=categorias, user_id=getUserName())
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

                # Creamos un dict con los campos de registro
                dict = {'nombre': nombre, 'password': password,
                        'email': email, 'card': card, 'sex': sex, 'saldo': saldo}
                dict_historial = {'compras': []}

                # Comprobamos si existe una carpeta con el mismo nombre
                dir_name = CUR_DIR + '/usuarios/' + nombre
                if (not os.path.isdir(dir_name)):
                    os.makedirs(dir_name)
                    # Escribimos un archivo json con el usuario
                    with open(dir_name + '/datos.json', 'w+') as outfile:
                        json.dump(dict, outfile)
                    with open(dir_name + '/historial.json', 'w+') as outfile_historial:
                        json.dump(dict_historial, outfile_historial)
                else:
                    return "El usuario ya existe"

                return render_template('index.html', seleccion=catalogo["peliculas"], cats=categorias, user_id=getUserName())

            if "buscar" in type:
                search = request.form['buscar']
                #pelis = catalogo["peliculas"].filter(lambda x: x["titulo"] == filmname)
                #category = request.form['categoria']
                # print(category)

                lista_filtrada = []
                for pelicula in catalogo['peliculas']:
                    if pelicula["titulo"].lower().find(search.lower()) != -1:
                        lista_filtrada.append(pelicula)

                return render_template('index.html', seleccion=lista_filtrada[:9], cats=categorias, user_id=getUserName())

        # Pasamos la lista de peliculas para obtener los datos en seleccion
        return render_template('index.html', seleccion=catalogo["peliculas"], cats=categorias, user_id=getUserName())


    @app.route('/detalle', methods=['POST', 'GET'])
    def detalle():
        if request.method == 'POST':
            type = request.form.keys()
            print(type)
            if "username" in type:

                #Recibimos los campos de registro
                nombre = request.form['username']
                password = hashlib.md5(request.form['password'].encode('utf8')).hexdigest()
                pelicula = request.form['peli']

                #Comprobamos si existe una carpeta con el mismo nombre
                dir_name = CUR_DIR + '/usuarios/' + nombre
                if (not os.path.isdir(dir_name)):
                    flash("No existe ese usuario")
                else:
                    with open(dir_name + '/datos.json', 'r') as outfile:
                        datos_usuario = json.load(outfile)

                    if password != datos_usuario["password"]:
                        flash("Contrasenia incorrecta")
                    else:
                        #Creamos la cookie de session
                        session['user'] = datos_usuario["nombre"]
                        session.modified = True

                for peli in catalogo["peliculas"]:
                    if peli['titulo'] == pelicula:
                        resp = make_response(render_template('detalle.html', seleccion = peli, recomendadas = recomendacion_aletoria(), cats = categorias, user_id=getUserName()))
                        return resp

        pelicula = request.args.get('pelicula')
        for peli in catalogo["peliculas"]:
            if peli['titulo'] == pelicula:
                return render_template('detalle.html', seleccion=peli, recomendadas=recomendacion_aletoria(), cats=categorias, user_id=getUserName())

        return "No se ha encontrado la pelicula"

    @app.route('/adicion', methods=['GET'])
    def adicion():
        id_peli = request.args.get('id')
        id_peli = int(id_peli)
        peli = getPeliculaById(id_peli)
        if session.get('carro'):
            session['carro'].append(id_peli)
            session.modified = True
        else:
            session['carro'] = []
            session['carro'].append(id_peli)

        return redirect(url_for('detalle', pelicula=peli["titulo"]))

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

                #Comprobamos si existe una carpeta con el mismo nombre
                dir_name = CUR_DIR + '/usuarios/' + nombre
                if (not os.path.isdir(dir_name)):
                    flash("No existe ese usuario")
                else:

                    with open(dir_name + '/datos.json', 'r') as outfile:
                        datos_usuario = json.load(outfile)

                    if password != datos_usuario["password"]:
                        flash("Contrasenia incorrecta")
                    else:
                        #Creamos la cookie de session
                        session['user'] = datos_usuario["nombre"]
                        session.modified = True

                #resp = make_response(render_template('carrito.html', seleccion = catalogo["peliculas"], cats = categorias, user_id = datos_usuario["nombre"]))

        if not session.get('carro'):
            return render_template('carrito.html', seleccion = None, user_id=getUserName())
        else:
            ids = session['carro']

            total = 0
            pelis_dict = {}

            for peli_id in ids:
                peli = getPeliculaById(peli_id)

                if peli_id in pelis_dict:
                    pelis_dict[peli_id]["cant"] += 1
                else:
                    pelis_dict[peli_id] = {"peli": peli, "cant": 1}

                total += peli['precio']

            return render_template('carrito.html', seleccion = pelis_dict, precio = total, user_id=getUserName())

    @app.route('/tramitar', methods=['GET'])
    def tramitar():
        if (session.get('user')):
            nombre = session['user']
            coste, dict_pelis = procesar_carro()
            dir_name = CUR_DIR + '/usuarios/' + nombre

            if (not os.path.isdir(dir_name)):
                flash("No existe ese usuario")
            else:
                # Comprobar si hay saldo
                with open(dir_name + '/datos.json') as f:
                    datos = json.load(f)

                saldo = datos['saldo']
                if saldo >= coste:
                    # Descontamos coste
                    datos['saldo'] = saldo - coste

                    with open(dir_name + '/datos.json', 'w+') as f_datos:
                        json.dump(datos, f_datos)

                    fecha = str(datetime.datetime.now())
                    dict_compra = {'fecha': fecha, 'coste': coste, 'peliculas': dict_pelis}

                    with open(dir_name + '/historial.json') as f_historial:
                        historial = json.load(f_historial)

                    # Anadimos la compra al historial
                    historial['compras'].append(dict_compra)

                    with open(dir_name + '/historial.json', 'w+') as outfile:
                        json.dump(historial, outfile)

                    flash("Has realizado tu compra exitosamente")

                    vaciar_carro()

                else:
                    flash("No tienes suficiente saldo")

        else:
            flash("Necesitas haber iniciado sesion para tramitar el pedido")
        return render_template("index.html", seleccion=catalogo["peliculas"], cats=categorias, user_id=getUserName())

    @app.route('/eliminar', methods=['GET'])
    def eliminar():
        id_peli = request.args.get('pelicula')
        id_peli = int(id_peli)
        if session.get('carro'):
            session['carro'].remove(id_peli)
            session.modified = True
        return redirect("/carrito")

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.pop('user', None)
        return redirect("/")

    @app.route('/visitas', methods=['GET', 'POST'])
    def visitas():
        x = randint(0, 10000)
        rv = make_response(
            Response(str(x), headers={'Content-Type': 'text/html'}),
            200)
        return rv

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
