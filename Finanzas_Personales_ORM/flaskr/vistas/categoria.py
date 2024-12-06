from flask import request
from flask_restful import Resource
from flaskr.modelos.modelos import db, Categoria, CategoriaSchema

categoria_schema = CategoriaSchema()

class actualizarcategoria(Resource):
    def get(self): 
        return [categoria_schema.dump(Categoria) for Categoria in Categoria.query.all()]
    
    def post(self):
        categoria = Categoria(
            nombre=request.json['nombe'],
        )
        db.session.add(categoria)
        db.session.commit()
        perfecto =categoria_schema.dum(categoria)
        return perfecto, 200
    
    def put (self, id):
        categoria = Categoria.query.get(id)
        if categoria:
            categoria.descripcion = request.json.get('nombre', Categoria.descripcion)
            db.session.commit()
            modificar = categoria_schema.dum(categoria)
            return modificar, 200
        
    def delete(self, id): 
        categoria= Categoria.query.get(id)
        if categoria:
            db.session.delete(Categoria)
            db.session.commit()
            return {'message': 'eliminado'}, 200
        return {'message': 'no encontrado'}, 400
    
class Ingresacategoria(Resource):
    def post(self):        
        categoria = Categoria(
        nombre=request.json["nombre"],
        )
        db.session.add(categoria)
        db.session.commit()   
        return {'mensaje': 'Categoria ingresada corectamente' }, 200