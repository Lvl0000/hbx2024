import json
from transformers import pipeline
import time

# Cargar el modelo de traducción (alemán a español)
translator = pipeline("translation_de_to_es", model="Helsinki-NLP/opus-mt-de-es")

def traducir_json(file_path, output_path, chunk_size=100):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    translated_data = {}
    items = list(data.items())
    total = len(items)

    print(f"Total de elementos a traducir: {total}")
    for i in range(0, total, chunk_size):
        chunk = items[i:i + chunk_size]
        for key, text in chunk:
            try:
                # Traducir solo el segundo argumento del par clave-valor
                translated_text = translator(text)[0]["translation_text"]
                translated_data[key] = translated_text
                print(f"{i+1}/{total} - Traducido '{text}' a '{translated_text}'")
                time.sleep(0.1)  # Evita sobrecarga
            except Exception as e:
                print(f"Error en traducción para {key}: {e}")
                translated_data[key] = text  # Mantiene el original en caso de error

        # Guardar progreso en archivo para evitar pérdida de datos si se interrumpe
        with open(output_path, "w", encoding="utf-8") as out_file:
            json.dump(translated_data, out_file, ensure_ascii=False, indent=4)

    print("Traducción completada y guardada en", output_path)

# Uso del script
traducir_json("ExternalTexts.json", "salida.json")
