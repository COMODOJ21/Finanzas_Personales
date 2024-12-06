from flask import request
from flask_restful import Resource
from flaskr.modelos.modelos import db, Gasto, GastoSchema
from cloudinary.uploader import upload
from werkzeug.security import generate_password_hash



gasto_schema = GastoSchema()

class Gastonuevo(Resource):
    def get(self): 
        return [gasto_schema.dump(gasto) for gasto in Gasto.query.all()]
    
    def post(self):       
        nuevogasto = Gasto(
            cantidad=request.json["cantidad"],
            descripcion=request.json["descripcion"],
            fecha=request.json["fecha"],
        )
        db.session.add(nuevogasto)
        db.session.commit()   
        return {'mensaje': 'Gasto ingresado exitosamente' }, 200
    
    def put (self, id):
        gasto = Gasto.query.get(id)
        if gasto:
            gasto.cantidad = request.json.get('cantidad', gasto.cantidad)
            gasto.descripcion = request.json.get('descripcion', gasto.descripcion)
            gasto.fecha = request.json.get('nota', gasto.fecha)
            db.session.commit()
            return gasto_schema.dump(gasto), 200
        return {'message': 'Gasto no encontrado'}, 400
        
    def delete(self, id): 
        gasto= Gasto.query.get(id)
        if gasto:
            db.session.delete(gasto)
            db.session.commit()
            return {'message': 'Gasto eliminado'}, 200
        return {'message': 'Gasto no encontrado'}, 400
    

from flaskr.modelos.modelos import db, Usuario, Rol
from werkzeug.security import generate_password_hash

def crear_super_admin():
    rol_super_admin = Rol.query.filter_by(descripcion="Super Admin").first()
    if not rol_super_admin:
        rol_super_admin = Rol(descripcion="Super Admin", super_admin=True)
        db.session.add(rol_super_admin)
        db.session.commit()  

    usuario_super_admin = Usuario.query.filter_by(nombre="Super Admin").first()
    if not usuario_super_admin:
        hashed_password = generate_password_hash("supersecretpassword", method='sha256')
        usuario_super_admin = Usuario(
            nombre="Super Admin",
            correo="admin@finanzas.com",
            telefono="123456789",
            contrasena=hashed_password,
            rol_id=rol_super_admin.id  
        )
        db.session.add(usuario_super_admin)
        db.session.commit()
        print(f"Usuario 'Super Admin' creado con rol {rol_super_admin.descripcion}.")
    else:
        print("El usuario 'Super Admin' ya existe.")



