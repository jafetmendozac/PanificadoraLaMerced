from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
from database import get_db
from schemas.pago import PagoCreate, PagoResponse

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"]
)

@router.get("/", response_model=List[PagoResponse])
def listar_pagos(db: Session = Depends(get_db)):
    return db.query(models.Pago).all()

@router.get("/{id_pago}", response_model=PagoResponse)
def obtener_pago(id_pago: int, db: Session = Depends(get_db)):
    pago = db.query(models.Pago).filter(models.Pago.id_pago == id_pago).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

@router.post("/", response_model=PagoResponse, status_code=201)
def crear_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    nuevo_pago = models.Pago(**pago.model_dump())
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

@router.delete("/{id_pago}")
def eliminar_pago(id_pago: int, db: Session = Depends(get_db)):
    pago = db.query(models.Pago).filter(models.Pago.id_pago == id_pago).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    db.delete(pago)
    db.commit()
    return {"mensaje": "Pago eliminado correctamente"}
