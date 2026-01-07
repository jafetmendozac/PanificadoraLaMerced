from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
from database import get_db
from schemas.produccion import ProduccionCreate, ProduccionResponse

router = APIRouter(
    prefix="/produccion",
    tags=["Producción"]
)

# ======================
# LISTAR PRODUCCIONES
# ======================
@router.get("/", response_model=List[ProduccionResponse])
def listar_producciones(db: Session = Depends(get_db)):
    return db.query(models.Produccion).all()

# ======================
# OBTENER POR ID
# ======================
@router.get("/{id_produccion}", response_model=ProduccionResponse)
def obtener_produccion(id_produccion: int, db: Session = Depends(get_db)):
    produccion = db.query(models.Produccion).filter(
        models.Produccion.id_produccion == id_produccion
    ).first()

    if not produccion:
        raise HTTPException(status_code=404, detail="Producción no encontrada")

    return produccion

# ======================
# CREAR PRODUCCIÓN
# ======================
@router.post("/", response_model=ProduccionResponse, status_code=201)
def crear_produccion(produccion: ProduccionCreate, db: Session = Depends(get_db)):
    # Validar empleado
    if not db.query(models.Empleado).filter(
        models.Empleado.id_empleado == produccion.id_empleado
    ).first():
        raise HTTPException(status_code=400, detail="Empleado no existe")

    # Validar pedido
    if not db.query(models.PedidoCliente).filter(
        models.PedidoCliente.id_pedido == produccion.id_pedido
    ).first():
        raise HTTPException(status_code=400, detail="Pedido no existe")

    nueva_produccion = models.Produccion(**produccion.model_dump())
    db.add(nueva_produccion)
    db.commit()
    db.refresh(nueva_produccion)

    return nueva_produccion

# ======================
# ELIMINAR PRODUCCIÓN
# ======================
@router.delete("/{id_produccion}")
def eliminar_produccion(id_produccion: int, db: Session = Depends(get_db)):
    produccion = db.query(models.Produccion).filter(
        models.Produccion.id_produccion == id_produccion
    ).first()

    if not produccion:
        raise HTTPException(status_code=404, detail="Producción no encontrada")

    db.delete(produccion)
    db.commit()
    return {"mensaje": "Producción eliminada"}
