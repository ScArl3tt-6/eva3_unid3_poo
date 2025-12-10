import mysql.connector
import hashlib
import getpass
from prettytable import PrettyTable
from datetime import date
import sys

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="boutique_api",
        autocommit=False
    )

def registrar_usuario():
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("\n" + "="*40)
    print("REGISTRO DE USUARIO")
    print("="*40)
    
    usuario = input("Nombre de usuario: ")
    email = input("Email: ")
    contraseña = getpass.getpass("Contraseña: ")
    
    salt = "boutique_salt_2025"
    hash_contraseña = hashlib.sha256((contraseña + salt).encode()).hexdigest()
    
    try:
        cursor.execute(
            "INSERT INTO usuarios (username, email, contrasena, sal) VALUES (%s, %s, %s, %s)",
            (usuario, email, hash_contraseña, salt)
        )
        conn.commit()
        print("Usuario registrado (contraseña encriptada con SHA256)")
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def login():
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("\n" + "="*40)
    print("INICIO DE SESION")
    print("="*40)
    
    usuario = input("Usuario: ")
    contraseña = getpass.getpass("Contraseña: ")
    
    cursor.execute("SELECT contrasena, sal FROM usuarios WHERE username = %s", (usuario,))
    resultado = cursor.fetchone()
    
    if resultado:
        hash_guardado, salt = resultado
        hash_ingresado = hashlib.sha256((contraseña + salt).encode()).hexdigest()
        
        if hash_ingresado == hash_guardado:
            print("Login exitoso")
            cursor.close()
            conn.close()
            return True
        else:
            print("Contraseña incorrecta")
    else:
        print("Usuario no encontrado")
    
    cursor.close()
    conn.close()
    return False

def obtener_datos_api():
    print("\n" + "="*40)
    print("OBTENER DATOS ")
    print("="*40)

    productos_api = [
        {"id": 1, "nombre": "Labial Mate Rojo", "precio": 9990, "categoria": "Labios"},
        {"id": 2, "nombre": "Base Liquida", "precio": 14990, "categoria": "Rostro"},
        {"id": 3, "nombre": "Paleta Sombras", "precio": 19990, "categoria": "Ojos"},
        {"id": 4, "nombre": "Mascara Pestanias", "precio": 7990, "categoria": "Ojos"},
        {"id": 5, "nombre": "Iluminador", "precio": 12990, "categoria": "Rostro"}
    ]

    tabla = PrettyTable(["ID", "Producto", "Precio", "Categoria"])
    for p in productos_api:
        tabla.add_row([p['id'], p['nombre'], f"${p['precio']}", p['categoria']])
    print(tabla)

    conn = conectar_db()
    cursor = conn.cursor()

    for producto in productos_api:
        cursor.execute("""
            INSERT IGNORE INTO api_productos (api_id, nombre, precio, categoria) 
            VALUES (%s, %s, %s, %s)
        """, (producto['id'], producto['nombre'], producto['precio'], producto['categoria']))

    conn.commit()
    print(f"{len(productos_api)} productos guardados en BD")

    cursor.close()
    conn.close()

