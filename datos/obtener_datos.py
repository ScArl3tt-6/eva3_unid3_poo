from datos.conexion import obtener_sesion

def obtener_todos(modelo):
    sesion = obtener_sesion()
    try:
        resultados = sesion.query(modelo).all()
        return resultados
    except Exception as e:
        print(f"Error al obtener: {e}")
        return []
    finally:
        sesion.close()