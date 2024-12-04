import re
import time
from transformers import pipeline

translator = pipeline("translation_de_to_es", model="Helsinki-NLP/opus-mt-de-es")

def traducir_sql(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    translated_lines = []
    # Expresión regular modificada para capturar cualquier texto en las posiciones 5, 15 y 20
    regex = re.compile(
        r"INSERT INTO `catalog_pages` VALUES \((\d+, \d+, '[^']*', '[^']*', '([^']*)'(?:, [^,]*){9}, '([^']*)'(?:, [^,]*){4}, '([^']*)'.*?)\);"
    )

    print(f"Total de líneas a procesar: {len(lines)}")
    
    for i, line in enumerate(lines, start=1):
        match = regex.search(line)
        if match:
            try:
                # Capturamos los textos en las posiciones 5, 15 y 20 si existen
                original_text_5 = match.group(2) or ""
                original_text_15 = match.group(3) or ""
                original_text_20 = match.group(4) or ""

                # Traducimos los textos no vacíos
                translated_text_5 = translator(original_text_5)[0]["translation_text"] if original_text_5 else ""
                translated_text_15 = translator(original_text_15)[0]["translation_text"] if original_text_15 else ""
                translated_text_20 = translator(original_text_20)[0]["translation_text"] if original_text_20 else ""

                # Reemplazamos en la línea original con los textos traducidos
                translated_line = line
                if original_text_5:
                    translated_line = translated_line.replace(f"'{original_text_5}'", f"'{translated_text_5}'")
                    print(f"{i}/{len(lines)} - Traducción '{original_text_5}' a '{translated_text_5}'")

                if original_text_15:
                    translated_line = translated_line.replace(f"'{original_text_15}'", f"'{translated_text_15}'")
                    print(f"{i}/{len(lines)} - Traducción '{original_text_15}' a '{translated_text_15}'")

                if original_text_20:
                    translated_line = translated_line.replace(f"'{original_text_20}'", f"'{translated_text_20}'")
                    print(f"{i}/{len(lines)} - Traducción '{original_text_20}' a '{translated_text_20}'")

                translated_lines.append(translated_line)
                time.sleep(0.1)  # Pausa para evitar exceso de consultas
            except Exception as e:
                print(f"Error en traducción para línea {i}: {e}")
                translated_lines.append(line)  # Línea sin cambios si hay error
        else:
            translated_lines.append(line)  # Si no coincide, agregar línea sin cambios
    
    # Guardamos las líneas traducidas en el archivo de salida
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.writelines(translated_lines)
    
    print("Traducción completada y guardada en", output_path)

# Ejecutamos la función con los archivos de entrada y salida
traducir_sql("traducir2.sql", "traducido2.sql")
