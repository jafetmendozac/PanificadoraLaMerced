from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
from database import get_db
from schemas.estado import EstadoCreate, EstadoResponse

router = APIRouter(
    prefix="/estados",
    tags=["Estados de Pedido"]
)

@router.get("/", response_model=List[EstadoResponse])
def listar_estados(db: Session = Depends(get_db)):
    return db.query(models.EstadoPedido).all()

@router.get("/{id_estado}", response_model=EstadoResponse)
def obtener_estado(id_estado: int, db: Session = Depends(get_db)):
    estado = db.query(models.EstadoPedido).filter(
        models.EstadoPedido.id_estado == id_estado
    ).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado

@router.post("/", response_model=EstadoResponse, status_code=201)
def crear_estado(estado: EstadoCreate, db: Session = Depends(get_db)):
    nuevo_estado = models.EstadoPedido(**estado.model_dump())
    db.add(nuevo_estado)
    db.commit()
    db.refresh(nuevo_estado)
    return nuevo_estado

@router.delete("/{id_estado}")
def eliminar_estado(id_estado: int, db: Session = Depends(get_db)):
    estado = db.query(models.EstadoPedido).filter(
        models.EstadoPedido.id_estado == id_estado
    ).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")

    db.delete(estado)
    db.commit()
    return {"mensaje": "Estado eliminado correctamente"}
