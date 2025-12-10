from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auxiliares import usuario_db, servidor_db, puerto_db, nombre_db

url_db = f"mysql+mysqlconnector://{usuario_db}@{servidor_db}:{puerto_db}/{nombre_db}"
motor_db = create_engine(url_db)
Session = sessionmaker(bind=motor_db)

def obtener_sesion():
    return Session()