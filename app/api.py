from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/lalishop_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Crear modelo de datos
class Categoria(db.Model):
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))

    def __init__(self, nombre):
        self.nombre = nombre

class UsuarioAdmin(db.Model):
    idUsuarioAdmin = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    contrasenia = db.Column(db.String(50))

    def __init__(self, nombre, correo, contrasenia):
        self.nombre = nombre
        self.correo = correo
        self.contrasenia = contrasenia

class Usuario(db.Model):
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    contrasenia = db.Column(db.String(50))

    def __init__(self, nombre, correo, contrasenia):
        self.nombre = nombre
        self.correo = correo
        self.contrasenia = contrasenia

class Producto(db.Model):
    
    idProducto = db.Column(db.Integer, primary_key=True)
    idUsuarioAdmin = db.Column(db.Integer)
    idCategoria = db.Column(db.Integer)
    nombreProducto = db.Column(db.String(50))
    nombreCatrgoria = db.Column(db.String(50))
    url = db.Column(db.String(50))
    descripcion = db.Column(db.String(100))
    precio = db.Column(db.Float)
    cantidad = db.Column(db.Integer)

    def __init__(self, idUsuarioAdmin, idCategoria, nombreProducto, nombreCategoria, url, descripcion, cantidad, precio):
        self.idUsuarioAdmin = idUsuarioAdmin
        self.idCategoria = idCategoria
        self.nombreProducto = nombreProducto
        self.nombreCategoria = nombreCategoria
        self.url = url
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio = precio

class Ordenes(db.Model):

    idOrden = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer)
    idProducto = db.Column(db.Integer)
    nombreUsuario = db.Column(db.String(50))
    fechaOrden = db.Column(db.DateTime)
    numeroArticulos = db.Column(db.Integer)
    total = db.Column(db.Float)

    def __init__(self, idUsuario, idProducto, nombreUsuario, fechaOrden, numeroArticulos, total):
        self.idUsuario = idUsuario
        self.idProducto = idProducto
        self.nombreUsuario = nombreUsuario
        self.fechaOrden = fechaOrden
        self.numeroArticulos = numeroArticulos
        self.total = total

with app.app_context():
        db.init_app(app)
        db.create_all()

#Esquema de categoria    
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('idCategoria','nombre')

#Esquema de usuarioAdmin
class UsuarioAdminSchema(ma.Schema):
    class Meta:
        fields = ('idUsuarioAdmin','nombre','correo','contrasenia')

#Esquema de usuario
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('idUsuario','nombre','correo','contrasenia')

#Esquema de producto
class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('idProducto','idUsuarioAdmin','idCategoria','nombreProducto','nombreCategoria','url','descripcion','cantidad','precio')

#Esquema de ordenes
class OrdenesSchema(ma.Schema):
    class Meta:
        fields = ('idOrden','idUsuario','idProducto','nombreUsuario','fechaOrden','numeroArticulos','total')

#una sola respuesta
categoria_schema = CategoriaSchema()
usuarioAdmin_schema = UsuarioAdminSchema()
usuario_schema = UsuarioSchema()
producto_schema = ProductoSchema()
orden_schema = OrdenesSchema()

#varias respuestas
categorias_schema = CategoriaSchema(many=True)
usuarioAdmins_schema = UsuarioAdminSchema(many=True)
usuarios_schema = UsuarioSchema(many=True)
productos_schema = ProductoSchema(many=True)
ordenes_schema = OrdenesSchema(many=True)

# CATEGORIA
#GET
@app.route('/categoria',methods=['GET'])
def get_categorias():
    categorias = Categoria.query.all()
    result = categorias_schema.dump(categorias)
    return jsonify(result)

#GET por id de Categoria
@app.route('/categoria/<id>',methods=['GET'])
def get_categoria(id):
    categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(categoria)

