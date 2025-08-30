import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

def ajustar_epg_finalisimo(archivo_entrada, archivo_salida):
    """
    Ajusta un archivo EPG XML aplicando reglas de corrección específicas
    basadas en la zona horaria indicada en el archivo original, que es errónea.
    """
    try:
        tree = ET.parse(archivo_entrada)
        root = tree.getroot()

        # Define la zona horaria correcta de destino (España en verano)
        ZONA_HORARIA_ES = timezone(timedelta(hours=2))

        # Itera sobre todos los elementos 'programme'
        for programme in root.findall('programme'):
            start_str = programme.get('start')
            stop_str = programme.get('stop')

            if start_str and stop_str:
                
                # --- LÓGICA DE CORRECCIÓN POR CASOS ---
                
                # Extrae la hora "ingenua" (sin zona) del string
                start_dt_naive = datetime.strptime(start_str.split(' ')[0], "%Y%m%d%H%M%S")
                stop_dt_naive = datetime.strptime(stop_str.split(' ')[0], "%Y%m%d%H%M%S")
                
                # Decide qué regla aplicar basándose en la etiqueta de zona horaria original
                if ' +0200' in start_str:
                    # REGLA 1 (+0200): La hora está 2 horas adelantada. Restamos 2h.
                    start_corregido = start_dt_naive - timedelta(hours=2)
                    stop_corregido = stop_dt_naive - timedelta(hours=2)
                
                elif ' +0100' in start_str:
                    # REGLA 2 (+0100): La hora está 3 horas atrasada. Sumamos 3h.
                    start_corregido = start_dt_naive + timedelta(hours=3)
                    stop_corregido = stop_dt_naive + timedelta(hours=3)

                else: # Esto se aplicará a +0000 y cualquier otro caso no especificado
                    # REGLA 3 (+0000, etc.): La hora es correcta, solo falta la zona.
                    start_corregido = start_dt_naive
                    stop_corregido = stop_dt_naive

                # Finalmente, a la hora ya corregida, le asignamos la zona horaria correcta de España
                nuevo_start_dt = start_corregido.replace(tzinfo=ZONA_HORARIA_ES)
                nuevo_stop_dt = stop_corregido.replace(tzinfo=ZONA_HORARIA_ES)

                # Formatea el resultado final y lo guarda
                formato_final = "%Y%m%d%H%M%S %z"
                programme.set('start', nuevo_start_dt.strftime(formato_final).replace(':', ''))
                programme.set('stop', nuevo_stop_dt.strftime(formato_final).replace(':', ''))

        tree.write(archivo_salida, encoding='utf-8', xml_declaration=True)
        print(f"Archivo EPG con corrección final guardado en: {archivo_salida}")

    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")

# --- Instrucciones de uso ---
if __name__ == '__main__':
    archivo_xml_original = 'guiaiptv.xml'
    archivo_xml_corregido = 'guiaepg.xml'
    
    ajustar_epg_finalisimo(archivo_xml_original, archivo_xml_corregido)