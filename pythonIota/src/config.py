import json
import os


def load_config(file_path):
    """Načte konfigurační soubor a provede validaci."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Konfigurační soubor '{file_path}' nebyl nalezen.")

        if not os.path.isfile(file_path):
            raise Exception(f"'{file_path}' není platný soubor.")

        if os.path.getsize(file_path) == 0:
            raise Exception(f"Konfigurační soubor '{file_path}' je prázdný.")

        with open(file_path, 'r') as file:
            config = json.load(file)

        if not isinstance(config, dict):
            raise Exception("Konfigurační soubor musí být JSON objekt.")

        if "database" not in config:
            raise Exception("Konfigurační soubor musí obsahovat klíč 'database'.")

        db_config = config.get("database", {})
        required_keys = {"host", "port", "user", "password", "database"}
        missing_keys = required_keys - db_config.keys()
        if missing_keys:
            raise Exception(f"Chybějící klíče v sekci 'database': {', '.join(missing_keys)}.")

        return config

    except FileNotFoundError as e:
        raise Exception(f"Soubor nebyl nalezen: {e}")
    except PermissionError as e:
        raise Exception(f"Nelze otevřít soubor '{file_path}': {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Chyba při parsování JSON: {e}")
    except Exception as e:
        raise Exception(f"Nastala neočekávaná chyba: {e}")
