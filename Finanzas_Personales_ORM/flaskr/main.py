from flask import Flask, jsonify, request
import cloudinary
from cloudinary.uploader import upload
from cloudinary.api import resources


app = Flask(__name__)

# Configura Cloudinary
cloudinary.config(
    cloud_name='dylk4sewf',  
    api_key='979346585492836',       
    api_secret='WhfWz_iwygrTxWz5waZw-HP4fYg'   
)

@app.route('/upload', methods=['POST'])
def upload_image():
    archivo = request.files['archivo']
    resultado = cloudinary.uploader.upload(archivo)
    return jsonify({
        "message": "Imagen subida con éxito",
        "url": resultado['url']
    })

@app.route('/imagenes', methods=['GET'])
def obtener_imagenes():
    try:
        # Obtén la lista de recursos (imágenes) de Cloudinary
        result = cloudinary.api.resources(
            type='upload',
            max_results=30  # Número máximo de resultados
        )

        # Devuelve la lista de imágenes
        return jsonify(result['resources'])
    except Exception as e:
        print(f'Error al obtener imágenes: {e}')
        return jsonify({'error': 'Error al obtener imágenes de Cloudinary'}), 500

if __name__ == '__main__':
    app.run(debug=True)
