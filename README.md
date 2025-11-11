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

        
## Notas

El archivo de salida principal es `3. Articulos.csv` (generado por `_3. Entradas.py` y enriquecido en pasos posteriores).

Los directorios `0. Sistema`, `1. Usuario` y `2. Asistente` contienen los prompts que definen cómo se comporta el modelo en cada parte del proceso.

---

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

**Clonar el repositorio:**
git clone https://github.com/tu-usuario/dchbrain-v4o-mini.git

cd dchbrain-v4o-mini

**Crear y activar un entorno virtual**
python -m venv venv
**Linux / macOS**
source venv/bin/activate
**Windows**
venv\Scripts\activate

## Instalar dependencias:
pip install -r requirements.txt

**Configuración de claves de API**
El archivo 0. GPTs.txt almacena las claves de la API de OpenAI.

Formato:

sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

sk-yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

## Uso

1. Preparar las keywords

Edita `1. Keywords.txt` y añade una keyword por línea:
ideas para ahorrar energía en casa
cómo elegir un portátil para programar
beneficios del ejercicio al aire libre

2. Titularizar
python "_2. Titularizar.py"
Este script generará un archivo `2. Titulos.csv` donde habrá genera un título SEO en base a cada keyword

3. Generar artículos

python "_3. Entradas.py"
Este script:
- 3.1 Lee 1. `2. Titulos.csv`
- 3.2 Llama a la API de OpenAI usando los prompts de 0. Sistema, 1. Usuario y 2. Asistente.
- 3.3 Genera el contenido y lo guarda en `3. Articulos.csv`

4. Añadir vídeos de YouTube

python "_4. YouTube.py"
Este script:
- 4.1 Lee 3. Articulos.csv.
- 4.2 Busca un vídeo relevante para cada artículo.
- 4.3 Añade el código de inserción del vídeo en el contenido.

5. Asignar fechas y autores

python "_5. Fechas.py"
python "_6. Autores.py"
Estos scripts añaden columnas de fecha y autor a 3. Articulos.csv.

6. Generar imágenes

python "_7. Imagen.py"
Este script:
- 6.1 Lee el título o información relevante de cada artículo.
- 6.2 Llama a la API de imágenes de OpenAI.
- 6.3 Guarda cada imagen en 3. Portadas/.
- 6.4 Opcionalmente añade la referencia de la imagen al CSV de artículos.

Resultado final:

 - Articulos.csv con todos los campos necesarios para tu CMS.

 - Portadas/ con las imágenes asociadas.

Personalización de prompts

Los prompts se organizan en tres carpetas:

- 0. Sistema: instrucciones de alto nivel para el modelo (rol del sistema).

- 1. Usuario: instrucciones que simulan la petición del usuario.

- 2. Asistente: ejemplos o ajustes de tono del asistente.

Cada carpeta contiene ficheros separados para:

- 0. Titulo.txt

- 1. Imagen.txt

- 2. Estructura.txt

- 3. Cuerpo.txt

- 4. Descripcion.txt

- 5. Categoria.txt

Editando estos ficheros puedes cambiar el estilo de escritura, el enfoque del contenido, el tono de las descripciones y las reglas de clasificación sin tocar el código Python.

**made by Pedro Corchuelo**