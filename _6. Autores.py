import csv
import random

def modificar_csv(archivo_entrada):
    autores = [line.strip() for line in open("1. Autores.txt", "r", encoding="utf-8")]
    with open(archivo_entrada, 'r', newline="", encoding="utf-8") as archivo_csv_entrada:
        datos_csv = list(csv.reader(archivo_csv_entrada))
        datos_csv[0].append("Autor")
        for fila in datos_csv[1:]:
            fila.append(random.choice(autores))
    with open(archivo_entrada, 'w', newline="", encoding="utf-8") as archivo_entrada:
        escritor = csv.writer(archivo_entrada)
        escritor.writerows(datos_csv)

modificar_csv("3. Articulos.csv")
