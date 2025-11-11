import csv
import openai
import os
import requests

# Función para obtener la clave de API de OpenAI desde el archivo
def obtener_clave_openai(archivo_claves):
    with open(archivo_claves, 'r', encoding='utf-8') as f:
        return f.read().strip()

# Carpeta para guardar las imágenes
carpeta_portadas = '3. Portadas'  
os.makedirs(carpeta_portadas, exist_ok=True)

def leer_titulos_desde_csv(archivo_csv):
    titulos = []
    with open(archivo_csv, 'r', newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            titulos.append(fila['Titulo'])
    return titulos

def procesar_imagen(titulo, clave_openai):
    try:
        openai.api_key = clave_openai
        respuesta = openai.Image.create(n=1, prompt=f"Generar imagen para: {titulo}", size="512x512")
        url_imagen = respuesta["data"][0]["url"]
        print(f"URL de la imagen: {url_imagen}")
        nombre_archivo = f"hola_{os.urandom(2).hex()}.webp"
        imagen = requests.get(url_imagen).content
        ruta_guardado = os.path.join(carpeta_portadas, nombre_archivo)
        with open(ruta_guardado, 'wb') as f:
            f.write(imagen)
        print(f"Imagen guardada: {nombre_archivo}")
        return nombre_archivo, url_imagen
    except openai.error.OpenAIError as e:
        # Manejo de errores si la generación de imagen falla
        print(f"Error al procesar imagen para '{titulo}': {e}")
        return None, None

def procesar_titulos(archivo_csv, archivo_claves):
    clave_openai = obtener_clave_openai(archivo_claves)
    titulos = leer_titulos_desde_csv(archivo_csv)
    
    for titulo in titulos:
        # Generar imagen
        procesar_imagen(titulo, clave_openai)

# Ejecutar el procesamiento del CSV
archivo_csv = '3. Articulos.csv'  
archivo_claves = '0. GPTs.txt'  
procesar_titulos(archivo_csv, archivo_claves)
