import json
from transformers import pipeline
import time

# Cargar el modelo de traducción (alemán a español)
translator = pipeline("translation_de_to_es", model="Helsinki-NLP/opus-mt-de-es")

def traducir_json(file_path, output_path, chunk_size=100):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Hacer una copia del JSON original para preservar la estructura
    translated_data = data.copy()
    
    # Obtener los elementos 'furnitype' desde la estructura de 'roomitemtypes'
    items = data.get("roomitemtypes", {}).get("furnitype", [])
    total = len(items)

    print(f"Total de elementos a traducir: {total}")
    
    # Iterar en trozos (chunks) de datos para traducir
    for i in range(0, total, chunk_size):
        chunk = items[i:i + chunk_size]
        for item in chunk:
            try:
                # Traducir solo los campos 'name' y 'description'
                if 'name' in item:
                    original_name = item['name']
                    translated_name = translator(original_name)[0]["translation_text"]
                    item['name'] = translated_name
                    print(f"Traducido 'name' de '{original_name}' a '{translated_name}'")
                
                if 'description' in item:
                    original_description = item['description']
                    translated_description = translator(original_description)[0]["translation_text"]
                    item['description'] = translated_description
                    print(f"Traducido 'description' de '{original_description}' a '{translated_description}'")
                
                time.sleep(0.1)  # Evita sobrecarga
            except Exception as e:
                print(f"Error en traducción para el item {item['id']}: {e}")
                # Si ocurre un error, dejamos los valores originales
                item['name'] = item.get('name', '')
                item['description'] = item.get('description', '')

        # Guardar progreso en archivo para evitar pérdida de datos si se interrumpe
        with open(output_path, "w", encoding="utf-8") as out_file:
            json.dump(translated_data, out_file, ensure_ascii=False, indent=4)

    print("Traducción completada y guardada en", output_path)

# Uso del script
traducir_json("FurnitureData.json", "salida.json")

