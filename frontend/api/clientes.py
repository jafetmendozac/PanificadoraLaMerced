from frontend.api.type import get, post, put, delete

def listar_clientes():
    return get("/clientes")

def obtener_cliente(id_cliente):
    return get(f"/clientes/{id_cliente}")

def crear_cliente(data):
    return post("/clientes", data)

def actualizar_cliente(id_cliente, data):
    return put(f"/clientes/{id_cliente}", data)

def eliminar_cliente(id_cliente):
    return delete(f"/clientes/{id_cliente}")
