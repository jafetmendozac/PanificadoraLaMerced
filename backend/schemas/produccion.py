from pydantic import BaseModel
from datetime import date

class ProduccionBase(BaseModel):
    fecha: date
    turno: bool = False
    cantidad_producida: int
    id_empleado: int
    id_pedido: int

class ProduccionCreate(ProduccionBase):
    pass

class ProduccionResponse(ProduccionBase):
    id_produccion: int

    class Config:
        from_attributes = True
