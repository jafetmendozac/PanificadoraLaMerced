from pydantic import BaseModel, Field

class DetallePedidoBase(BaseModel):
    cantidad: int = Field(..., gt=0)           # cantidad > 0
    precio_unitario: float = Field(..., ge=0) # precio >= 0
    id_pedido: int = Field(..., gt=0)      

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedidoUpdate(DetallePedidoBase):
    pass

class DetallePedidoResponse(DetallePedidoBase):
    id_detalle_pedido: int

    class Config:
        from_attributes = True
