from pydantic import BaseModel
from typing import Optional

class ProveedorBase(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    telefono: Optional[str]
    ruc: str

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorResponse(ProveedorBase):
    id_proveedor: int

    class Config:
        from_attributes = True
