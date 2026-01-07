from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import models
from database import get_db

router = APIRouter(
    prefix="/empleados",
    tags=["Empleados"]
)

class EmpleadoBase(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    turno: bool
    id_cargo: int

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoResponse(EmpleadoBase):
    id_empleado: int

    class Config:
        from_attributes = True

@router.get("/", response_model=List[EmpleadoResponse])
def obtener_empleados(db: Session = Depends(get_db)):
    return db.query(models.Empleado).all()

@router.get("/{id_empleado}", response_model=EmpleadoResponse)
def obtener_empleado(id_empleado: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@router.post("/", response_model=EmpleadoResponse, status_code=201)
def crear_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    db_empleado = models.Empleado(**empleado.model_dump())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

@router.put("/{id_empleado}", response_model=EmpleadoResponse)
def actualizar_empleado(id_empleado: int, empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    db_empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    for key, value in empleado.model_dump().items():
        setattr(db_empleado, key, value)

    db.commit()
    db.refresh(db_empleado)
    return db_empleado

@router.delete("/{id_empleado}")
def eliminar_empleado(id_empleado: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    db.delete(empleado)
    db.commit()
    return {"mensaje": "Empleado eliminado"}
