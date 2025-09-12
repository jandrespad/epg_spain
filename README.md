# EPG Fixed Timezone (Spain)

Este script de Python descarga un fichero EPG (Guía Electrónica de Programas) en formato XML desde una URL, ajusta las marcas de tiempo de los programas según unas reglas predefinidas y guarda el resultado en un nuevo fichero XML.

## Características

- **Descarga en memoria**: El fichero EPG se descarga directamente desde una URL sin necesidad de guardarlo localmente primero.
- **Configuración externa**: Todas las variables (URL, nombre del fichero de salida, zona horaria) se gestionan a través de un fichero `.env`, sin necesidad de modificar el código.
- **Corrección de zona horaria**: Aplica una lógica específica para corregir las horas de inicio y fin de los programas basándose en el offset de zona horaria incorrecto del fichero original.

## Requisitos

- Python 3.x
- Las siguientes librerías de Python:
  - `requests`
  - `python-dotenv`

## Instalación

1.  **Clona el repositorio o descarga los ficheros del proyecto:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO>
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    Para activarlo:
    - En Windows: `.\venv\Scripts\activate`
    - En macOS/Linux: `source venv/bin/activate`

3.  **Instala las dependencias necesarias:**
    Crea un fichero `requirements.txt` con el siguiente contenido:
    ```txt
    requests
    python-dotenv
    ```
    Y luego instálalo con pip:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración

1.  **Crea el fichero `.env`** en el directorio raíz del proyecto. Puedes copiar el contenido del fichero `env.example` si existe, o usar la siguiente plantilla:

    ```env
    # URL del fichero EPG original que se va a descargar.
    EPG_URL="https://fuente/guiaepg.xml"

    # Nombre del fichero XML que se generará con las correcciones.
    OUTPUT_FILENAME="ficherosalida.xml"

    # Zona horaria de destino deseada (offset en horas).
    # Ejemplo: 2 para CEST (horario de verano en España), 1 para CET (horario de invierno).
    TIMEZONE_OFFSET_HOURS=2
    ```

2.  **Modifica los valores** en el fichero `.env` según tus necesidades.

## Uso

Una vez que hayas completado la instalación y configuración, simplemente ejecuta el script principal desde tu terminal:

```bash
python main.py
```

El script descargará el fichero, procesará los datos y, si todo va bien, verás un mensaje de confirmación. El fichero corregido (`ficherosalida.xml` o el nombre que hayas configurado) aparecerá en el directorio raíz del proyecto.