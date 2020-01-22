from tasks import app
from flask import render_template, request

import csv


@app.route("/") #son los metodos que vamos a aceptar, nuestra ruta va a poder ser get o post
def index():
    <lee tareas en ficherzo .data/tareas.dat>
        return render_template("index.html") #render_template es para plantillas
    
@app.route("/newtask" methods=['GET', 'POST'])
def newtask():
    if request.method == 'GET':
        return render_template('task.html')


    fdatos = open('./data/tareas.dat', 'w') # 'w' de escritura
    csvwriter = csv.writer(fdatos, delimiter=",", quotechar='"')

    title = request.values.get('title')
    desc = request.values.get('desc')
    date = request.values.get('date')

    csvwriter.writerow([title, desc, date])

    fdatos.close()
    return redirect(url_for("index")) #una vez hecho todo el if, al darle a enviar, creará una carpeta en "data"
