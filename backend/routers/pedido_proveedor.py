from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

import models
from database import get_db
from schemas.pedido_proveedor import (
    PedidoProveedorCreate,
    PedidoProveedorResponse
)

router = APIRouter(
    prefix="/pedidos-proveedor",
    tags=["Pedidos Proveedor"]
)

# ======================
# LISTAR
# ======================
@router.get("/", response_model=List[PedidoProveedorResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(models.PedidoProveedor).all()

# ======================
# OBTENER POR ID
# ======================
@router.get("/{id_abastecimiento}", response_model=PedidoProveedorResponse)
def obtener_pedido(id_abastecimiento: int, db: Session = Depends(get_db)):
    pedido = db.query(models.PedidoProveedor).filter(
        models.PedidoProveedor.id_abastecimiento == id_abastecimiento
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido proveedor no encontrado")

    return pedido

# ======================
# CREAR
# ======================
@router.post("/", response_model=PedidoProveedorResponse, status_code=201)
def crear_pedido(pedido: PedidoProveedorCreate, db: Session = Depends(get_db)):
    # Validación de fechas
    if pedido.fecha_entrega and pedido.fecha_entrega < pedido.fecha_pedido:
        raise HTTPException(
            status_code=400,
            detail="La fecha de entrega no puede ser menor a la fecha de pedido"
        )

    nuevo = models.PedidoProveedor(**pedido.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ======================
# ACTUALIZAR
# ======================
@router.put("/{id_abastecimiento}", response_model=PedidoProveedorResponse)
def actualizar_pedido(
    id_abastecimiento: int,
    pedido: PedidoProveedorCreate,
    db: Session = Depends(get_db)
):
    db_pedido = db.query(models.PedidoProveedor).filter(
        models.PedidoProveedor.id_abastecimiento == id_abastecimiento
    ).first()

    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido proveedor no encontrado")

    if pedido.fecha_entrega and pedido.fecha_entrega < pedido.fecha_pedido:
        raise HTTPException(
            status_code=400,
            detail="La fecha de entrega no puede ser menor a la fecha de pedido"
        )

    for key, value in pedido.model_dump().items():
        setattr(db_pedido, key, value)

    db.commit()
    db.refresh(db_pedido)
    return db_pedido

# ======================
# ELIMINAR
# ======================
@router.delete("/{id_abastecimiento}")
def eliminar_pedido(id_abastecimiento: int, db: Session = Depends(get_db)):
    pedido = db.query(models.PedidoProveedor).filter(
        models.PedidoProveedor.id_abastecimiento == id_abastecimiento
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido proveedor no encontrado")

    db.delete(pedido)
    db.commit()
    return {"mensaje": "Pedido proveedor eliminado"}
