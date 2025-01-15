from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def init_db(config):
    db_config = config['database']
    connection_string = (f"mysql+pymysql://{db_config['user']}:{db_config['password']}"
                         f"@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    try:
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        raise Exception(f"Chyba při připojení k databázi: {e}")
