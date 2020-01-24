from tasks import app
from flask import render_template, request, redirect, url_for
from tasks.forms import TaskForm, ProccesTaskForm

import csv, sqlite3, os
from datetime import date

DATOS = './data/tareas.dat'
COPIA = './data/copia.txt'
BASE_DATOS = './data/task.db'

cabecera = ['title', 'description', 'date']

def openFiles(DATOS, COPIA):
        original = open(DATOS, 'r')
        copia = open(COPIA, 'w')
        return original, copia

def closeFiles(original, copia):
    original.close()
    copia.close()

def renameFiles(DATOS, COPIA):
    os.remove(DATOS)
    os.rename(COPIA, DATOS)
    
def todasTareasDB():
    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    consulta = 'SELECT  titulo, descripcion, fecha, id FROM tareas;'
    rows = cursor.execute(consulta)
    filas = []
    for row in rows:
        filas.append(row)
    
    print(filas)
    conn.close()
    return filas

def addTaskDB(title, description, fx):
    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    consulta = '''
        INSERT INTO tareas (titulo, descripcion, fecha)
                    VALUES (?, ?, ?);
    '''
    cursor.execute(consulta,(title, description, fx))
    conn.commit()
    conn.close()

def leeTaskDB(id):
    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    consulta = '''
        SELECT  titulo, descripcion, fecha, id FROM tareas
         WHERE id = ?;
    '''
    rows = cursor.execute(consulta, (id,))
    fila = rows.fetchone()
    
    conn.close()
    return fila

def borraTaskDB(id):
    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    consulta = '''
        DELETE FROM tareas
         WHERE id = ?;
    '''
    cursor.execute(consulta, (id,))
    conn.commit()
    conn.close()

def modTaskDB(id):
    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    consulta = """
        UPDATE tareas
           SET titulo = ?, descripcion = ?, fecha = ?
         WHERE id = ?;
    """
    cursor.execute(consulta, (request.values.get('title'), request.values.get('description'), request.values.get('fx'), id))
    conn.commit()
    conn.close()

def todasTareas():
    fdatos = open(DATOS, 'r')
    csvreader = csv.reader(fdatos, delimiter=",", quotechar='"')

    registros = []
    for linea in csvreader:
        registros.append(linea)

    fdatos.close()
    return registros

def addTask(title, desc, fx):
    fdatos = open(DATOS, 'a', newline='') # 'w' de escritura, 'a' de append
    csvwriter = csv.writer(fdatos, delimiter=",", quotechar='"')        
    csvwriter.writerow([title, desc, fx])
    fdatos.close()

def leeTask(ix):
    fdatos = open(DATOS, 'r')
    csvreader = csv.reader(fdatos, delimiter=",", quotechar='"')

    registroAct = None

    ix = int(ix)
    for ilinea, linea in enumerate (csvreader, start=1):
        if ilinea == ix:
            registroAct = linea
            break

    return registroAct

def borraTask(ix):
    return modTask(ix, True)


def modTask(ix, borra=False):
    original, copia = openFiles(DATOS, COPIA)
    csvreader = csv.reader(original, delimiter=",", quotechar='"')
    for ilinea, linea in enumerate(csvreader, start=1):
        csvwriter = csv.writer(copia, delimiter=",", quotechar='"', lineterminator='\r')           
 
        if ilinea == ix:
            if not borra:
                title = request.values.get('title')
                desc = request.values.get('description')
                fx = request.values.get('fx')
                csvwriter.writerow([title, desc, fx])
        else:
            title = linea[0]
            desc = linea[1]
            fx = linea[2]
            csvwriter.writerow([title, desc, fx])
    closeFiles(original, copia)
    renameFiles(DATOS, COPIA)

@app.route("/")
def index():
    registros = todasTareasDB()
    return render_template("index.html", registros=registros)

@app.route("/newtask", methods=['GET', 'POST']) #son los metodos que vamos a aceptar, nuestra ruta va a poder ser get o post
def newTask():
    form = TaskForm(request.form)

    if request.method =='GET': #request es una instancia de repeticion que nos pide el servidor
        return render_template("task.html", form=form) #render_template es para plantillas
    
    if form.validate():
        title = request.values.get('title')
        desc = request.values.get('description')
        fx = request.values.get('fx')

        addTaskDB(title, desc, fx)

        return redirect(url_for("index")) #esto redirige a index
    else:
        return render_template("task.html", form=form)#return render_template("task.html") #una vez hecho todo el if, al darle a enviar, creará una carpeta en "data"


@app.route("/processtask", methods=['GET', 'POST'])
def proccesTask():
    form = ProccesTaskForm(request.form)

    if request.method == 'GET':
        ix = request.values.get('ix')
        if ix:
            registroAct = leeTaskDB(ix)

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
                    

                form = ProccesTaskForm(data={'ix': ix, 'title': registroAct[0], 'description': registroAct[1], 'fx': fechaTarea, 'btn': accion})

            return render_template("processtask.html", form=form)
        else:
            return redirect(url_for("index"))

    if form.btn.data == 'B':
        ix = int(request.values.get('ix'))
        borraTaskDB(ix)

        return redirect(url_for('index'))
        
    if form.btn.data == 'M':
        if form.validate():     
            ix = int(request.values.get('ix'))      
            modTaskDB(ix)          
            return redirect(url_for("index"))
        return render_template("processtask.html", form=form)

    