from pydantic import BaseModel
from datetime import date
from typing import Optional

class PedidoClienteBase(BaseModel):
    tipo_entrega: bool = False
    tipo_pedido: bool = False
    cantidad_producto: int
    fecha: date
    id_cliente: int
    id_pago: int
    id_estado: Optional[int] = 1

class PedidoClienteCreate(PedidoClienteBase):
    pass

class PedidoClienteResponse(PedidoClienteBase):
    id_pedido: int

    class Config:
        from_attributes = True
