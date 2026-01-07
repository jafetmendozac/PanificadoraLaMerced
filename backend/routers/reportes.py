from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

# REPORTE: Ventas por día
# SELECT fecha, SUM(cantidad_producto) 
# FROM Pedido_cliente
# GROUP BY fecha;

@router.get("/ventas-por-dia")
def ventas_por_dia(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.PedidoCliente.fecha,
            func.sum(models.PedidoCliente.cantidad_producto).label("total_vendido")
        )
        .group_by(models.PedidoCliente.fecha)
        .order_by(models.PedidoCliente.fecha)
        .all()
    )

    return resultados



# 2️⃣ Ventas por mes
@router.get("/ventas-por-mes")
def ventas_por_mes(db: Session = Depends(get_db)):
    return (
        db.query(
            func.month(models.PedidoCliente.fecha).label("mes"),
            func.sum(models.PedidoCliente.cantidad_producto).label("total_vendido")
        )
        .group_by(func.month(models.PedidoCliente.fecha))
        .order_by("mes")
        .all()
    )



# 2️⃣ REPORTE: Productos más vendidos
# SELECT nombre_producto, SUM(cantidad)
# FROM Producto
# JOIN Detalle_Pedido
# GROUP BY nombre_producto;
@router.get("/productos-mas-vendidos")
def productos_mas_vendidos(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.Producto.nombre_producto,
            func.sum(models.DetallePedido.cantidad).label("total_vendido")
        )
        .join(models.PedidoCliente, models.Producto.id_pedido == models.PedidoCliente.id_pedido)
        .join(models.DetallePedido, models.DetallePedido.id_pedido == models.PedidoCliente.id_pedido)
        .group_by(models.Producto.nombre_producto)
        .order_by(func.sum(models.DetallePedido.cantidad).desc())
        .all()
    )

    return resultados



# 3️⃣ Pedidos por estado
# SELECT 
#     ep.descripcion_estado,
#     COUNT(*) AS total_pedidos
# FROM Pedido_cliente p
# JOIN Estado_Pedido ep ON p.id_estado = ep.id_estado
# GROUP BY ep.descripcion_estado;
# @router.get("/pedidos-por-estado")
def pedidos_por_estado(db: Session = Depends(get_db)):
    return (
        db.query(
            models.EstadoPedido.descripcion_estado,
            func.count(models.PedidoCliente.id_pedido).label("cantidad")
        )
        .join(models.PedidoCliente)
        .group_by(models.EstadoPedido.descripcion_estado)
        .all()
    )


# 4️⃣ Ingresos totales 💰
@router.get("/ingresos-totales")
def ingresos_totales(db: Session = Depends(get_db)):
    return (
        db.query(
            func.sum(
                models.DetallePedido.cantidad *
                models.DetallePedido.precio_unitario
            ).label("ingresos")
        )
        .scalar()
    )



# 5️⃣ Productos más vendidos
@router.get("/productos-mas-vendidos")
def productos_mas_vendidos(db: Session = Depends(get_db)):
    return (
        db.query(
            models.Producto.nombre_producto,
            func.sum(models.DetallePedido.cantidad).label("total_vendido")
        )
        .join(models.PedidoCliente, models.Producto.id_pedido == models.PedidoCliente.id_pedido)
        .join(models.DetallePedido, models.DetallePedido.id_pedido == models.PedidoCliente.id_pedido)
        .group_by(models.Producto.nombre_producto)
        .order_by(func.sum(models.DetallePedido.cantidad).desc())
        .all()
    )



# 6️⃣ Stock actual de productos
@router.get("/stock-productos")
def stock_productos(db: Session = Depends(get_db)):
    return (
        db.query(
            models.Producto.nombre_producto,
            models.Producto.cantidad_producto
        )
        .order_by(models.Producto.cantidad_producto)
        .all()
    )




# 3️⃣ REPORTE: Producción por empleado
# SELECT empleado, SUM(cantidad_producida)
# FROM Produccion
# GROUP BY empleado;

@router.get("/produccion-por-empleado")
def produccion_por_empleado(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.Empleado.nombre,
            models.Empleado.apellido_paterno,
            func.sum(models.Produccion.cantidad_producida).label("total_producido")
        )
        .join(models.Produccion)
        .group_by(models.Empleado.id_empleado)
        .order_by(func.sum(models.Produccion.cantidad_producida).desc())
        .all()
    )

    return resultados


# 8️⃣ Producción por día

@router.get("/produccion-por-dia")
def produccion_por_dia(db: Session = Depends(get_db)):
    return (
        db.query(
            models.Produccion.fecha,
            func.sum(models.Produccion.cantidad_producida).label("total_producido")
        )
        .group_by(models.Produccion.fecha)
        .order_by(models.Produccion.fecha)
        .all()
    )

# 9️⃣ Insumos más comprados
@router.get("/insumos-mas-comprados")
def insumos_mas_comprados(db: Session = Depends(get_db)):
    return (
        db.query(
            models.Insumos.nombre_insumo,
            func.sum(models.PedidoProveedor.cantidad).label("cantidad_total")
        )
        .join(models.PedidoProveedor)
        .group_by(models.Insumos.nombre_insumo)
        .order_by(func.sum(models.PedidoProveedor.cantidad).desc())
        .all()
    )



# 🔟 Compras por proveedor

@router.get("/compras-por-proveedor")
def compras_por_proveedor(db: Session = Depends(get_db)):
    return (
        db.query(
            models.Proveedor.nombre,
            models.Proveedor.apellido_paterno,
            func.sum(
                models.PedidoProveedor.cantidad *
                models.PedidoProveedor.precio_unitario
            ).label("total_compras")
        )
        .join(models.PedidoProveedor)
        .group_by(models.Proveedor.id_proveedor)
        .order_by(func.sum(
            models.PedidoProveedor.cantidad *
            models.PedidoProveedor.precio_unitario
        ).desc())
        .all()
    )


# 🟦 REPORTE 5 — Producción por turno
# SELECT 
#     turno,
#     SUM(cantidad_producida) AS total_producido
# FROM Produccion
# GROUP BY turno;


# 🟧 REPORTE 6 — Insumos con bajo stock (preventivo)
# SELECT 
#     nombre_insumo,
#     stock_minimo,
#     stock_maximo
# FROM Insumos
# WHERE stock_minimo <= stock_maximo;