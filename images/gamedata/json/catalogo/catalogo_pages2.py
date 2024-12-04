import re
import time
from transformers import pipeline

# Configuración del traductor
translator = pipeline("translation_de_to_es", model="Helsinki-NLP/opus-mt-de-es")

def traducir_sql(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    translated_lines = []
    
    # Expresión regular adaptada para la tabla 'catalog_pages' y el campo 20
    regex = re.compile(r"INSERT INTO `catalog_pages` VALUES \((.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,'(.*?)'.*?)\);")

    print(f"Total de líneas a procesar: {len(lines)}")
    
    for i, line in enumerate(lines, start=1):
        # Solo procesamos las primeras 20 líneas para depuración
        if i > 20:
            break

        match = regex.search(line)
        if match:
            try:
                # Extraemos el texto del campo 20 (en alemán)
                original_text = match.group(2)
                
                # Añadir un mensaje de depuración con el tiempo antes de traducir
                print(f"Traduciendo línea {i}: {original_text[:30]}...")  # Mostrar los primeros 30 caracteres

                # Traducimos el texto capturado
                translated_text = translator(original_text)[0]["translation_text"]
                
                # Añadir el texto traducido en la línea SQL
                translated_line = line.replace(f"'{original_text}'", f"'{translated_text}'")
                print(f"{i}/{len(lines)} - Traducción '{original_text}' a '{translated_text}'")
                
                translated_lines.append(translated_line)
                time.sleep(1)  # Aumentamos el tiempo de espera a 1 segundo para evitar sobrecargar la API
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
traducir_sql("traducido21.sql", "traducido23.sql")
