# DchBrain V4o-mini · Generador automático de contenido para blogs
DchBrain V4o-mini es un sistema en Python para generar contenido de blog a gran escala a partir de una lista de palabras clave. El pipeline convierte cada keyword en un artículo completo en HTML con:
- Título
- Estructura (H2, H3, etc.)
- Cuerpo del texto
- Meta descripción SEO
- Categoría
- Slug para la URL
- Vídeo de YouTube incrustado
- Imagen generada con IA
Está pensado como una cadena de montaje de contenido: de un simple listado de keywords a artículos listos para importar en tu CMS.


## Características principales
- Generación de texto con IA usando la API de OpenAI (GPT-4o-mini).
- Generación de imágenes por artículo con la API de OpenAI (DALL·E u otro modelo).
- Búsqueda y añadido automático de vídeos relevantes de YouTube para cada entrada.
- Prompts definidos en ficheros de texto (`.txt`), fáciles de editar sin tocar código.
- Procesamiento concurrente de múltiples artículos para reducir tiempos.
- Rotación de claves de API para repartir carga y mitigar límites de uso.
- Persistencia en CSV para no repetir trabajo sobre keywords ya procesadas.

## Flujo de trabajo
El proceso completo se ejecuta en varios pasos secuenciales, guiados por los scripts numerados en la raíz del proyecto:

1. Preparación de keywords  
   - Archivo de entrada: `1. Keywords.txt`  
   - Contiene la lista de palabras clave, una por línea.

2. Generación de títulos (opcional según tu flujo actual)  
   - Script: `_2. Titularizar.py`  
   - A partir de las keywords, puede generar títulos o preparar un CSV intermedio.

3. Generación de artículos  
   - Script principal: `_3. Entradas.py`  
   - Para cada keyword o título:
     - Llama a la API de OpenAI.
     - Genera título, estructura (H2/H3), cuerpo en HTML, meta descripción, categoría y slug.
     - Escribe el resultado en `3. Articulos.csv`.

4. Inserción de vídeos de YouTube  
   - Script: `_4. YouTube.py`  
   - Para cada artículo en `3. Articulos.csv`:
     - Busca un vídeo relevante en YouTube en función del tema.
     - Añade el código de incrustación del vídeo al contenido.

5. Asignación de fechas y autores  
   - Scripts: `_5. Fechas.py` y `_6. Autores.py`  
   - Enriquecen `3. Articulos.csv` con:
     - Fecha de publicación.
     - Autor o perfil de autor.

6. Generación de imágenes  
   - Script: `_7. Imagen.py`  
   - Para cada artículo:
     - Llama a la API de imágenes de OpenAI.
     - Guarda la imagen resultante en `3. Portadas/`.
     - Opcionalmente añade la ruta de la imagen al CSV.

Al final del proceso, `3. Articulos.csv` contiene todos los artículos listos para importarse en un CMS y la carpeta `3. Portadas/` contiene las imágenes asociadas.



## Estructura del proyecto

Estructura actual de archivos y directorios:
```text
.
│   .DS_Store
│   0. GPTs.txt          ← Claves de API de OpenAI (una por línea)
│   1. Keywords.txt      ← Lista de keywords de entrada
│   _2. Titularizar.py   ← Generación de títulos (opcional)
│   _3. Entradas.py      ← Generación de artículos (script principal)
│   _4. YouTube.py       ← Búsqueda y añadido de vídeos de YouTube
│   _5. Fechas.py        ← Asignación de fechas a los artículos
│   _6. Autores.py       ← Asignación de autores
│   _7. Imagen.py        ← Generación de imágenes por artículo
│
├───0. Sistema           ← Prompts de sistema para la IA
│       0. Titulo.txt
│       1. Imagen.txt
│       2. Estructura.txt
│       3. Cuerpo.txt
│       4. Descripcion.txt
│       5. Categoria.txt
│
├───1. Usuario           ← Prompts de usuario para la IA
│       0. Titulo.txt
│       1. Imagen.txt
│       2. Estructura.txt
│       3. Cuerpo.txt
│       4. Descripcion.txt
│       5. Categoria.txt
│
├───2. Asistente         ← Prompts de asistente para la IA
│       0. Titulo.txt
│       1. Imagen.txt
│       2. Estructura.txt
│       3. Cuerpo.txt
│       4. Descripcion.txt
│       5. Categoria.txt
│
├───3. Portadas          ← Imágenes generadas por IA
│
└───_. Keywords CSV
        .DS_Store
        README.md
        requierements.txt
        
```

        
## Notas

