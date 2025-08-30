import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

def ajustar_hora_epg_definitivo(archivo_entrada, archivo_salida):
    """
    Ajusta la hora en un archivo EPG XML aplicando una corrección universal.
    Esta versión asume que TODOS los tiempos en el archivo original están 2 horas
    adelantados respecto a la hora UTC real, ignorando la zona horaria
    especificada en el propio archivo.
    """
    try:
        tree = ET.parse(archivo_entrada)
        root = tree.getroot()

        # Itera sobre todos los elementos 'programme'
        for programme in root.findall('programme'):
            start_str = programme.get('start')
            stop_str = programme.get('stop')

            if start_str and stop_str:
                # --- LÓGICA DEFINITIVA ---
                
                # 1. Extrae solo la parte de la fecha y hora, ignorando la zona horaria del final.
                #    Ej: "20250830210000 +0000" -> "20250830210000"
                start_time_str_naive = start_str.split(' ')[0]
                stop_time_str_naive = stop_str.split(' ')[0]
                
                # 2. Convierte esa cadena a un objeto de tiempo, tratándolo como si fuera UTC.
                start_dt_erroneo_utc = datetime.strptime(start_time_str_naive, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
                stop_dt_erroneo_utc = datetime.strptime(stop_time_str_naive, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
                
                # 3. Resta 2 horas para obtener la hora UTC REAL.
                start_dt_real_utc = start_dt_erroneo_utc - timedelta(hours=2)
                stop_dt_real_utc = stop_dt_erroneo_utc - timedelta(hours=2)

                # 4. Formatea la fecha al formato final deseado.
                #    Python se encargará de poner el offset correcto (+0200 para verano en España).
                formato_final = "%Y%m%d%H%M%S %z"
                programme.set('start', start_dt_real_utc.strftime(formato_final))
                programme.set('stop', stop_dt_real_utc.strftime(formato_final))

        # Guarda el XML modificado
        tree.write(archivo_salida, encoding='utf-8', xml_declaration=True)
        print(f"Archivo EPG con corrección definitiva guardado en: {archivo_salida}")

    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")

# --- Instrucciones de uso ---
# 1. Guarda este código (ej. "ajustar_epg_definitivo.py").
# 2. Pon tu archivo XML original en la misma carpeta (ej. "guia.xml").
# 3. Ejecuta el script desde la terminal: python ajustar_epg_definitivo.py

if __name__ == '__main__':
    archivo_xml_original = 'guiaiptv.xml'
    archivo_xml_corregido = 'guiaepg.xml'

    ajustar_hora_epg_definitivo(archivo_xml_original, archivo_xml_corregido)