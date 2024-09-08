import json
from pedidos.models import Producto
from django.db.utils import IntegrityError

json_file_path = '../db_cocktails.json'

def run_fill_db():
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            productos_data = json.load(file)
            
            for producto in productos_data:
                try:
                    Producto.objects.create(
                        nombre=producto['nombre'],
                        categoria=producto['categoria'],
                        ingredientes=producto['ingredientes'],
                        precio=producto['precio'],
                        imagen_url=producto.get('imagen', '')
                    )
                    print(f"Producto '{producto['nombre']}' guardado correctamente.")
                except IntegrityError as e:
                    print(f"Error al guardar el producto '{producto['nombre']}': {str(e)}")
                    
    except FileNotFoundError:
        print(f"Archivo JSON no encontrado en la ruta: {json_file_path}")
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")