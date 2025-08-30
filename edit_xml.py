import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Importa la librería para manejar zonas horarias.
# zoneinfo es para Python 3.9+. Si usas una versión anterior, instala y usa pytz.
try:
    import zoneinfo
except ImportError:
    # Si zoneinfo no está disponible, intenta usar pytz.
    # Necesitarás instalarlo: pip install pytz
    from pytz import timezone as ZoneInfo
    print("Usando la librería 'pytz'. Asegúrate de que está instalada (`pip install pytz`).")


def ajustar_hora_epg_inteligente(archivo_entrada, archivo_salida):
    """
    Ajusta la hora en un archivo EPG XML de forma inteligente, aplicando
    diferentes reglas según la zona horaria de cada programa.
    """
    try:
        tree = ET.parse(archivo_entrada)
        root = tree.getroot()

        # Define la zona horaria de destino (España)
        ZONA_HORARIA_ES = zoneinfo.ZoneInfo("Europe/Madrid")

        # Itera sobre todos los elementos 'programme'
        for programme in root.findall('programme'):
            start_str = programme.get('start')
            stop_str = programme.get('stop')

            if start_str and stop_str:
                formato_fecha = "%Y%m%d%H%M%S %z"

                # Procesa el tiempo de inicio (start)
                start_dt_original = datetime.strptime(start_str, formato_fecha)
                
                # Procesa el tiempo de fin (stop)
                stop_dt_original = datetime.strptime(stop_str, formato_fecha)

                # --- LÓGICA INTELIGENTE ---
                # Revisa el offset (la diferencia horaria con UTC)
                offset_horas = start_dt_original.utcoffset().total_seconds() / 3600

                if offset_horas == 2.0:
                    # CASO 1: Es un canal +0200 (España). Corregimos el error de 2h.
                    start_dt_corregido = start_dt_original - timedelta(hours=2)
                    stop_dt_corregido = stop_dt_original - timedelta(hours=2)
                else:
                    # CASO 2: Es un canal de otra zona horaria.
                    # Asumimos que la hora es correcta y la convertimos a la hora española.
                    start_dt_corregido = start_dt_original.astimezone(ZONA_HORARIA_ES)
                    stop_dt_corregido = stop_dt_original.astimezone(ZONA_HORARIA_ES)
                
                # Vuelve a formatear las fechas al formato original (YYYYMMDDHHMMSS +ZZZZ)
                programme.set('start', start_dt_corregido.strftime(formato_fecha))
                programme.set('stop', stop_dt_corregido.strftime(formato_fecha))

        # Guarda el XML modificado
        tree.write(archivo_salida, encoding='utf-8', xml_declaration=True)
        print(f"Archivo EPG ajustado inteligentemente y guardado en: {archivo_salida}")

    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")

# --- Instrucciones de uso ---
# 1. Guarda este código en un archivo con extensión .py (ej. "ajustar_epg_auto.py").
# 2. Pon tu archivo XML original en la misma carpeta (ej. "guia.xml").
# 3. Ejecuta el script desde la terminal: python ajustar_epg_auto.py

if __name__ == '__main__':
    archivo_xml_original = 'guiaiptv.xml'  # Cambia esto por el nombre de tu archivo
    archivo_xml_corregido = 'guiaepg.xml' # Nombre del nuevo archivo

    ajustar_hora_epg_inteligente(archivo_xml_original, archivo_xml_corregido)