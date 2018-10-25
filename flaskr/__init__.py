import os
import hashlib
import json
import functools
from flask import Flask, session
from flask_session import Session
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)
from random import randint


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


    def getPeliculaById(id_peli):
        for peli in catalogo['peliculas']:
            if peli['id'] == id_peli:
                return peli
        return None 
        #'{"id": 0, "titulo": "Avatar","poster": "imgs/avatar.jpg","director": "James Cameron","precio": 10,"anno": 2009,"desc": "Un senor militar se vuelve azul y alucina con un mundo alienigena.","etiquetas": ["ciencia ficcion","espacio"],"actores": [{"nombre": "Zoe Saldana","personaje": "Neytiri"},{"nombre": "Sam Worthington","personaje": "Jake Sully"}]}'

    # Definimos index.html
    @app.route('/', methods=['POST', 'GET'])
    def index():

        #session['carro'] = []
        # Identificamos solicitudes post tras busqueda
        if request.method == 'POST':
            type = request.form.keys()

            if "seleccion" in type:
                search = request.form['seleccion']
                #pelis = catalogo["peliculas"].filter(lambda x: x["titulo"] == filmname)
                #category = request.form['categoria']
                # print(category)

                lista_filtrada = []
                for pelicula in catalogo['peliculas']:
                    if search in pelicula["etiquetas"]:
                        lista_filtrada.append(pelicula)

                indice = int(categorias.index(search))

                return render_template('index.html', seleccion=lista_filtrada[:9], cats=categorias)

            if "username" in type:

                # Recibimos los campos de registro
                nombre = request.form['username']
                password = hashlib.md5(
                    request.form['password'].encode('utf8')).hexdigest()

                # Comprobamos si existe una carpeta con el mismo nombre
                dir_name = CUR_DIR + '/usuarios/' + nombre
                if (not os.path.isdir(dir_name)):
                    return "No existe ese usuario"

                with open(dir_name + '/datos.json', 'r') as outfile:
                    datos_usuario = json.load(outfile)

                if password != datos_usuario["password"]:
                    return "Contrasenia incorrecta"

                # TODO Hacer el login
                print("LOGIN EXITOSOOOOOOOO")
                return render_template('index.html', seleccion=catalogo["peliculas"][:9], cats=categorias)
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

                # Comprobamos si existe una carpeta con el mismo nombre
                dir_name = CUR_DIR + '/usuarios/' + nombre
                if (not os.path.isdir(dir_name)):
                    os.makedirs(dir_name)
                    # Escribimos un archivo json con el usuario
                    with open(dir_name + '/datos.json', 'w+') as outfile:
                        json.dump(dict, outfile)
                else:
                    return "El usuario ya existe"

                return render_template('index.html', seleccion=catalogo["peliculas"][:9], cats=categorias)

            if "buscar" in type:
                search = request.form['buscar']
                #pelis = catalogo["peliculas"].filter(lambda x: x["titulo"] == filmname)
                #category = request.form['categoria']
                # print(category)

                lista_filtrada = []
                for pelicula in catalogo['peliculas']:
                    if pelicula["titulo"].lower().find(search.lower()) != -1:
                        lista_filtrada.append(pelicula)

                return render_template('index.html', seleccion=lista_filtrada[:9], cats=categorias)

        # Pasamos la lista de peliculas para obtener los datos en seleccion
        return render_template('index.html', seleccion=catalogo["peliculas"][:9], cats=categorias)

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
                    return "No existe ese usuario"

                with open(dir_name + '/datos.json', 'r') as outfile:
                    datos_usuario = json.load(outfile)

                if password != datos_usuario["password"]:
                    return "Contrasenia incorrecta"

                #Creamos la cookie de session
                session['user'] = datos_usuario["nombre"]
                session.modified = True


                for peli in catalogo["peliculas"]:
                    if peli['titulo'] == pelicula:
                        resp = make_response(render_template('detalle.html', seleccion = peli, recomendadas = catalogo["peliculas"][:9], cats = categorias, user_id = datos_usuario["nombre"]))
                        return resp
                return "No se ha encontrado pelicula"

        pelicula = request.args.get('pelicula')
        for peli in catalogo["peliculas"]:
            if peli['titulo'] == pelicula:
                return render_template('detalle.html', seleccion=peli, recomendadas=catalogo["peliculas"][:3], cats=categorias)

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

        print("========> anado al carrito: "+peli['titulo']+"("+str(id_peli)+") "+"["+str(len(session['carro']))+"]")
        for item in session['carro']:
            print(str(item))
        #print("========> anado al carrito: "+peli[indice]+"("+str(id_peli)+")")
        
        return render_template('detalle.html', seleccion=peli, recomendadas=catalogo["peliculas"][:3], cats=categorias)

        #return "No se ha encontrado la pelicula"

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
                    return "No existe ese usuario"

                with open(dir_name + '/datos.json', 'r') as outfile:
                    datos_usuario = json.load(outfile)

                if password != datos_usuario["password"]:
                    return "Contrasenia incorrecta"

                #Creamos la cookie de session
                session['user'] = datos_usuario["nombre"]
                session.modified = True

                resp = make_response(render_template('carrito.html', seleccion = catalogo["peliculas"][:9], cats = categorias, user_id = datos_usuario["nombre"]))
        
        if 'carro' not in session:
            return render_template('carrito.html', seleccion = None, user_id = session.get('user'))
        else:
            ids = session['carro']
            #pelis_carro = {}
            lista_pelis = []

            print("---SESION---")
            for item in ids:
                print("-"+str(item))

            total = 0
            for peli_id in ids:
                peli_id = int(peli_id)
                peli = getPeliculaById(peli_id)
                print("vamos a mostrar la peli: ===> "+peli['titulo'])
                if peli == None:
                    break
                total += peli['precio']

                lista_pelis.append(peli)
                #if peli_id in pelis_carro:
                    #pelis_carro[peli_id]['cant'] += 1
                #else:
                    #pelis_carro[peli_id] = {"cant":1, "titulo":peli['titulo'], "poster":peli['poster'], "desd":peli['desc'], "precio":peli['precio']}

            return render_template('carrito.html', seleccion = lista_pelis, user_id = session.get('user'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
