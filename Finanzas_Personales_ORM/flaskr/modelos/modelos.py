from marshmallow import fields
from flask_sqlalchemy  import SQLAlchemy

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


#tablas/clases del proyecto

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    descripcion =db.Column(db.String(100), nullable=True)
    super_admin = db.Column(db.Boolean, default=False)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=True)
    contrasena_hash = db.Column(db.String(128), nullable=True)  
    correo =db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(100), nullable=False)
    
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    
    rol = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))
    
    
           
    @property
    def contrasena(self):
        raise AttributeError("La contraseña no es un atributo legible.")

    @contrasena.setter
    def contrasena(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def verificar_contrasena(self, password):
        return check_password_hash(self.contrasena_hash, password) 
    
    @property
    def es_super_admin(self):
        return self.rol.super_admin 
    
    
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=True)
    


class Ingreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=True)
    descripcion = db.Column(db.String(200))
    fecha = db.Column(db.Date)
    
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    categoria = db.relationship('Categoria', backref=db.backref('ingresos', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('ingresos', lazy=True))


class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=True)
    descripcion = db.Column(db.String(200))
    fecha = db.Column(db.Date)
    imagen_url = db.Column(db.String(200), nullable=True)
    
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    categoria = db.relationship('Categoria', backref=db.backref('gastos', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('gastos', lazy=True))
    
    

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        include_relationships = True 
        load_instance = True
    
    
class UsuarioSchema(SQLAlchemyAutoSchema):
    rol = fields.Nested(RolSchema)
    es_super_admin = fields.Boolean(dump_only=True)

    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

        
        
class CategoriaSchema(SQLAlchemyAutoSchema):
    class meta:
        model = Categoria
        include_relationships = True  
        load_instance = True
        
        
        
class IngresoSchema(SQLAlchemyAutoSchema):
    categoria = fields.Nested(CategoriaSchema) 
    class meta:
        model = Ingreso
        include_relationships = True 
        load_instance = True
        
        

class GastoSchema(SQLAlchemyAutoSchema):
    categoria = fields.Nested(CategoriaSchema) 
    class meta:
        model = Gasto
        include_relationships = True 
        load_instance = True
        