def crear_en_api():
    print("\n" + "="*40)
    print("CREAR NUEVO PRODUCTO (POST)")
    print("="*40)

    nombre = input("Nombre del producto: ")
    precio = float(input("Precio: "))
    categoria = input("Categoria: ")

    # Generar un nuevo id simple: tomar max api_id + 1 o usar un valor estático
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(api_id), 0) FROM api_productos")
    row = cursor.fetchone()
    nuevo_id = (row[0] or 0) + 1

    print(f"\nProducto creado en API simulada")
    print(f"ID: {nuevo_id}")
    print(f"Nombre: {nombre}")
    print(f"Precio: ${precio}")
    print(f"Categoria: {categoria}")

    cursor.execute(
        "INSERT INTO api_productos (api_id, nombre, precio, categoria) VALUES (%s, %s, %s, %s)",
        (nuevo_id, nombre, precio, categoria)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("Producto guardado en BD local")

def modificar_en_api():
    print("\n" + "="*40)
    print("MODIFICAR PRODUCTO (PUT)")
    print("="*40)
    
    id_producto = input("ID del producto a modificar: ")
    nuevo_nombre = input("Nuevo nombre: ")
    nuevo_precio = float(input("Nuevo precio: "))
    nueva_categoria = input("Nueva categoria: ")
    
    print(f"\nProducto {id_producto} modificado en API simulada")
    print(f"Nuevo nombre: {nuevo_nombre}")
    print(f"Nuevo precio: ${nuevo_precio}")
    print(f"Nueva categoria: {nueva_categoria}")
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE api_productos 
        SET nombre = %s, precio = %s, categoria = %s 
        WHERE api_id = %s
    """, (nuevo_nombre, nuevo_precio, nueva_categoria, id_producto))
    conn.commit()
    cursor.close()
    conn.close()
    print("Producto actualizado en BD local")

def eliminar_de_api():
    print("\n" + "="*40)
    print("ELIMINAR PRODUCTO (DELETE)")
    print("="*40)
    
    id_producto = input("ID del producto a eliminar: ")
    confirmacion = input(f"Seguro de eliminar producto {id_producto}? (s/n): ")
    
    if confirmacion.lower() == 's':
        print(f"\nProducto {id_producto} eliminado ")
        
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM api_productos WHERE api_id = %s", (id_producto,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Producto eliminado de BD local")
    else:
        print("Eliminacion cancelada")

def ver_datos_bd():
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("\n" + "="*40)
    print("USUARIOS REGISTRADOS")
    print("="*40)
    cursor.execute("SELECT id, username, email FROM usuarios")
    usuarios = cursor.fetchall()
    if usuarios:
        tabla = PrettyTable(["ID", "Usuario", "Email"])
        for u in usuarios:
            tabla.add_row(u)
        print(tabla)
    else:
        print("No hay usuarios registrados")
    
    print("\n" + "="*40)
    print("PRODUCTOS DE API EN BD")
    print("="*40)
    cursor.execute("SELECT id, api_id, nombre, precio, categoria FROM api_productos")
    productos = cursor.fetchall()
    if productos:
        tabla = PrettyTable(["ID DB", "ID API", "Producto", "Precio", "Categoria"])
        for p in productos:
            tabla.add_row(p)
        print(tabla)
    else:
        print("No hay productos en BD")
    
    cursor.close()
    conn.close()

def gestion_clientes():
    while True:
        print("\n" + "="*40)
        print("GESTION DE CLIENTES")
        print("="*40)
        print("1. Agregar cliente")
        print("2. Ver clientes")
        print("3. Buscar cliente")
        print("4. Volver")
        
        opcion = input("Opcion: ")
        
        if opcion == "1":
            agregar_cliente()
        elif opcion == "2":
            ver_clientes()
        elif opcion == "3":
            buscar_cliente()
        elif opcion == "4":
            break
        else:
            print("Opcion invalida")

def agregar_cliente():
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("\n--- AGREGAR CLIENTE ---")
    rut = input("RUT: ")
    nombre = input("Nombre: ")
    email = input("Email: ")
    telefono = input("Telefono: ")
    direccion = input("Direccion: ")
    
    try:
        cursor.execute("""
            INSERT INTO clientes (rut_cliente, nombre_cliente, correo_cliente, telefono_cliente, direccion_cliente)
            VALUES (%s, %s, %s, %s, %s)
        """, (rut, nombre, email, telefono, direccion))
        conn.commit()
        print("Cliente agregado correctamente")
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def ver_clientes():
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_cliente, rut_cliente, nombre_cliente, correo_cliente FROM clientes")
    clientes = cursor.fetchall()
    
    if clientes:
        tabla = PrettyTable(["ID", "RUT", "Nombre", "Email"])
        for c in clientes:
            tabla.add_row(c)
        print(tabla)
    else:
        print("No hay clientes registrados")
    
    cursor.close()
    conn.close()

def buscar_cliente():
    conn = conectar_db()
    cursor = conn.cursor()
    
    nombre_buscar = input("Nombre del cliente a buscar: ")
    
    cursor.execute("SELECT * FROM clientes WHERE nombre_cliente LIKE %s", (f"%{nombre_buscar}%",))
    clientes = cursor.fetchall()
    
    if clientes:
        tabla = PrettyTable(["ID", "RUT", "Nombre", "Email", "Telefono", "Direccion"])
        for c in clientes:
            tabla.add_row(c)
        print(tabla)
    else:
        print("Cliente no encontrado")
    
    cursor.close()
    conn.close()

def gestion_productos():
    while True:
        print("\n" + "="*40)
        print("GESTION DE PRODUCTOS")
        print("="*40)
        print("1. Agregar producto")
        print("2. Ver productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Volver")
        
        opcion = input("Opcion: ")
        
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            ver_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            break
        else:
            print("Opcion invalida")

def agregar_producto():
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("\n--- AGREGAR PRODUCTO ---")
    nombre = input("Nombre: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))
    descripcion = input("Descripcion: ")
    
    try:
        cursor.execute("""
            INSERT INTO productos (nombre_producto, precio_producto, stock_producto, descripcion_producto)
            VALUES (%s, %s, %s, %s)
        """, (nombre, precio, stock, descripcion))
        conn.commit()
        print("Producto agregado correctamente")
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def ver_productos():
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_producto, nombre_producto, precio_producto, stock_producto FROM productos")
    productos = cursor.fetchall()
    
    if productos:
        tabla = PrettyTable(["ID", "Producto", "Precio", "Stock"])
        for p in productos:
            tabla.add_row(p)
        print(tabla)
    else:
        print("No hay productos registrados")
    
    cursor.close()
    conn.close()

def actualizar_producto():
    conn = conectar_db()
    cursor = conn.cursor()
    
    id_producto = input("ID del producto a actualizar: ")
    
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    
    if not producto:
        print("Producto no encontrado")
        cursor.close()
        conn.close()
        return
    
    print(f"\nProducto actual: {producto[1]} - Precio: ${producto[2]} - Stock: {producto[3]}")
    
    nuevo_nombre = input("Nuevo nombre (dejar vacio para no cambiar): ")
    nuevo_precio = input("Nuevo precio (dejar vacio para no cambiar): ")
    nuevo_stock = input("Nuevo stock (dejar vacio para no cambiar): ")
    nueva_desc = input("Nueva descripcion (dejar vacio para no cambiar): ")
    
    actualizaciones = []
    valores = []
    
    if nuevo_nombre:
        actualizaciones.append("nombre_producto = %s")
        valores.append(nuevo_nombre)
    if nuevo_precio:
        actualizaciones.append("precio_producto = %s")
        valores.append(float(nuevo_precio))
    if nuevo_stock:
        actualizaciones.append("stock_producto = %s")
        valores.append(int(nuevo_stock))
    if nueva_desc:
        actualizaciones.append("descripcion_producto = %s")
        valores.append(nueva_desc)
    
    if actualizaciones:
        valores.append(id_producto)
        query = f"UPDATE productos SET {', '.join(actualizaciones)} WHERE id_producto = %s"
        cursor.execute(query, valores)
        conn.commit()
        print("Producto actualizado")
    else:
        print("No se realizaron cambios")
    
    cursor.close()
    conn.close()

def eliminar_producto():
    conn = conectar_db()
    cursor = conn.cursor()
    
    id_producto = input("ID del producto a eliminar: ")
    
    cursor.execute("SELECT nombre_producto FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    
    if not producto:
        print("Producto no encontrado")
        cursor.close()
        conn.close()
        return
    
    confirmacion = input(f"Seguro de eliminar '{producto[0]}'? (s/n): ")
    
    if confirmacion.lower() == 's':
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        conn.commit()
        print("Producto eliminado")
    else:
        print("Eliminacion cancelada")
    
    cursor.close()
    conn.close()

def menu():
    authenticated = False
    while True:
        print("\n" + "="*50)
        print("SISTEMA BOUTIQUE MAQUILLAJE - API SIMULADA")
        print("="*50)

        if not authenticated:
            # Solo mostrar opciones de autenticación hasta iniciar sesión
            print("1. Registrar usuario ")
            print("2. Login")
            print("0. Salir")

            opcion = input("\nOpcion: ")

            if opcion == "1":
                registrar_usuario()
            elif opcion == "2":
                if login():
                    authenticated = True
                    print("\n--- Acceso concedido al sistema ---")
            elif opcion == "0":
                print("Hasta luego!")
                break
            else:
                print("Opcion invalida. Debes iniciar sesión para ver el resto del menú.")
        else:
            # Usuario autenticado: mostrar el menú completo
            print("--- API y Datos ---")
            print("3. Obtener datos  (GET)")
            print("4. Crear en API (POST)")
            print("5. Modificar en API (PUT)")
            print("6. Eliminar en API (DELETE)")
            print("7. Ver datos guardados en BD")
            print("8. Gestion de Clientes")
            print("9. Gestion de Productos")
            print("0. Salir")

            opcion = input("\nOpcion: ")

            if opcion == "3":
                obtener_datos_api()
            elif opcion == "4":
                crear_en_api()
            elif opcion == "5":
                modificar_en_api()
            elif opcion == "6":
                eliminar_de_api()
            elif opcion == "7":
                ver_datos_bd()
            elif opcion == "8":
                gestion_clientes()
            elif opcion == "9":
                gestion_productos()
            elif opcion == "0":
                print("Hasta luego!")
                break
            else:
                print("Opcion invalida")

if __name__ == "__main__":
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            api_id INT NOT NULL,
            nombre VARCHAR(100),
            precio DECIMAL(10,2),
            categoria VARCHAR(50),
            fecha_guardado DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    
    menu() 