#POST Categoria
@app.route('/categoria',methods=['POST'])
def add_categoria():
    nombre = request.json['nombre']
    new_categoria = Categoria(nombre)
    db.session.add(new_categoria)
    db.session.commit()

    return categoria_schema.jsonify(new_categoria)

#PUT Categoria
@app.route('/categoria/<id>',methods=['PUT'])
def update_categoria(id):
    categoria = Categoria.query.get(id)
    nombre = request.json['nombre']
    categoria.nombre = nombre
    db.session.commit()
    return categoria_schema.jsonify(categoria)

#DELETE Categoria
@app.route('/categoria/<id>',methods=['DELETE'])
def delete_categoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return categoria_schema.jsonify(categoria)

# USUARIO ADMIN
#GET
@app.route('/usuarioAdmin',methods=['GET'])
def get_usuarioAdmins():
    usuarioAdmins = UsuarioAdmin.query.all()
    result = usuarioAdmins_schema.dump(usuarioAdmins)
    return jsonify(result)

#GET por id de UsuarioAdmin
@app.route('/usuarioAdmin/<id>',methods=['GET'])
def get_usuarioAdmin(id):
    usuarioAdmin = UsuarioAdmin.query.get(id)
    return usuarioAdmin_schema.jsonify(usuarioAdmin)

#POST UsuarioAdmin
@app.route('/usuarioAdmin',methods=['POST'])
def add_usuarioAdmin():
    nombre = request.json['nombre']
    correo = request.json['correo']
    contrasenia = request.json['contrasenia']
    new_usuarioAdmin = UsuarioAdmin(nombre,correo,contrasenia)
    db.session.add(new_usuarioAdmin)
    db.session.commit()

    return usuarioAdmin_schema.jsonify(new_usuarioAdmin)

#PUT UsuarioAdmin
@app.route('/usuarioAdmin/<id>',methods=['PUT'])
def update_usuarioAdmin(id):
    usuarioAdmin = UsuarioAdmin.query.get(id)
    nombre = request.json['nombre']
    correo = request.json['correo']
    contrasenia = request.json['contrasenia']
    usuarioAdmin.nombre = nombre
    usuarioAdmin.correo = correo
    usuarioAdmin.contrasenia = contrasenia
    db.session.commit()
    return usuarioAdmin_schema.jsonify(usuarioAdmin)

#DELETE UsuarioAdmin
@app.route('/usuarioAdmin/<id>',methods=['DELETE'])
def delete_usuarioAdmin(id):
    usuarioAdmin = UsuarioAdmin.query.get(id)
    db.session.delete(usuarioAdmin)
    db.session.commit()
    return usuarioAdmin_schema.jsonify(usuarioAdmin)

