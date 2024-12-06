from flask import request
from flask_restful import Resource
from flaskr.modelos.modelos import db, Ingreso, IngresoSchema


ingreso_schema = IngresoSchema()

class Modificaingreso(Resource):
    def get(self): 
        return [ingreso_schema.dump(Ingreso) for Ingreso in Ingreso.query.all()]
    
    def post(self):
        modificaringreso = Ingreso(
            cantidad=request.json['cantidad'],
            descripcion=request.json['descripcion'],
            fecha=request.json['fecha'],
        )
        db.session.add(modificaringreso)
        db.session.commit()
        modificado =ingreso_schema.dum(modificaringreso)
        return modificado, 200
    
    def put (self, id):
        ingreso = Ingreso.query.get(id)
        if ingreso:
            ingreso.cantidad = request.json.get('cantidad', Ingreso.cantidad)
            ingreso.descripcion = request.json.get('descripcion', Ingreso.descripcion)
            ingreso.fecha = request.json.get('nota', Ingreso.fecha)
            db.session.commit()
            actualizar_ingreso = ingreso_schema.dum(Ingreso)
            return actualizar_ingreso, 200
        
    def delete(self, id): 
        ingreso= Ingreso.query.get(id)
        if ingreso:
            db.session.delete(Ingreso)
            db.session.commit()
            return {'message': 'Ingreso eliminado'}, 200
        return {'message': 'Ingreso no encontrado'}, 400

class Ingresonuevo(Resource):
    def post(self):        
        nuevoingreso = Ingreso(
        cantidad=request.json.get("cantidad"),
        descripcion=request.json["descripcion"],
        fecha=request.json["fecha"],
        categoria_id = request.json.get('categoria_id', None),
        usuario_id=request.json['usuario_id']
        )
        db.session.add(nuevoingreso)
        db.session.commit()   
        return {'mensaje': 'Ingresado exitosamente' }, 200  