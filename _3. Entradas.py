import csv
import openai
import re
import concurrent.futures
import threading
import unicodedata

apis = [line.strip() for line in open("0. GPTs.txt", "r", encoding="utf-8")]
titulos = list(csv.DictReader(open("2. Titulos.csv", newline='', encoding='utf-8')))
imagen_sistema = open("0. Sistema/1. Imagen.txt", "r", encoding="utf-8").read().strip()
imagen_usuario = open("1. Usuario/1. Imagen.txt", "r", encoding="utf-8").read().strip()
imagen_asistente = open("2. Asistente/1. Imagen.txt", "r", encoding="utf-8").read().strip()
estructura_sistema = open("0. Sistema/2. Estructura.txt", "r", encoding="utf-8").read().strip()
estructura_usuario = open("1. Usuario/2. Estructura.txt", "r", encoding="utf-8").read().strip()
estructura_asistente = open("2. Asistente/2. Estructura.txt", "r", encoding="utf-8").read().strip()
cuerpo_sistema = open("0. Sistema/3. Cuerpo.txt", "r", encoding="utf-8").read().strip()
cuerpo_usuario = open("1. Usuario/3. Cuerpo.txt", "r", encoding="utf-8").read().strip()
cuerpo_asistente = open("2. Asistente/3. Cuerpo.txt", "r", encoding="utf-8").read().strip()
descripcion_sistema = open("0. Sistema/4. Descripcion.txt", "r", encoding="utf-8").read().strip()
descripcion_usuario = open("1. Usuario/4. Descripcion.txt", "r", encoding="utf-8").read().strip()
descripcion_asistente = open("2. Asistente/4. Descripcion.txt", "r", encoding="utf-8").read().strip()
categoria_sistema = open("0. Sistema/5. Categoria.txt", "r", encoding="utf-8").read().strip()
categoria_usuario = open("1. Usuario/5. Categoria.txt", "r", encoding="utf-8").read().strip()
categoria_asistente = open("2. Asistente/5. Categoria.txt", "r", encoding="utf-8").read().strip()

clave_api_actual = 0
contador_titulos = 0
total_titulos = len(titulos)

def obtener_numero_articulos_existente():
    try:
        with open("3. Articulos.csv", "r", newline="", encoding="utf-8") as archivo_csv:
            lector = csv.reader(archivo_csv)
            next(lector)
            return sum(1 for _ in lector)
    except FileNotFoundError:
        return 0

articulos_actuales = obtener_numero_articulos_existente()

def chatGPT(sistema, usuario, asistente):
    global clave_api_actual
    respuesta = ""
    while True:
        clave_api_actual = (clave_api_actual + 1) % len(apis)
        clave_api = apis[clave_api_actual]
        openai.api_key = clave_api
        try:
            respuesta = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": usuario},
                    {"role": "assistant", "content": asistente}
                ]
            )
            texto_respuesta = respuesta.choices[0].message["content"].strip()
            return texto_respuesta
        except Exception:
            pass

def obtener_imagen(titulo):
    imagen = chatGPT(imagen_sistema, imagen_usuario.format(titulo=titulo), imagen_asistente)
    imagen = imagen.rstrip(".")
    if imagen.startswith('"') and imagen.endswith('"'):
        imagen = imagen[1:-1]
        imagen = imagen.rstrip(".")
    return imagen

def obtener_estructura(titulo):
    estructura = chatGPT(estructura_sistema, estructura_usuario.format(titulo=titulo), estructura_asistente.format(titulo=titulo))
    estructura = re.sub('\n+', '\n', estructura)
    estructura = estructura.replace("- ", "")
    estructura = estructura.split("\n")
    return estructura

