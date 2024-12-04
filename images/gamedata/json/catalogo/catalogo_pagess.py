# traducir_argumento_20.py
import re
import time
from transformers import pipeline

# Configuración del traductor
translator = pipeline("translation_de_to_es", model="Helsinki-NLP/opus-mt-de-es")

# Función para escapar comillas simples para SQL
def escape_sql_text(text):
    return text.replace("'", "''")

# Función para traducir solo el argumento 20
def traducir_argumento_20(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    translated_lines = []
    
    # Expresión regular corregida para manejar correctamente los patrones SQL
    regex = re.compile(r"INSERT INTO `catalog_pages` VALUES \((\d+, \d+, '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '[^']*', '([^']*)', '[^']*', '[^']*'\);")

    for i, line in enumerate(lines, start=1):
        match = regex.search(line)
        
        if match:
            # Extraemos el valor del argumento 20
            original_text_20 = match.group(1) or ""
            try:
                if original_text_20 and original_text_20 != "NULL":  # Solo traducir si no es NULL
                    translated_text_20 = escape_sql_text(translator(original_text_20)[0]["translation_text"])
                    line = line.replace(f"'{original_text_20}'", f"'{translated_text_20}'")
                    print(f"{i}/{len(lines)} - Traducción '{original_text_20}' a '{translated_text_20}'")
                elif original_text_20 == "NULL":  # Si es NULL, no traducir, solo conservar
                    line = line.replace("'NULL'", "NULL")
                translated_lines.append(line)
                time.sleep(0.1)
            except Exception as e:
                print(f"Error en traducción para línea {i}: {e}")
                translated_lines.append(line)
        else:
            translated_lines.append(line)
    
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.writelines(translated_lines)
    
    print("Traducción completada y guardada en", output_path)


# Ejecutar la función con los archivos de entrada y salida
traducir_argumento_20("traducido21.sql", "traducido23.sql")
