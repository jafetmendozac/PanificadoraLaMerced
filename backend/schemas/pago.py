from pydantic import BaseModel

class PagoBase(BaseModel):
    metodo_pago: bool

class PagoCreate(PagoBase):
    pass

class PagoResponse(PagoBase):
    id_pago: int

    class Config:
        from_attributes = True
