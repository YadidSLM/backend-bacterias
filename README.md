# backend-bacterias

Backend en **Flask (Python 3.11)** para la graficación de datos de expresión génica bacteriana y construcción de redes de coexpresión.  

## Requisitos

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [PostgreSQL 12 o superior](https://www.postgresql.org/download/)
- Al menos 7 GB de almacenamiento disponible para la carga de datos a la base de datos.

## Instalación

1. Clona este repositorio:
   Asegúrate de estar en la rama bacterias_ubuntu antes de clonar el repo.

   ```bash
   git clone https://github.com/YadidSLM/backend-bacterias.git
   cd backend-bacterias
   ```

2. Crea un entorno virtual e instálalo:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración de la base de datos

1. Asegúrate de tener PostgreSQL corriendo.
2. Crea la base de datos llamada **bacterias**:

   ```sql
   CREATE DATABASE bacterias;
   ```

3. Configura las variables de entorno necesarias en tu sistema:

   - `DB_USER` -> Nombre de usuario de la base de datos, ej. bacterias_user.
   - `DB_PASSWORD` -> Contraseña del usuario de PostgreSQL.
   - `FLASK_APP=src/app.py`
   - `DB_HOST=localhost` -> Si lo corres localmente.
   - `DB_PORT` -> Puerto que uses para el servidor, puedes intener con 5432 si está ocupado usa otro puerto.
   - `DB_NAME=bacterias` -> Nombre de la base de datos
   

4. Genera las tablas ejecutando el archivo Python correspondiente (revisa que estés en la carpeta del proyecto):

   ```bash
   python -m src.management_db.create_db
   ```
   Si quieres borrar las tablas puedes ejecutar el sript dentro de management_db:
   ```bash
   python -m src.management_db.drop.db
   ```
## Cargar bacterias a la base de datos:

Descarga las siguientes tablas .txt de la bacteria que desees descargar de:
```
https://drive.google.com/drive/folders/1rs2O2_eArKa3i87IL2WOfSW7LKr_eGi0?usp=drive_link
```
- colombos**Nombre de bacteria**.txt
- Signed-CytoscapeInput-edges-**Nombre de bacteria**-Bicor00.txt
- SignedCytoscapeInput-nodes-**Nombre de bacteria**-Bicor00.txt

Muévelas a una carpeta con el nombre de la bacteria dentro de la carpeta archivos que está dentro de src como se muestra en el diagrama:
```
backend-bacterias/
│── requirements.txt
│── README.md
└── src/
   ├── archivos/
   |   ├── bacteria1ACargar/
   |   |   ├──colombosNombre_de_bacteria.txt
   |   |   ├──Signed-CytoscapeInput-edges-nombre de bacteria-Bicor00.txt
   |   |   └──SignedCytoscapeInput-nodes-nombre de bacteria-Bicor00.txt
   |   ├── bacteria2ACargar/
   |   |   ├──colombosNombre_de_bacteria.txt
   |   |   ├──Signed-CytoscapeInput-edges-nombre de bacteria-Bicor00.txt
   |   |   └──SignedCytoscapeInput-nodes-nombre de bacteria-Bicor00.txt
   |   └──
   ├── models/            # Modelos de SQLAlchemy
   ├── management_db/     # Configuración y conexión a la BD
   │   ├── app.py         # Punto de entrada del servidor Flask
   │   └── create_tables.py (ejemplo)
   └── ...
```
Después de tener los archivos importados ahora es posible cargar una bacteria a la vez; después de seguir las siguientes instrucciones, haga lo mismo con las bacterias que quiera ir cargando a la base de datos:

1. Ve al script load_data.py y modifica el nombre de los archvios y el nombre de la carepeta de la bacteria que estés cargando en las líneas 8, 9 y 10.
2. Tomando en cuenta los id_bacteria que se muestran de la línea 24 a la 41, ve a la línea 87 e ingresa el índice de la lista donde se encuentra la bacteria a cragar sus datos en la siguiente línea:
```
bact = db.session.query(Bacteria).filter(Bacteria.bacteria == bacterias[ ÍNDICE AQUÍ ]).one_or_none()

Ejemplo:
bact = db.session.query(Bacteria).filter(Bacteria.bacteria == bacterias[3]).one_or_none() #Bacteria Tther con id_bacteria 2 e índice 3.
```
Corra el script con:
```bash
python -m src.management_db.load_data
```
Va a tardar alrededor de 12 horas cargar todos los datos, dependiendo de la bacteria.
Al finalizar la carga de datos, puede borrar los archvos de la bacteria de la carpeta archivos y puede volver a hacer lo mismo para cargar otra bacteria.

## Ejecución del servidor

Desde la carpeta `backend-bacterias`, enciende el servidor con:

```bash
python -m src.management_db.app
```

El backend quedará corriendo en:

```
http://127.0.0.1:4000
```

## Acceder a la base de datos de postgreSQL desde la terminal.
Verifica que tengas postgres instalado, puedes acceder al manejador de la base de datos con:
```
psql -h localhost -U bacterias_user -d bacterias
```
Ya dentro puedes hacer las consultas SQL que desees hacer.
Para ver las tablas puedes ejecutar: `\d`

Y para salir de postreSQL con: `exit`

## Uso de la API
1. Para recibir imagen base 64 de la red de coexpresión.
Ingresa el locus tag que desees buscar en la siguiente ruta:
```
http://127.0.0.1:4000/coexpresion_network/get-network/locus_tag
```

2. Para recibir imagen base 64 del boxplot.
Ingresa el locus tag que desees buscar en la siguiente ruta:
```
http://127.0.0.1:4000/expresion/boxplot/locus_tag
```
Regresa en datos JSON la imagen base 64 la cual puedes copiar y pegar en una nueva ventana de navegador para previsualizarla.
