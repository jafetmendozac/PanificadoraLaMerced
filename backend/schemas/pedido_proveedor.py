from pydantic import BaseModel
from datetime import date
from typing import Optional

class PedidoProveedorBase(BaseModel):
    fecha_pedido: date
    fecha_entrega: Optional[date] = None
    cantidad: float
    precio_unitario: float
    id_insumo: int
    id_proveedor: int

class PedidoProveedorCreate(PedidoProveedorBase):
    pass

class PedidoProveedorResponse(PedidoProveedorBase):
    id_abastecimiento: int

    class Config:
        from_attributes = True
