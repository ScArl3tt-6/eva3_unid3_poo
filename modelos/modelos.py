from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# ========== USUARIOS SISTEMA ==========
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(15), nullable=False)
    email = Column(String(255), nullable=False)
    contrasena = Column(String(255), nullable=False)
    sal = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=func.now())

# ========== DATOS API ==========
class ApiProducto(Base):
    __tablename__ = 'api_productos'
    id = Column(Integer, primary_key=True)
    api_id = Column(Integer, nullable=False)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String(50))
    fecha_guardado = Column(DateTime, default=func.now())

class ApiPost(Base):
    __tablename__ = 'api_posts'
    id = Column(Integer, primary_key=True)
    api_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())

# ========== BOUTIQUE MAQUILLAJE ==========
class Cliente(Base):
    __tablename__ = 'clientes'
    id_cliente = Column(Integer, primary_key=True)
    rut_cliente = Column(String(15), nullable=False)
    nombre_cliente = Column(String(100), nullable=False)
    correo_cliente = Column(String(100), nullable=False)
    telefono_cliente = Column(String(20))
    direccion_cliente = Column(String(150))

class Producto(Base):
    __tablename__ = 'productos'
    id_producto = Column(Integer, primary_key=True)
    nombre_producto = Column(String(100), nullable=False)
    precio_producto = Column(Float, nullable=False)
    stock_producto = Column(Integer, nullable=False)
    descripcion_producto = Column(String(200))

class Pedido(Base):
    __tablename__ = 'pedidos'
    id_pedido = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    nombre_cliente = Column(String(255))
    fecha_pedido = Column(Date)
    estado_pedido = Column(String(50))
    total_pedido = Column(Float)
    metodo_pago = Column(String(50))

class DetallePedido(Base):
    __tablename__ = 'detalles_pedido'
    id_detalle = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'))
    id_producto = Column(Integer, ForeignKey('productos.id_producto'))
    cantidad_pedido = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal_pedido = Column(Float, nullable=False)

class Pago(Base):
    __tablename__ = 'pagos'
    id_pago = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'))
    monto_pago = Column(Float, nullable=False)
    fecha_pago = Column(Date, nullable=False)
    estado_pago = Column(String(50))
    metodo_pago = Column(String(50))