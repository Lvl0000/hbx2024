import re
import time
from transformers import pipeline


translator = pipeline("translation_de_to_es", model="Helsinki-NLP/opus-mt-de-es")

def traducir_sql(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    translated_lines = []
    regex = re.compile(r"INSERT INTO `catalog_items` VALUES \((\d+, '.+?', \d+, \d+, \d+, \d+, '([^']+)', .+?)\);")

    print(f"Total de líneas a procesar: {len(lines)}")
    
    for i, line in enumerate(lines, start=1):
        
        match = regex.search(line)
        if match:
            try:
                original_text = match.group(2)
                translated_text = translator(original_text)[0]["translation_text"]
                
               
                translated_line = line.replace(f"'{original_text}'", f"'{translated_text}'")
                print(f"{i}/{len(lines)} - LevelBot '{original_text}' a '{translated_text}'")
                
                translated_lines.append(translated_line)
                time.sleep(0.1) 
            except Exception as e:
                print(f"Error en traducción para línea {i}: {e}")
                translated_lines.append(line)  
        else:
            translated_lines.append(line)  
    
   
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.writelines(translated_lines)
    
    print("Traducción completada y guardada en", output_path)


traducir_sql("traducir1.sql", "traducido1.sql")
