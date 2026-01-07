from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
from database import get_db
from schemas.pedido_cliente import (
    PedidoClienteCreate,
    PedidoClienteResponse
)

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos Clientes"]
)

# ======================
# LISTAR PEDIDOS
# ======================
@router.get("/", response_model=List[PedidoClienteResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(models.PedidoCliente).all()

# ======================
# OBTENER POR ID
# ======================
@router.get("/{id_pedido}", response_model=PedidoClienteResponse)
def obtener_pedido(id_pedido: int, db: Session = Depends(get_db)):
    pedido = db.query(models.PedidoCliente).filter(
        models.PedidoCliente.id_pedido == id_pedido
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    return pedido

# ======================
# CREAR PEDIDO
# ======================
@router.post("/", response_model=PedidoClienteResponse, status_code=201)
def crear_pedido(pedido: PedidoClienteCreate, db: Session = Depends(get_db)):
    # Validaciones FK
    if not db.query(models.Cliente).filter(
        models.Cliente.id_cliente == pedido.id_cliente
    ).first():
        raise HTTPException(status_code=400, detail="Cliente no existe")

    if not db.query(models.Pago).filter(
        models.Pago.id_pago == pedido.id_pago
    ).first():
        raise HTTPException(status_code=400, detail="Método de pago no existe")

    if not db.query(models.EstadoPedido).filter(
        models.EstadoPedido.id_estado == pedido.id_estado
    ).first():
        raise HTTPException(status_code=400, detail="Estado no existe")

    nuevo_pedido = models.PedidoCliente(**pedido.model_dump())
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido

# ======================
# ACTUALIZAR ESTADO
# ======================
@router.put("/{id_pedido}/estado/{id_estado}")
def actualizar_estado(id_pedido: int, id_estado: int, db: Session = Depends(get_db)):
    pedido = db.query(models.PedidoCliente).filter(
        models.PedidoCliente.id_pedido == id_pedido
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    estado = db.query(models.EstadoPedido).filter(
        models.EstadoPedido.id_estado == id_estado
    ).first()

    if not estado:
        raise HTTPException(status_code=404, detail="Estado no existe")

    pedido.id_estado = id_estado
    db.commit()
    return {"mensaje": "Estado actualizado"}

# ======================
# ELIMINAR PEDIDO
# ======================
@router.delete("/{id_pedido}")
def eliminar_pedido(id_pedido: int, db: Session = Depends(get_db)):
    pedido = db.query(models.PedidoCliente).filter(
        models.PedidoCliente.id_pedido == id_pedido
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    db.delete(pedido)
    db.commit()
    return {"mensaje": "Pedido eliminado"}
