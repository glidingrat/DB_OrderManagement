from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import sessionmaker

def init_db(config):
    """Inicializuje připojení k databázi a ověřuje správnost všech parametrů."""
    db_config = config['database']
    connection_string = (f"mysql+pymysql://{db_config['user']}:{db_config['password']}"
                         f"@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    try:
        # Vytvoření databázového enginu
        engine = create_engine(connection_string)

        # Ověření připojení
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        # Vytvoření session factory
        Session = sessionmaker(bind=engine)
        return Session()
    except OperationalError as e:
        if "Access denied for user" in str(e):
            raise Exception("Config chyba: Nesprávný user nebo password.")
        elif "Unknown database" in str(e):
            raise Exception(f"Config chyba: Databáze '{db_config['database']}' neexistuje.")
        elif "Can't connect to MySQL server" in str(e):
            raise Exception("Config chyba: Nelze se připojit k serveru. Zkontrolujte host nebo port.")
        else:
            raise Exception(f"Config chyba: Chyba připojení: {e}")
    except ProgrammingError as e:
        raise Exception(f"Chyba v konfiguraci databáze: {e}")
    except Exception as e:
        raise Exception(f"Neočekávaná chyba při připojení k databázi: {e}")

