from flaskr import app, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import psycopg2
db = SQLAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://sa:12345678@localhost:5432/pacientes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gcgzggrqwzmdtk:d7905b404e3103371b5973915b1cd74c81281c195c3a0330ad91a6d1c3cd07a3@ec2-54-225-254-115.compute-1.amazonaws.com:5432/d6i1rgvh54mffe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Alumnos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(30))


# CREATE
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        c_nombre = request.form['nombre']
        c_apellido = request.form['apellido']
        alumno = Alumnos(nombre=c_nombre, apellido=c_apellido)
        db.session.add(alumno)
        db.session.commit()
        alumnos = call_pacientes()
        return render_template("nuevo.html", nombre=c_nombre, l_alumnos=alumnos)
    lista = ["Acerca", "Contacto", "Nosotros", "FAQ"]
    return render_template("about.html", lista=lista)


@app.route('/second/<nombre>')
def hola(nombre=None):
    return render_template("index.html", mensaje=nombre)


@app.route('/nuevo')
def nuevo():
    return render_template("nuevo.html")


# DELETE
@app.route('/eliminar/<id>')
def eliminar(id):
    Alumnos.query.filter(Alumnos.id == id).delete()
    db.session.commit()
    return redirect(url_for('listar'))


# UPDATE
@app.route('/modificar/<id>')
def modificar(id):
    alumno = Alumnos.query.filter(Alumnos.id == id).first()
    return render_template("editar.html", alumno=alumno)


@app.route('/actualizar', methods=['GET', 'POST'])
def actualizar():
    if request.method == "POST":
        qry = Alumnos.query.get(request.form['id'])
        qry.nombre = request.form['nombreE']
        qry.apellido = request.form['apellidoE']
        db.session.commit()
        return redirect(url_for('listar'))


# READ
@app.route('/listar')
def listar():
    alumnos = call_pacientes()
    return render_template("nuevo.html", l_alumnos=alumnos)


@app.route('/escolares')
def call_pacientes():
    connection = psycopg2.connect("postgres://gcgzggrqwzmdtk:d7905b404e3103371b5973915b1cd74c81281c195c3a0330ad91a6d1c3cd07a3@ec2-54-225-254-115.compute-1.amazonaws.com:5432/d6i1rgvh54mffe")
    cursor = connection.cursor()
    cursor.execute("SELECT * from alumnos;")
    record = cursor.fetchall()
    return record


@app.errorhandler(404)
def error(e):
    return 'Página no encontrada'
