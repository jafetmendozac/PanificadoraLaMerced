from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
from database import get_db
from schemas.detalle_pedido import (
    DetallePedidoCreate,
    DetallePedidoResponse,
    DetallePedidoUpdate
)

router = APIRouter(
    prefix="/detalle-pedidos",
    tags=["Detalle Pedido"]
)

# ======================
# LISTAR DETALLES
# ======================
@router.get("/", response_model=List[DetallePedidoResponse])
def listar_detalles(db: Session = Depends(get_db)):
    return db.query(models.DetallePedido).all()

# ======================
# LISTAR POR PEDIDO
# ======================
@router.get("/pedido/{id_pedido}", response_model=List[DetallePedidoResponse])
def listar_por_pedido(id_pedido: int, db: Session = Depends(get_db)):
    pedido = db.query(models.PedidoCliente).filter(
        models.PedidoCliente.id_pedido == id_pedido
    ).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no existe")

    return db.query(models.DetallePedido).filter(
        models.DetallePedido.id_pedido == id_pedido
    ).all()

# ======================
# CREAR DETALLE
# ======================
@router.post("/", response_model=DetallePedidoResponse, status_code=201)
def crear_detalle(detalle: DetallePedidoCreate, db: Session = Depends(get_db)):
    pedido = db.query(models.PedidoCliente).filter(
        models.PedidoCliente.id_pedido == detalle.id_pedido
    ).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido no existe")

    nuevo_detalle = models.DetallePedido(**detalle.model_dump())
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)
    return nuevo_detalle

# ======================
# ACTUALIZAR DETALLE
# ======================
@router.put("/{id_detalle}", response_model=DetallePedidoResponse)
def actualizar_detalle(id_detalle: int, detalle: DetallePedidoUpdate, db: Session = Depends(get_db)):
    existing = db.query(models.DetallePedido).filter(
        models.DetallePedido.id_detalle_pedido == id_detalle
    ).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    pedido = db.query(models.PedidoCliente).filter(
        models.PedidoCliente.id_pedido == detalle.id_pedido
    ).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido no existe")

    # Actualizamos los campos
    existing.cantidad = detalle.cantidad
    existing.precio_unitario = detalle.precio_unitario
    existing.id_pedido = detalle.id_pedido

    db.commit()
    db.refresh(existing)
    return existing

# ======================
# ELIMINAR DETALLE
# ======================
@router.delete("/{id_detalle}")
def eliminar_detalle(id_detalle: int, db: Session = Depends(get_db)):
    detalle = db.query(models.DetallePedido).filter(
        models.DetallePedido.id_detalle_pedido == id_detalle
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    db.delete(detalle)
    db.commit()
    return {"mensaje": "Detalle eliminado"}


# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List

# import models
# from database import get_db
# from schemas.detalle_pedido import (
#     DetallePedidoCreate,
#     DetallePedidoResponse
# )

# router = APIRouter(
#     prefix="/detalle-pedidos",
#     tags=["Detalle Pedido"]
# )

# # ======================
# # LISTAR DETALLES
# # ======================
# @router.get("/", response_model=List[DetallePedidoResponse])
# def listar_detalles(db: Session = Depends(get_db)):
#     return db.query(models.DetallePedido).all()

# # ======================
# # LISTAR POR PEDIDO
# # ======================
# @router.get("/pedido/{id_pedido}", response_model=List[DetallePedidoResponse])
# def listar_por_pedido(id_pedido: int, db: Session = Depends(get_db)):
#     pedido = db.query(models.PedidoCliente).filter(
#         models.PedidoCliente.id_pedido == id_pedido
#     ).first()

#     if not pedido:
#         raise HTTPException(status_code=404, detail="Pedido no existe")

#     return db.query(models.DetallePedido).filter(
#         models.DetallePedido.id_pedido == id_pedido
#     ).all()

# # ======================
# # CREAR DETALLE
# # ======================
# @router.post("/", response_model=DetallePedidoResponse, status_code=201)
# def crear_detalle(detalle: DetallePedidoCreate, db: Session = Depends(get_db)):

#     pedido = db.query(models.PedidoCliente).filter(
#         models.PedidoCliente.id_pedido == detalle.id_pedido
#     ).first()

#     if not pedido:
#         raise HTTPException(status_code=400, detail="Pedido no existe")

#     nuevo_detalle = models.DetallePedido(**detalle.model_dump())
#     db.add(nuevo_detalle)
#     db.commit()
#     db.refresh(nuevo_detalle)
#     return nuevo_detalle

# # ======================
# # ELIMINAR DETALLE
# # ======================
# @router.delete("/{id_detalle}")
# def eliminar_detalle(id_detalle: int, db: Session = Depends(get_db)):
#     detalle = db.query(models.DetallePedido).filter(
#         models.DetallePedido.id_detalle_pedido == id_detalle
#     ).first()

#     if not detalle:
#         raise HTTPException(status_code=404, detail="Detalle no encontrado")

#     db.delete(detalle)
#     db.commit()
#     return {"mensaje": "Detalle eliminado"}
