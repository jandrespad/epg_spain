# main.py

import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from io import StringIO

def adjust_epg_timezone():
    load_dotenv()

    epg_url = os.getenv('EPG_URL')
    output_filename = os.getenv('OUTPUT_FILENAME')
    timezone_offset_hours = int(os.getenv('TIMEZONE_OFFSET_HOURS', 2))

    if not epg_url or not output_filename:
        print("Error: Asegúrate de que las variables EPG_URL y OUTPUT_FILENAME están definidas en el fichero .env")
        return

    try:
        print(f"Descargando EPG desde: {epg_url}")
        response = requests.get(epg_url)
        response.raise_for_status()
        xml_content = response.text

        tree = ET.parse(StringIO(xml_content))
        root = tree.getroot()

        target_timezone = timezone(timedelta(hours=timezone_offset_hours))

        for programme in root.findall('programme'):
            start_str = programme.get('start')
            stop_str = programme.get('stop')

            if not start_str or not stop_str:
                continue

            try:
                start_naive_dt = datetime.strptime(start_str.split(' ')[0], "%Y%m%d%H%M%S")
                stop_naive_dt = datetime.strptime(stop_str.split(' ')[0], "%Y%m%d%H%M%S")

                corrected_start = start_naive_dt
                corrected_stop = stop_naive_dt

                if ' +0200' in start_str:
                    corrected_start = start_naive_dt - timedelta(hours=2)
                    corrected_stop = stop_naive_dt - timedelta(hours=2)
                elif ' +0100' in start_str:
                    corrected_start = start_naive_dt + timedelta(hours=3)
                    corrected_stop = stop_naive_dt + timedelta(hours=3)

                new_start_dt = corrected_start.replace(tzinfo=target_timezone)
                new_stop_dt = corrected_stop.replace(tzinfo=target_timezone)

                output_format = "%Y%m%d%H%M%S %z"
                programme.set('start', new_start_dt.strftime(output_format).replace(':', ''))
                programme.set('stop', new_stop_dt.strftime(output_format).replace(':', ''))
            
            except (ValueError, IndexError) as e:
                print(f"Aviso: Omitiendo un programa debido a un formato de fecha inesperado en '{start_str}'. Error: {e}")
                continue


        tree.write(output_filename, encoding='utf-8', xml_declaration=True)
        print(f"Proceso completado. El fichero EPG corregido se ha guardado como: {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el fichero: {e}")
    except ET.ParseError as e:
        print(f"Error al procesar el fichero XML: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")

if __name__ == '__main__':
    adjust_epg_timezone()