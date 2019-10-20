from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/minitienda.db'

db = SQLAlchemy(app)

class Articulos(db.Model):
	"""Artículos de nuestra tienda"""
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(100),nullable=False)
	precio = db.Column(db.String(255))
	iva = db.Column(db.String,default=21)
	descripcion = db.Column(db.String(255))
	image = db.Column(db.String(255))
	stock = db.Column(db.String(10))
    categoria = db.Column(db.String(20))

class Categorias(db.Model):
	"""Categorias"""
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(100),nullable=False)

@app.route('/')
@app.route('/articulos')
def home():
    categorias = Categorias.query.all()
    articulos = Articulos.query.all()
    return render_template('index.html', articulos = articulos, categorias = categorias)

@app.route('/categorias')
def categorias():
	categorias=Categorias.query.all()
	return render_template("categorias.html",categorias=categorias)

@app.route('/crear-categoria', methods=['POST'])
def crearCategoria():
    nuevaCategoria = Categorias(nombre=request.form['nombre'])
    db.session.add(nuevaCategoria)
    db.session.commit()
    return redirect(url_for('categorias'))

@app.route('/crear-articulo', methods=['POST'])
def crearArticulo():
    nuevoArticulo = Articulos(nombre=request.form['nombre'],
    precio=request.form['precio'],
    descripcion=request.form['descripcion'],
    image=request.form['image'],
    stock=request.form['stock'],
    categoriaId=request.form['categoriaId'])
    db.session.add(nuevoArticulo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/eliminarArticulo/<id>')
def eliminarArticulo(id):
    Articulos.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
