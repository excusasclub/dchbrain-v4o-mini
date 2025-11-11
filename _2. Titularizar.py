import csv
import openai
import concurrent.futures
import threading
import os

apis = [line.strip() for line in open("0. GPTs.txt", "r", encoding="utf-8")]
keywords = [line.strip() for line in open("1. Keywords.txt", "r", encoding="utf-8")]
titulo_sistema = open("0. Sistema/0. Titulo.txt", "r", encoding="utf-8").read().strip()
titulo_usuario = open("1. Usuario/0. Titulo.txt", "r", encoding="utf-8").read().strip()
titulo_asistente = open("2. Asistente/0. Titulo.txt", "r", encoding="utf-8").read().strip()

clave_api_actual = 0

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
        except Exception as e:
            pass

bloqueo = threading.Lock()

def procesar_keyword(keyword):
    global contador_keywords
    titulo = chatGPT(titulo_sistema, titulo_usuario.format(keyword=keyword), titulo_asistente).rstrip(".").strip('"').rstrip(".")
    intentos = 0
    while len(titulo) > 70 and intentos < 3:
        titulo = chatGPT(titulo_sistema, f"Haz más pequeño el título: \"{titulo}\"", titulo_asistente).rstrip(".").strip('"').rstrip(".")
        intentos += 1
    resultado = [keyword, titulo]
    with bloqueo:
        contador_keywords += 1
        print(f"{contador_keywords}/{len(keywords_trabajadas) + len(keywords_a_procesar)} | {keyword} | {titulo}")
        with open("2. Titulos.csv", "a", newline="", encoding="utf-8") as archivo_csv:
            escritor = csv.writer(archivo_csv)
            if os.path.getsize("2. Titulos.csv") == 0:
                escritor.writerow(["Keyword", "Titulo"])
            escritor.writerow(resultado)

def obtener_keywords_trabajadas():
    trabajadas = set()
    try:
        with open("2. Titulos.csv", "r", newline="", encoding="utf-8") as archivo_csv:
            lector = csv.reader(archivo_csv)
            try:
                next(lector)
            except StopIteration:
                return trabajadas
            for fila in lector:
                trabajadas.add(fila[0])
    except FileNotFoundError:
        pass
    return trabajadas

keywords_trabajadas = obtener_keywords_trabajadas()
keywords_a_procesar = [kw for kw in keywords if kw not in keywords_trabajadas]
contador_keywords = len(keywords_trabajadas)

with concurrent.futures.ThreadPoolExecutor(max_workers=512) as ejecutor:
    [ejecutor.submit(procesar_keyword, keyword) for keyword in keywords_a_procesar]
