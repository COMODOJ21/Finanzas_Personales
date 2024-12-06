from flask import request, abort
from flask_restful import Resource
from flaskr.modelos.modelos import db, Usuario, UsuarioSchema, Rol
from flask_jwt_extended import jwt_required, create_access_token

usuario_schema = UsuarioSchema()

class VistaUsuario(Resource):
    def get(self): 
       return [usuario_schema.dump(usuario) for usuario in Usuario.query.all()]


    def post(self): 
        nuevo_usuario = Usuario(
            nombre=request.json['nombre'],
            contrasena=request.json['contrasena'],
            correo=request.json['correo'],
            telefono=request.json['telefono']  
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        usuario_actualizados = usuario_schema.dump(nuevo_usuario)
        return usuario_actualizados, 200

    def put(self, id): 
        usuario = Usuario.query.get(id)
        if usuario:
            usuario.nombre = request.json.get('nombre', usuario.nombre)
            usuario.contrasena = request.json.get('contrasena', usuario.contrasena)
            usuario.correo = request.json.get('correo', usuario.correo)
            usuario.telefono = request.json.get('telefono', usuario.telefono)
            db.session.commit()
            usuarios_actualizados = usuario_schema.dump(usuario)
        return usuarios_actualizados, 200

    def delete(self, id): 
        usuario = Usuario.query.get(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return {'message': 'Usuario eliminado'}, 200
        return {'message': 'Usuario no encontrado'}, 400

class VistaLogin(Resource):
    def post(self):
        u_nombre = request.json["nombre"]
        u_contrasena = request.json["contrasena"]
        usuarios = Usuario.query.filter_by(nombre=u_nombre).first()
        if usuarios and usuarios.verificar_contrasena(u_contrasena):
            return {'mensaje': 'Inicio de sesión exitoso'}, 200
        else:
            return {'mensaje': 'Nombre de usuario o contraseña incorrectos'}, 400

class VistaSignIn(Resource):
    def post(self):        
        nuevo_usuario = Usuario(
        nombre=request.json["nombre"],
        contrasena=request.json["contrasena"],
        correo = request.json["correo"],
        telefono = request.json["telefono"],
        rol_id=request.json['rol_id']
        )
        token_de_acceso = create_access_token(identity=request.json['nombre'])
        db.session.add(nuevo_usuario)
        db.session.commit()   
        return {'mensaje': 'Usuario creado exitosamente', 'token_de_acceso': token_de_acceso}, 200
    
def crear_super_admin():
    rol_super_admin = Rol.query.filter_by(descripcion="Super Admin").first()
    if not rol_super_admin:
        rol_super_admin = Rol(descripcion="Super Admin", super_admin=True)
        db.session.add(rol_super_admin)
        db.session.commit()

    usuario_super_admin = Usuario(
        nombre="Super Admin",
        correo="admin@finanzas.com",
        telefono="123456789",
        contrasena="supersecretpassword",
        rol_id=rol_super_admin.id
    )
    db.session.add(usuario_super_admin)
    db.session.commit()