# USUARIO
#GET
@app.route('/usuario',methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    result = usuarios_schema.dump(usuarios)
    return jsonify(result)

#GET por id de Usuario
@app.route('/usuario/<id>',methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    return usuario_schema.jsonify(usuario)

#POST Usuario
@app.route('/usuario',methods=['POST'])
def add_usuario():
    nombre = request.json['nombre']
    correo = request.json['correo']
    contrasenia = request.json['contrasenia']
    new_usuario = Usuario(nombre,correo,contrasenia)
    db.session.add(new_usuario)
    db.session.commit()

    return usuario_schema.jsonify(new_usuario)

#PUT Usuario
@app.route('/usuario/<id>',methods=['PUT'])
def update_usuario(id):
    usuario = Usuario.query.get(id)
    nombre = request.json['nombre']
    correo = request.json['correo']
    contrasenia = request.json['contrasenia']
    usuario.nombre = nombre
    usuario.correo = correo
    usuario.contrasenia = contrasenia
    db.session.commit()
    return usuario_schema.jsonify(usuario)

#DELETE Usuario
@app.route('/usuario/<id>',methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return usuario_schema.jsonify(usuario)

# PRODUCTO
#GET
@app.route('/producto',methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    result = productos_schema.dump(productos)
    return jsonify(result)

#GET por id de Producto
@app.route('/producto/<id>',methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    return producto_schema.jsonify(producto)

#POST Producto
@app.route('/producto',methods=['POST'])
def add_producto():
    idUsuarioAdmin = request.json['idUsuarioAdmin']
    idCategoria = request.json['idCategoria']
    nombreProducto = request.json['nombreProducto']
    nombreCategoria = request.json['nombreCategoria']
    url = request.json['url']
    descripcion = request.json['descripcion']
    cantidad = request.json['cantidad']
    precio = request.json['precio']
    new_producto = Producto(idUsuarioAdmin, idCategoria, nombreProducto, nombreCategoria, url, descripcion, cantidad, precio)
    db.session.add(new_producto)
    db.session.commit()

    return producto_schema.jsonify(new_producto)

#PUT Producto
@app.route('/producto/<id>',methods=['PUT'])
def update_producto(id):
    producto = Producto.query.get(id)
    idUsuarioAdmin = request.json['idUsuarioAdmin']
    idCategoria = request.json['idCategoria']
    nombreProducto = request.json['nombreProducto']
    nombreCategoria = request.json['nombreCategoria']
    url = request.json['url']
    descripcion = request.json['descripcion']
    cantidad = request.json['cantidad']
    precio = request.json['precio']
    producto.idUsuarioAdmin = idUsuarioAdmin
    producto.idCategoria = idCategoria
    producto.nombreProducto = nombreProducto
    producto.nombreCategoria = nombreCategoria
    producto.url = url
    producto.descripcion = descripcion
    producto.cantidad = cantidad
    producto.precio = precio

    db.session.commit()
    return producto_schema.jsonify(producto)

#DELETE Producto
@app.route('/producto/<id>',methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)

# Ordenes
#GET
@app.route('/ordenes',methods=['GET'])
def get_ordenes():
    ordenes = Ordenes.query.all()
    result = ordenes_schema.dump(ordenes)
    return jsonify(result)

#GET por id de Ordenes
@app.route('/ordenes/<id>',methods=['GET'])
def get_orden(id):
    orden = Ordenes.query.get(id)
    return orden_schema.jsonify(orden)

#POST Ordenes
@app.route('/ordenes',methods=['POST'])
def add_orden():
    idUsuario = request.json['idUsuario']
    idProducto = request.json['idProducto']
    nombreUsuario = request.json['nombreUsuario']
    fechaOrden = request.json['fechaOrden']
    numeroArticulos = request.json['numeroArticulos']
    total = request.json['total']
    new_orden = Ordenes(idUsuario,idProducto,nombreUsuario,fechaOrden,numeroArticulos,total)
    db.session.add(new_orden)
    db.session.commit()

    return orden_schema.jsonify(new_orden)

#PUT Ordenes
@app.route('/ordenes/<id>',methods=['PUT'])
def update_orden(id):
    ordenes = Ordenes.query.get(id)
    idUsuario = request.json['idUsuario']
    idProducto = request.json['idProducto']
    nombreUsuario = request.json['nombreUsuario']
    fechaOrden = request.json['fechaOrden']
    numeroArticulos = request.json['numeroArticulos']
    total = request.json['total']
    ordenes.idUsuario = idUsuario
    ordenes.idProducto = idProducto
    ordenes.nombreUsuario = nombreUsuario
    ordenes.fechaOrden = fechaOrden
    ordenes.numeroArticulos = numeroArticulos
    ordenes.total = total
    db.session.commit()
    return orden_schema.jsonify(ordenes)

#DELETE Ordenes
@app.route('/ordenes/<id>',methods=['DELETE'])
def delete_orden(id):
    ordenes = Ordenes.query.get(id)
    db.session.delete(ordenes)
    db.session.commit()
    return orden_schema.jsonify(ordenes)


# mensaje de bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje': 'Bienvenido a la API de tienda de ropa'})

if __name__ == '__main__':
    app.run(debug=True)