El archivo de salida principal es `3. Articulos.csv` (generado por `_3. Entradas.py` y enriquecido en pasos posteriores).

Los directorios `0. Sistema`, `1. Usuario` y `2. Asistente` contienen los prompts que definen cómo se comporta el modelo en cada parte del proceso.

.........................................................................................

## Requisitos

- Python 3.10 o superior  
- Google Chrome u otro navegador compatible si usas Selenium para la parte de YouTube  
- `chromedriver` o el driver correspondiente instalado y accesible en el PATH  

## Dependencias 

- `openai`  
- `pandas`  
- `requests`  
- `selenium`  
- `python-dotenv` (si se usa)  
- Cualquier otra dependencia que uses en tus scripts  

## Instalación

### Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/dchbrain-v4o-mini.git

cd dchbrain-v4o-mini
```

### Crear y activar un entorno virtual
```bash
python -m venv venv
```

### Linux / macOS
```bash
source venv/bin/activate
```

### Windows
```bash
venv\Scripts\activate
```

## Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración de claves de API
El archivo 0. GPTs.txt almacena las claves de la API de OpenAI.

Formato:

sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

sk-yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

## Uso

### 1. Preparar las keywords
Edita el archivo `1. Keywords.txt` y añade una keyword por línea:

```text  
ideas para ahorrar energía en casa  
cómo elegir un portátil para programar  
beneficios del ejercicio al aire libre  
```

.........................................................................................

### 2. Titularizar
Genera los títulos SEO a partir de las keywords:

```bash
python "_2. Titularizar.py"  
```

Este script crea un archivo `2. Titulos.csv` con los títulos optimizados según cada palabra clave.

.........................................................................................

### 3. Generar artículos
Crea los artículos completos en HTML:

```bash  
python "_3. Entradas.py"  
```

Este script:  
1. Lee `2. Titulos.csv`.  
2. Llama a la API de OpenAI usando los prompts de `0. Sistema`, `1. Usuario` y `2. Asistente`.  
3. Genera los artículos y los guarda en `3. Articulos.csv`.

.........................................................................................

### 4. Añadir vídeos de YouTube
Asocia vídeos relevantes a cada artículo:

```bash  
python "_4. YouTube.py"  
```

Este script:  
1. Lee `3. Articulos.csv`.  
2. Busca un vídeo relevante en YouTube.  
3. Inserta el código de vídeo en el contenido HTML del artículo.

.........................................................................................

### 5. Asignar fechas y autores
Ejecuta ambos scripts para completar la información de publicación:

```bash  
python "_5. Fechas.py"  
python "_6. Autores.py"  
```

Estos scripts añaden columnas de **fecha** y **autor** a `3. Articulos.csv`.

.........................................................................................

### 6. Generar imágenes
Crea las imágenes personalizadas para cada artículo:

```bash  
python "_7. Imagen.py"  
```

Este script:  
1. Lee el título o la información relevante del artículo.  
2. Llama a la API de imágenes de OpenAI.  
3. Guarda la imagen en `3. Portadas/`.  
4. (Opcional) Añade la ruta de la imagen al CSV final.

.........................................................................................

### Resultado final

- `3. Articulos.csv` contiene los artículos listos para tu CMS.  
- `3. Portadas/` guarda todas las imágenes generadas.

.........................................................................................

## Personalización de prompts

Los prompts definen el estilo, tono y enfoque de los textos generados.  
Están organizados en tres carpetas:

- `0. Sistema`: instrucciones de alto nivel para el modelo (rol del sistema).  
- `1. Usuario`: instrucciones que simulan la petición del usuario.  
- `2. Asistente`: ejemplos o ajustes de tono del asistente.  

Cada carpeta contiene los siguientes archivos:

- `0. Titulo.txt`  
- `1. Imagen.txt`  
- `2. Estructura.txt`  
- `3. Cuerpo.txt`  
- `4. Descripcion.txt`  
- `5. Categoria.txt`  

Puedes modificar cualquiera de estos archivos para cambiar el tono, estilo y reglas de redacción sin alterar el código Python.

.........................................................................................

**Made by Pedro Corchuelo**