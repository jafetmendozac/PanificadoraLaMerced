from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

# 1️⃣ Ventas por día
# 📊 Total de productos vendidos por fecha
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

    data = []
    for r in resultados:
        data.append({
            "fecha": r.fecha.strftime("%Y-%m-%d"),
            "total_vendido": int(r.total_vendido)
        })

    return data

# 3️⃣ Insumos más comprados

# 🏭 Compras a proveedores
@router.get("/insumos-mas-comprados")
def insumos_mas_comprados(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.Insumos.nombre_insumo,
            func.sum(models.PedidoProveedor.cantidad).label("cantidad_total")
        )
        .join(
            models.PedidoProveedor,
            models.Insumos.id_insumo == models.PedidoProveedor.id_insumo
        )
        .group_by(models.Insumos.nombre_insumo)
        .order_by(func.sum(models.PedidoProveedor.cantidad).desc())
        .all()
    )

    return [
        {
            "nombre_insumo": r.nombre_insumo,
            "cantidad_total": float(r.cantidad_total)
        }
        for r in resultados
    ]


# 4️⃣ Clientes frecuentes

# 👥 Clientes con más pedidos
@router.get("/clientes-frecuentes")
def clientes_frecuentes(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.Cliente.nombre,
            models.Cliente.apellido_paterno,
            func.count(models.PedidoCliente.id_pedido).label("total_pedidos")
        )
        .join(
            models.PedidoCliente,
            models.Cliente.id_cliente == models.PedidoCliente.id_cliente
        )
        .group_by(models.Cliente.id_cliente)
        .order_by(func.count(models.PedidoCliente.id_pedido).desc())
        .all()
    )

    return [
        {
            "nombre": r.nombre,
            "apellido_paterno": r.apellido_paterno,
            "total_pedidos": r.total_pedidos
        }
        for r in resultados
    ]



# 5️⃣ Producción por turno

# 🏭 Total producido por turno
@router.get("/produccion-por-turno")
def produccion_por_turno(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.Produccion.turno,
            func.sum(models.Produccion.cantidad_producida).label("total_producido")
        )
        .group_by(models.Produccion.turno)
        .all()
    )

    return [
        {
            "turno": r.turno,
            "total_producido": r.total_producido
        }
        for r in resultados
    ]
