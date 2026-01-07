from sqlalchemy import Boolean, Column, Integer, String, Date, DECIMAL, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "Cliente"
    
    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    telefono_celular = Column(String(9))
    
    pedidos = relationship("PedidoCliente", back_populates="cliente")

class Pago(Base):
    __tablename__ = "Pago"
    
    id_pago = Column(Integer, primary_key=True, autoincrement=True)
    metodo_pago = Column(Boolean, nullable=False, default=False)
    
    pedidos = relationship("PedidoCliente", back_populates="pago")

class EstadoPedido(Base):
    __tablename__ = "Estado_Pedido"
    
    id_estado = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_estado = Column(String(10), unique=True, nullable=False)
    
    pedidos = relationship("PedidoCliente", back_populates="estado")

class PedidoCliente(Base):
    __tablename__ = "Pedido_cliente"
    
    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    tipo_entrega = Column(Boolean, nullable=False, default=False)
    tipo_pedido = Column(Boolean, nullable=False, default=False)
    cantidad_producto = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)
    id_cliente = Column(Integer, ForeignKey("Cliente.id_cliente"), nullable=False)
    id_pago = Column(Integer, ForeignKey("Pago.id_pago"), nullable=False)
    id_estado = Column(Integer, ForeignKey("Estado_Pedido.id_estado"), nullable=False, default=1)
    
    __table_args__ = (
        CheckConstraint('cantidad_producto > 0', name='check_cantidad_producto'),
    )
    
    cliente = relationship("Cliente", back_populates="pedidos")
    pago = relationship("Pago", back_populates="pedidos")
    estado = relationship("EstadoPedido", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido")
    productos = relationship("Producto", back_populates="pedido")
    producciones = relationship("Produccion", back_populates="pedido")

class DetallePedido(Base):
    __tablename__ = "Detalle_Pedido"
    
    id_detalle_pedido = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    id_pedido = Column(Integer, ForeignKey("Pedido_cliente.id_pedido"), nullable=False)
    
    __table_args__ = (
        CheckConstraint('cantidad > 0', name='check_detalle_cantidad'),
        CheckConstraint('precio_unitario >= 0', name='check_precio_unitario'),
    )
    
    pedido = relationship("PedidoCliente", back_populates="detalles")

class Proveedor(Base):
    __tablename__ = "Proveedor"
    
    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    telefono = Column(String(15))
    ruc = Column(String(11), unique=True, nullable=False)
    
    pedidos_proveedor = relationship("PedidoProveedor", back_populates="proveedor")

class Insumos(Base):
    __tablename__ = "Insumos"
    
    id_insumo = Column(Integer, primary_key=True, autoincrement=True)
    nombre_insumo = Column(String(100), nullable=False)
    unidad_medida = Column(String(20), nullable=False)
    stock_minimo = Column(DECIMAL(10, 3), nullable=False)
    stock_maximo = Column(DECIMAL(10, 3), nullable=False)
    
    __table_args__ = (
        CheckConstraint('stock_minimo >= 0', name='check_stock_minimo'),
        CheckConstraint('stock_maximo >= 0', name='check_stock_maximo'),
    )
    
    pedidos_proveedor = relationship("PedidoProveedor", back_populates="insumo")
    productos = relationship("Producto", back_populates="insumo")

class PedidoProveedor(Base):
    __tablename__ = "Pedido_proveedor"
    
    id_abastecimiento = Column(Integer, primary_key=True, autoincrement=True)
    fecha_pedido = Column(Date, nullable=False)
    fecha_entrega = Column(Date)
    cantidad = Column(DECIMAL(10, 3), nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    id_insumo = Column(Integer, ForeignKey("Insumos.id_insumo"), nullable=False)
    id_proveedor = Column(Integer, ForeignKey("Proveedor.id_proveedor"), nullable=False)
    
    __table_args__ = (
        CheckConstraint('cantidad > 0', name='check_pedido_cantidad'),
        CheckConstraint('precio_unitario >= 0', name='check_pedido_precio'),
    )
    
    proveedor = relationship("Proveedor", back_populates="pedidos_proveedor")
    insumo = relationship("Insumos", back_populates="pedidos_proveedor")

class Producto(Base):
    __tablename__ = "Producto"
    
    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(100), nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    cantidad_producto = Column(Integer, default=0)
    id_insumos = Column(Integer, ForeignKey("Insumos.id_insumo"))
    id_pedido = Column(Integer, ForeignKey("Pedido_cliente.id_pedido"))
    
    __table_args__ = (
        CheckConstraint('precio_unitario >= 0', name='check_producto_precio'),
        CheckConstraint('cantidad_producto >= 0', name='check_producto_cantidad'),
    )
    
    insumo = relationship("Insumos", back_populates="productos")
    pedido = relationship("PedidoCliente", back_populates="productos")

class Cargo(Base):
    __tablename__ = "Cargo"
    
    id_cargo = Column(Integer, primary_key=True, autoincrement=True)
    cargo = Column(String(8), nullable=False)
    
    empleados = relationship("Empleado", back_populates="cargo")

class Empleado(Base):
    __tablename__ = "Empleado"
    
    id_empleado = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    turno = Column(Boolean, nullable=False, default=False)
    id_cargo = Column(Integer, ForeignKey("Cargo.id_cargo"), nullable=False)
    
    cargo = relationship("Cargo", back_populates="empleados")
    producciones = relationship("Produccion", back_populates="empleado")

class Produccion(Base):
    __tablename__ = "Produccion"
    
    id_produccion = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    turno = Column(Boolean, nullable=False, default=False)
    cantidad_producida = Column(Integer, nullable=False)
    id_empleado = Column(Integer, ForeignKey("Empleado.id_empleado"), nullable=False)
    id_pedido = Column(Integer, ForeignKey("Pedido_cliente.id_pedido"), nullable=False)
    
    __table_args__ = (
        CheckConstraint('cantidad_producida > 0', name='check_cantidad_producida'),
    )
    
    empleado = relationship("Empleado", back_populates="producciones")
    pedido = relationship("PedidoCliente", back_populates="producciones")