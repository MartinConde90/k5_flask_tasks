from tasks import app
from flask import render_template, request, redirect, url_for

import csv

DATOS = './data/tareas.dat'
cabecera = ['title', 'description', 'date']

@app.route("/")
def index():
    fdatos = open(DATOS, 'r')
    csvreader = csv.reader(fdatos, delimiter=",", quotechar='"')

    registros = []
    for linea in csvreader:
        registros.append(linea)


    fdatos.close()
    return render_template("index.html", registros=registros)

@app.route("/newtask", methods=['GET', 'POST']) #son los metodos que vamos a aceptar, nuestra ruta va a poder ser get o post
def newTask():
    if request.method =='GET':
        return render_template("task.html") #render_template es para plantillas
    
    fdatos = open(DATOS, 'a') # 'w' de escritura, 'a' de append
    csvwriter = csv.writer(fdatos, delimiter=",", quotechar='"')

    title = request.values.get('title')
    desc = request.values.get('desc')
    date = request.values.get('date')

    csvwriter.writerow([title, desc, date])

    fdatos.close()
    return redirect(url_for("index")) #esto redirige a index
    #return render_template("task.html") #una vez hecho todo el if, al darle a enviar, creará una carpeta en "data"



    print('method:', request.method)
    print('parametros:', request.values)


'''
    recuperar parametros
    abrir fichero
    añadir registros
    devolver respuesta todo correcto
    '''