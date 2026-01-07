from pydantic import BaseModel
from typing import Optional

class DetallePedidoBase(BaseModel):
    cantidad: int
    precio_unitario: float
    id_pedido: int

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedidoResponse(DetallePedidoBase):
    id_detalle_pedido: int

    class Config:
        from_attributes = True
