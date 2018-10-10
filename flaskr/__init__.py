import os

import json
import functools
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
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

    #Aqui obtenemos el catalogo
    with open('flaskr/catalogo.json') as f:
        catalogo = json.load(f)

    #Definimos index.html
    @app.route('/')
    def index():

        #Pasamos la lista de peliculas para obtener los datos en seleccion
        return render_template('layout.html', seleccion = catalogo["peliculas"][:5])

    @app.route('/buscar/', methods=['POST'])
    def busqueda():
        search = request.form['buscar']

        #pelis = catalogo["peliculas"].filter(lambda x: x["titulo"] == filmname)

        lista_filtrada = []
        for pelicula in catalogo['peliculas']:
            if pelicula["titulo"].find(search) != -1:
                lista_filtrada.append(pelicula)

        if len(lista_filtrada) < 1:
            return render_template('layout.html', seleccion = catalogo["peliculas"][:5])
        else:
            return render_template('layout.html', seleccion = lista_filtrada[:5])

    @app.route('/detalle/', methods=['POST'])
    def detalle():

        try:
            if request.method == 'POST':
                peli = request.form['pelicula']

                return render_template('componentes/new_details.html', seleccion=peli)
        except:
            #En caso de no encontrar (no deberia pasar nunca)
            return url_for(index)
        return url_for(index)
                    

        
    # #Definimos index_logged.html
    # @app.route('/index_logged.html')
    # def index_logged():
    #     #Pasamos la lista de peliculas para obtener los datos en seleccion
    #     return render_template('index_logged.html',  seleccion=catalogo["peliculas"])
        
    # @app.route('/details_logged')
    # def details_logged(filmname):
    #     #Tratamos de encontrar la pelicula en la lista de peliculas
    #     pelis = catalogo["peliculas"].filter(lambda x: x["titulo"]== filmname)
    #     if pelis.len()<1:
    #         return render_template('index_logged.html', seleccion=catalogo["peliculas"])
    #     else:
    #         return render_template('details_logged.html', pelicula = pelis[0])
            
    # @app.route('/details_unlogged')
    # def details_unlogged(request):
    #     #Tratamos de encontrar la pelicula en la lista de peliculas
    #     pelis = catalogo["peliculas"].filter(lambda x: x["titulo"]== filmname)
    #     if pelis.len()<1:
    #         return render_template('index.html', seleccion=catalogo["peliculas"])
    #     else:
    #         return render_template('details_unlogged.html', pelicula = pelis[0])

    return app
        