def obtener_cuerpo(titulo, estructura):
    cuerpo = f"<p>{chatGPT(cuerpo_sistema, cuerpo_usuario.format(estructura=estructura), cuerpo_asistente.format(titulo=titulo))}"
    cuerpo = cuerpo.replace("<h2>Introducción</h2>", "")
    cuerpo = cuerpo.replace("<h3>Conclusiones</h3>", "")
    cuerpo = cuerpo.replace("<h3>Conclusión</h3>", "")
    cuerpo = re.sub(r'En (conclusión|resumen), (\w)', lambda match: match.group(2).upper(), cuerpo)
    cuerpo = cuerpo.replace("En conclusión, ", "").replace("En resumen, ", "")
    cuerpo = re.sub(r'<strong>En (conclusión|resumen),</strong> (\w)', lambda match: match.group(2).upper(), cuerpo)
    cuerpo = cuerpo.replace("<strong>En conclusión,</strong> ", "").replace("<strong>En resumen,</strong> ", "")
    return cuerpo

def obtener_descripcion(titulo):
    descripcion = chatGPT(descripcion_sistema, descripcion_usuario.format(titulo=titulo), descripcion_asistente)
    if descripcion.startswith('"') and descripcion.endswith('"'):
        descripcion = descripcion[1:-1]
    intentos = 0
    while len(descripcion) > 150 and intentos < 3:
        descripcion = chatGPT(descripcion_sistema, f"Haz más pequeña la metadescripción: \"{descripcion}\"", descripcion_asistente)
        if descripcion.startswith('"') and descripcion.endswith('"'):
            descripcion = descripcion[1:-1]
        intentos += 1
    return descripcion

def obtener_categoria(titulo):
    categoria = chatGPT(categoria_sistema, categoria_usuario.format(titulo=titulo), categoria_asistente)
    categoria = categoria.rstrip(".")
    if categoria.startswith('"') and categoria.endswith('"'):
        categoria = categoria[1:-1]
        categoria = categoria.rstrip(".")
    return categoria
def crear_slug(keywords):
    slug = unicodedata.normalize('NFKD', keywords.split('\n')[0].lower()).encode('ASCII', 'ignore').decode('ASCII').replace('ñ', 'n').replace(' ', '-')
    return slug

def procesar_titulo(titulo, escritor, bloqueo):
    global contador_titulos
    keyword = titulo["Keyword"]
    titulo = titulo["Titulo"]
    # imagen = obtener_imagen(titulo)
    estructura = obtener_estructura(titulo)
    articulo = obtener_cuerpo(titulo, estructura)
    descripcion = obtener_descripcion(titulo)
    categoria = obtener_categoria(titulo)
    slug = crear_slug(keyword)  # Nueva función para generar el slug
    fila = [keyword, titulo, articulo, descripcion, categoria, slug]  # Se agrega la nueva columna
    with bloqueo:
        escritor.writerow(fila)
        contador_titulos += 1
        print(f"{contador_titulos + articulos_actuales}/{total_titulos + articulos_actuales} | {keyword} | {titulo}")


def obtener_keywords_procesadas():
    procesadas = set()
    try:
        with open("3. Articulos.csv", "r", newline="", encoding="utf-8") as archivo_csv:
            lector = csv.reader(archivo_csv)
            try:
                next(lector)
            except StopIteration:
                return procesadas
            for fila in lector:
                procesadas.add(fila[0])
    except FileNotFoundError:
        pass
    return procesadas

keywords_procesadas = obtener_keywords_procesadas()
titulos_a_procesar = [titulo for titulo in titulos if titulo["Keyword"] not in keywords_procesadas]

with open("3. Articulos.csv", "a", newline="", encoding="utf-8") as archivo_csv:
    escritor = csv.writer(archivo_csv)
    if archivo_csv.tell() == 0:
        escritor.writerow(["Keyword", "Titulo", "Articulo", "Descripcion", "Categoria", "Slug"])  # Añade "Slug" al encabezado
    bloqueo = threading.Lock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=512) as ejecutor:
        futuros = [ejecutor.submit(procesar_titulo, titulo, escritor, bloqueo) for titulo in titulos_a_procesar]
        for futuro in concurrent.futures.as_completed(futuros):
            pass
