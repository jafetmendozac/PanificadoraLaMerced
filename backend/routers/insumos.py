from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
from database import get_db
from schemas.insumos import InsumoCreate, InsumoResponse

router = APIRouter(
    prefix="/insumos",
    tags=["Insumos"]
)

# ======================
# LISTAR
# ======================
@router.get("/", response_model=List[InsumoResponse])
def listar_insumos(db: Session = Depends(get_db)):
    return db.query(models.Insumos).all()

# ======================
# OBTENER POR ID
# ======================
@router.get("/{id_insumo}", response_model=InsumoResponse)
def obtener_insumo(id_insumo: int, db: Session = Depends(get_db)):
    insumo = db.query(models.Insumos).filter(
        models.Insumos.id_insumo == id_insumo
    ).first()

    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")

    return insumo

# ======================
# CREAR
# ======================
@router.post("/", response_model=InsumoResponse, status_code=201)
def crear_insumo(insumo: InsumoCreate, db: Session = Depends(get_db)):
    nuevo = models.Insumos(**insumo.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ======================
# ACTUALIZAR
# ======================
@router.put("/{id_insumo}", response_model=InsumoResponse)
def actualizar_insumo(id_insumo: int, insumo: InsumoCreate, db: Session = Depends(get_db)):
    db_insumo = db.query(models.Insumos).filter(
        models.Insumos.id_insumo == id_insumo
    ).first()

    if not db_insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")

    for key, value in insumo.model_dump().items():
        setattr(db_insumo, key, value)

    db.commit()
    db.refresh(db_insumo)
    return db_insumo

# ======================
# ELIMINAR
# ======================
@router.delete("/{id_insumo}")
def eliminar_insumo(id_insumo: int, db: Session = Depends(get_db)):
    insumo = db.query(models.Insumos).filter(
        models.Insumos.id_insumo == id_insumo
    ).first()

    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")

    db.delete(insumo)
    db.commit()
    return {"mensaje": "Insumo eliminado"}
