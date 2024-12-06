from flaskr import create_app
from flaskr.modelos.modelos import Usuario, Categoria, Ingreso, Gasto
from flask_migrate import Migrate
from .modelos import db 
from flask_restful import Api 
from flask_jwt_extended import JWTManager 
from flaskr.vistas.gasto import crear_super_admin

#rol vista
from flaskr.vistas.rol import CrearRol, ActualizacionRol
#usuario vista
from flaskr.vistas.usuario import VistaUsuario, VistaLogin, VistaSignIn
from flaskr.vistas.usuario import crear_super_admin

# categoria vista
from flaskr.vistas.categoria import actualizarcategoria, Ingresacategoria
# ingresos vista
from flaskr.vistas.ingreso import Modificaingreso, Ingresonuevo
# gasto vista
from flaskr.vistas.gasto import Gastonuevo

app = create_app('default')
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
migrate = Migrate(app, db)

api = Api(app)

#usuario///
api.add_resource(VistaUsuario, '/usuario', '/usuario/<int:id>')
api.add_resource(VistaLogin, '/login', '/login/<int:id>')
api.add_resource(VistaSignIn, '/signin', '/signin/<int:id>')

@app.before_first_request
def inicializar():
    crear_super_admin()

#rol//
api.add_resource(CrearRol, '/crear', '/rol/<int:id>')
api.add_resource(ActualizacionRol, '/actualizar', '/actualizar/<int:id>')

#categoria//
api.add_resource(actualizarcategoria, '/modificar', '/modificar/<int:id>')
api.add_resource(Ingresacategoria, '/ingreso', '/ingreso/<int:id>')

#ingresos//
api.add_resource(Modificaingreso, '/modificacion', '/modificacion/<int:id>')
api.add_resource(Ingresonuevo, '/nuevo', '/nuevo/<int:id>')

#gasto// 
api.add_resource(Gastonuevo, '/gasto')

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)