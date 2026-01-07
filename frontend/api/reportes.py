from api.type import get

def reporte_ventas():
    return get("/reportes/ventas")

def reporte_produccion():
    return get("/reportes/produccion")

def reporte_empleados():
    return get("/reportes/empleados")
