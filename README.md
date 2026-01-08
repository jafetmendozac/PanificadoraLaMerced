# BASE_DATOS_II_PROJECT

Proyecto para la asignatura Base de Datos II: backend (API), frontend (UI) y base de datos local.

## Contenido
- Descripción
- Tecnologías
- Requisitos
- Instalación rápida (Docker)
- Ejecución local (sin Docker)
- Inicializar la base de datos
- Estructura de carpetas
- Contribuir
- Licencia

## Descripción
Este repositorio contiene una aplicación completa con:
- Backend en FastAPI (carpeta `backend`) con routers para varias entidades (productos, pedidos, proveedores, etc.).
- Frontend (UI) en la carpeta `frontend/ui` para interacción con la API.
- Scripts y archivos de inicialización de la base de datos en la carpeta `database`.

El objetivo es gestionar inventarios, pedidos y reportes para un sistema de producción/ventas.

## Tecnologías
- Python 3.9+ (o 3.10+)
- FastAPI
- Uvicorn
- Streamlit (o frontend Python según implementación)
- SQLite (archivos en `database/`)
- Docker y Docker Compose (para levantar servicios fácilmente)

## Requisitos
- Docker & Docker Compose (recomendado)
- Python 3.9+ (para ejecución local)
- `pip` y `virtualenv` (opcional para entorno virtual)

## Instalación rápida (con Docker)
En la raíz del proyecto ejecute:

```bash
docker-compose up -d build

docker-compose up -d
```

Esto levantará los servicios configurados (API, y DB según `docker-compose.yml`).

Para detener y eliminar contenedores:

```bash
docker-compose down
```

Para eliminar los volumenes:

```bash
docker-compose down -v
```


```bash
python3 main.py
```
Esto cargara la interfaz pero necesitas dirigirte a la carpeta frontend


## Ejecución local (sin Docker)
1. Crear y activar entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias del backend:

```bash
pip install -r backend/requirements.txt
```

3. Instalar dependencias del frontend (si aplica):

```bash
pip install -r frontend/requirements.txt
```

4. Ejecutar el backend (ejemplo con uvicorn):

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

5. Ejecutar el frontend (si es Streamlit):

```bash
streamlit run frontend/ui/app.py --server.port 8501
```

Ajuste los comandos según la implementación real del `frontend`.

## Inicializar la base de datos
En `database/` se encuentran:
- `bd.sql`: dump o esquema de la base de datos.
- `init.sql`: scripts de inicialización.

Si usa Docker Compose, la inicialización puede ejecutarse automáticamente. Para inicializar manualmente con SQLite:

```bash
sqlite3 database/bd.sqlite < database/init.sql
```

(O ajuste el nombre del archivo según configuración).

## Estructura de carpetas (resumen)
- `backend/` - código de la API
  - `main.py` - punto de entrada de la API
  - `database.py` - conexión a BD
  - `models.py` - modelos ORM / Pydantic
  - `routers/` - endpoints por entidad
  - `schemas/` - esquemas Pydantic
  - `requirements.txt`
- `frontend/` - código del cliente/UI
  - `ui/` - apps/ventanas (Streamlit u otra)
  - `main.py` - lanzador del frontend
  - `requirements.txt`
- `database/` - archivos SQL (esquema, datos de ejemplo)
- `docker-compose.yml` - orquestación de servicios

## Endpoints y UI
La API expone routers organizados en `backend/routers/` (p. ej. `productos.py`, `pedidos_cliente.py`, `proveedor.py`, etc.).
- Para explorar la API cuando el backend está en ejecución, abra: `http://localhost:8000/docs` (Swagger UI).
- La UI del frontend usualmente está en `http://localhost:8501` (si usa Streamlit) o en la dirección configurada en `docker-compose.yml`.

## Contribuir
- Haga fork del repositorio y abra PRs.
- Antes de enviar cambios, ejecute linters y pruebas locales (si existen).
- Documente cambios en `README.md` y/o `CHANGELOG`.

## Notas y recomendaciones
- Revise `backend/requirements.txt` y `frontend/requirements.txt` antes de instalar.
- Asegúrese de que los puertos en `docker-compose.yml` no entren en conflicto con servicios locales.
- Si necesita ayuda para adaptar la ejecución local, comparta el error y ayudaré a ajustarlo.

## Licencia
Añada aquí la licencia del proyecto (p. ej. MIT) si aplica.

---

Archivo generado automáticamente: `README.md`. Ajuste contenido según detalles específicos del proyecto.
