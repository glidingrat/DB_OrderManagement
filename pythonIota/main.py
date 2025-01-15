from src.config import load_config
from src.database import init_db
from src.ui import start_ui

def main():
    try:
        config = load_config("config.json")

        # Inicializace databáze
        session = init_db(config)

        start_ui(session)
    except KeyboardInterrupt:
        print("\nProgram byl ukončen.")
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    main()

