import json

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"Konfigurační soubor '{file_path}' nebyl nalezen.")
    except json.JSONDecodeError as e:
        raise Exception(f"Chyba při parsování konfiguračního souboru: {e}")
