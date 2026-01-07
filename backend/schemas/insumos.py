from pydantic import BaseModel

class InsumoBase(BaseModel):
    nombre_insumo: str
    unidad_medida: str
    stock_minimo: float
    stock_maximo: float

class InsumoCreate(InsumoBase):
    pass

class InsumoResponse(InsumoBase):
    id_insumo: int

    class Config:
        from_attributes = True
