from datos.conexion import obtener_sesion
from typing import Iterable, Optional

try:
    from auxiliares.crypto import encrypt_object_fields
except Exception:
    # Si el módulo no está disponible, definimos un stub para no romper el flujo
    def encrypt_object_fields(obj, fields: Iterable[str]):
        return None


def insertar_objeto(objeto, encrypt_fields: Optional[Iterable[str]] = None):
    """Insert an object into the DB session.

    If `encrypt_fields` is provided (iterable of attribute names), the function
    will attempt to encrypt those fields on the object before inserting.
    """
    # Intentar encriptar campos si se solicita
    if encrypt_fields:
        try:
            encrypt_object_fields(objeto, encrypt_fields)
        except Exception as e:
            print(f"Advertencia: no se pudieron encriptar campos: {e}")

    sesion = obtener_sesion()
    try:
        sesion.add(objeto)
        sesion.commit()
        print("Objeto insertado correctamente.")
        return True
    except Exception as e:
        sesion.rollback()
        print(f"Error al insertar: {e}")
        return False
    finally:
        sesion.close()