from tasks import app
from flask import render_template, request, redirect, url_for
from tasks.forms import TaskForm, ProccesTaskForm

import csv
from datetime import date

DATOS = './data/tareas.dat'
COPIA = './data/copia.txt'
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
    form = TaskForm(request.form)

    if request.method =='GET': #request es una instancia de repeticion que nos pide el servidor
        return render_template("task.html", form=form) #render_template es para plantillas
    
    if form.validate():
        fdatos = open(DATOS, 'a', newline='') # 'w' de escritura, 'a' de append
        csvwriter = csv.writer(fdatos, delimiter=",", quotechar='"')

        title = request.values.get('title')
        desc = request.values.get('description')
        date = request.values.get('date')

        csvwriter.writerow([title, desc, date])

        fdatos.close()
        return redirect(url_for("index")) #esto redirige a index
        #return render_template("task.html") #una vez hecho todo el if, al darle a enviar, creará una carpeta en "data"
    else:
        return render_template("task.html", form=form)

@app.route("/processtask", methods=['GET', 'POST'])
def proccesTask():
    form = ProccesTaskForm(request.form)

    if request.method == 'GET':
        '''
         ix = 2
         btnModificar
        '''
        fdatos = open(DATOS, 'r')
        csvreader = csv.reader(fdatos, delimiter=",", quotechar='"')

        registroAct = None
        ilinea = 1
        ix = int(request.values.get('ix'))
        for linea in csvreader:
            if ilinea == ix:
                registroAct = linea
                break
            ilinea += 1

        if registroAct:
            if registroAct[2]:
                fechaTarea = date(int(registroAct[2][:4]), int(registroAct[2][5:7]), int(registroAct[2][8:]))
            else:
                fechaTarea = None
            
            accion = ''

            if 'btnModificar' in request.values:            
                accion = 'M'
            
            if 'btnBorrar' in request.values:
                accion = 'B'
                

            form = ProccesTaskForm(data={'ix': ix, 'title': registroAct[0], 'description': registroAct[1], 'date': fechaTarea, 'btn': accion})

        return render_template("processtask.html", form=form)


    if form.btn.data == 'B':
        print('borrar Registro')
        return redirect(url_for('index'))

    if form.btn.data == 'M':
        if form.validate():
            print("Modificar el fichero")
            '''
            crear fichero copia vacio en escritura
            leer y copiar todos los refistros desde tareas.txt a copia.txt hasta el anterior al que vamos a modificar
            grabar el nuevo registro con los datos del formulario
            leer y copiar el resto de los registros hasta el final
            cerrar los dos ficheros
            borrar tareas.txt
            renombrar copia.txt a tareas.txt
            '''
            return redirect(url_for('index'))
        
        return render_template("processtask.html", form=form)