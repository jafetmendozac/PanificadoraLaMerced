from pydantic import BaseModel

class EstadoBase(BaseModel):
    descripcion_estado: str

class EstadoCreate(EstadoBase):
    pass

class EstadoResponse(EstadoBase):
    id_estado: int

    class Config:
        from_attributes = True
