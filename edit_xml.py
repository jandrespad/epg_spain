import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def ajustar_hora_epg(archivo_entrada, archivo_salida, horas_a_restar):
    """
    Ajusta la hora de inicio y fin de los programas en un archivo XML de EPG.

    Args:
        archivo_entrada (str): Ruta al archivo XML de entrada.
        archivo_salida (str): Ruta donde se guardará el archivo XML modificado.
        horas_a_restar (int): El número de horas a restar.
    """
    try:
        tree = ET.parse(archivo_entrada)
        root = tree.getroot()

        # Itera sobre todos los elementos 'programme'
        for programme in root.findall('programme'):
            start_str = programme.get('start')
            stop_str = programme.get('stop')

            if start_str and stop_str:
                # Formato de fecha y hora en el XML
                formato_fecha = "%Y%m%d%H%M%S %z"

                # Convierte las cadenas de texto a objetos datetime
                start_dt = datetime.strptime(start_str, formato_fecha)
                stop_dt = datetime.strptime(stop_str, formato_fecha)

                # Resta las horas necesarias
                nuevo_start_dt = start_dt - timedelta(hours=horas_a_restar)
                nuevo_stop_dt = stop_dt - timedelta(hours=horas_a_restar)

                # Vuelve a formatear las fechas al formato original
                programme.set('start', nuevo_start_dt.strftime(formato_fecha))
                programme.set('stop', nuevo_stop_dt.strftime(formato_fecha))

        # Guarda el XML modificado
        tree.write(archivo_salida, encoding='utf-8', xml_declaration=True)
        print(f"Archivo EPG ajustado y guardado en: {archivo_salida}")

    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")

# --- Instrucciones de uso ---
# 1. Guarda este código en un archivo con extensión .py (por ejemplo, "ajustar_epg.py").
# 2. Asegúrate de tener tu archivo XML en la misma carpeta (por ejemplo, "guia.xml").
# 3. Modifica los nombres de los archivos si es necesario.
# 4. Ejecuta el script desde la terminal: python ajustar_epg.py

if __name__ == '__main__':
    archivo_xml_original = 'guiaiptv.xml'  # Cambia esto por el nombre de tu archivo
    archivo_xml_corregido = 'guiaepg.xml' # Nombre del nuevo archivo
    horas_de_ajuste = 2  # Las horas que necesitas restar

    ajustar_hora_epg(archivo_xml_original, archivo_xml_corregido, horas_de_ajuste)