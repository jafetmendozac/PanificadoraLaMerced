
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
from database import get_db
from schemas.cargo import CargoCreate, CargoResponse, CargoUpdate

router = APIRouter(
    prefix="/cargos",
    tags=["Cargos"]
)

# LISTAR TODOS
@router.get("/", response_model=List[CargoResponse])
def listar_cargos(db: Session = Depends(get_db)):
    return db.query(models.Cargo).all()

# OBTENER POR ID
@router.get("/{id_cargo}", response_model=CargoResponse)
def obtener_cargo(id_cargo: int, db: Session = Depends(get_db)):
    cargo = db.query(models.Cargo).filter(models.Cargo.id_cargo == id_cargo).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return cargo

# CREAR
@router.post("/", response_model=CargoResponse, status_code=201)
def crear_cargo(cargo: CargoCreate, db: Session = Depends(get_db)):
    nuevo_cargo = models.Cargo(**cargo.model_dump())
    db.add(nuevo_cargo)
    db.commit()
    db.refresh(nuevo_cargo)
    return nuevo_cargo

# ACTUALIZAR
@router.put("/{id_cargo}", response_model=CargoResponse)
def actualizar_cargo(id_cargo: int, cargo: CargoUpdate, db: Session = Depends(get_db)):
    existing_cargo = db.query(models.Cargo).filter(models.Cargo.id_cargo == id_cargo).first()
    if not existing_cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")

    # Actualiza y guarda
    existing_cargo.cargo = cargo.cargo
    db.commit()
    db.refresh(existing_cargo)
    return existing_cargo

# ELIMINAR
@router.delete("/{id_cargo}")
def eliminar_cargo(id_cargo: int, db: Session = Depends(get_db)):
    cargo = db.query(models.Cargo).filter(models.Cargo.id_cargo == id_cargo).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")

    db.delete(cargo)
    db.commit()
    return {"mensaje": "Cargo eliminado correctamente"}
