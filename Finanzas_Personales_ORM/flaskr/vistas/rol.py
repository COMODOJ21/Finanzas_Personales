from flask import request
from flask_restful import Resource
from flaskr.modelos.modelos import db, Rol, RolSchema


rol_schema = RolSchema()

class ActualizacionRol(Resource):
    def get(self): 
        return [rol_schema.dump(Rol) for Rol in Rol.query.all()]
    
    def post(self):
        nuevo_rol = Rol(
            descripcion=request.json['nota'],
        )
        db.session.add(nuevo_rol)
        db.session.commit()
        actualizar =rol_schema.dum(nuevo_rol)
        return actualizar, 200
    
    def put (self, id):
        rol = Rol.query.get(id)
        if rol:
            rol.descripcion = request.json.get('nota', Rol.descripcion)
            db.session.commit()
            actualizar_rol = rol_schema.dum(Rol)
            return actualizar_rol, 200
        
    def delete(self, id): 
        rol= Rol.query.get(id)
        if rol:
            db.session.delete(Rol)
            db.session.commit()
            return {'message': 'Rol eliminado'}, 200
        return {'message': 'Rol no encontrado'}, 400

class CrearRol(Resource):
    def post(self):        
        nuevo_rol = Rol(
        descripcion=request.json["descripcion"],
        )
        db.session.add(nuevo_rol)
        db.session.commit()   
        return {'mensaje': 'Rol creado exitosamente' }, 200      