from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
from database import get_db
from schemas.proveedor import ProveedorCreate, ProveedorResponse

router = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"]
)

@router.get("/", response_model=List[ProveedorResponse])
def listar_proveedores(db: Session = Depends(get_db)):
    return db.query(models.Proveedor).all()

@router.get("/{id_proveedor}", response_model=ProveedorResponse)
def obtener_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).filter(
        models.Proveedor.id_proveedor == id_proveedor
    ).first()

    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return proveedor

@router.post("/", response_model=ProveedorResponse, status_code=201)
def crear_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    nuevo = models.Proveedor(**proveedor.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_proveedor}", response_model=ProveedorResponse)
def actualizar_proveedor(id_proveedor: int, proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    db_proveedor = db.query(models.Proveedor).filter(
        models.Proveedor.id_proveedor == id_proveedor
    ).first()

    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    for key, value in proveedor.model_dump().items():
        setattr(db_proveedor, key, value)

    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

@router.delete("/{id_proveedor}")
def eliminar_proveedor(id_proveedor: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).filter(
        models.Proveedor.id_proveedor == id_proveedor
    ).first()

    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    db.delete(proveedor)
    db.commit()
    return {"mensaje": "Proveedor eliminado"}
