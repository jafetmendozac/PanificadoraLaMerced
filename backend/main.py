from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

from routers import clientes, productos, empleados, pedido_cliente, estado_pedido, pagos, cargos, detalle_pedido, insumos, proveedor, pedido_proveedor, produccion, reportes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Panificadora La Merced",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)  # 1
app.include_router(productos.router) # 2
app.include_router(empleados.router) # 3
app.include_router(pedido_cliente.router) # 4
app.include_router(detalle_pedido.router) # 5
app.include_router(estado_pedido.router) # 6
app.include_router(pagos.router) # 7
app.include_router(cargos.router) # 8
app.include_router(insumos.router) # 9
app.include_router(proveedor.router) # 10
app.include_router(pedido_proveedor.router) # 11
app.include_router(produccion.router) # 12

app.include_router(reportes.router) # Consultas especializadas


@app.get("/")
def root():
    return {"mensaje": "API Panificadora La Merced"}

@app.get("/health")
def health():
    return {"status": "ok"}