from pydantic import BaseModel, Field

class CargoBase(BaseModel):
    cargo: str

class CargoCreate(CargoBase):
    pass

# class CargoUpdate(BaseModel):
#     cargo: str | None = None  # Para PUT/PATCH parcial

class CargoUpdate(BaseModel):
    cargo: str = Field(..., min_length=1, max_length=8)

class CargoResponse(CargoBase):
    id_cargo: int

    class Config:
        from_attributes = True


# from pydantic import BaseModel

# class CargoBase(BaseModel):
#     cargo: str

# class CargoCreate(CargoBase):
#     pass

# class CargoResponse(CargoBase):
#     id_cargo: int

#     class Config:
#         from_attributes = True



