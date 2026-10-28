from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

# Inicializamos la aplicación
app = FastAPI(
    title="API de Rendimiento - CIEL Backend",
    description="Servicio seguro de entrega de código y métricas de rendimiento protegido por API Keys.",
    version="1.0.0"
)

# Definimos el nombre del encabezado HTTP que usarán las apps cliente
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Base de datos simulada de API Keys permitidas (en producción esto iría en SQLite o PostgreSQL)
# Formato: {"llave_secreta": "Nombre de la Aplicación"}
VALID_API_KEYS = {
    "sk_live_alpha99887766": "Aplicación Cliente Uno",
    "sk_live_beta55443322": "Panel de Monitoreo Estelar"
}

def verificar_api_key(api_key: str = Security(api_key_header)):
    """Valida que la llave de acceso esté presente y sea legítima."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta la API Key en el encabezado (X-API-Key)."
        )
    
    if api_key in VALID_API_KEYS:
        return VALID_API_KEYS[api_key]
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acceso denegado: API Key inválida o no autorizada."
    )

# Modelo de respuesta con Pydantic para documentar la API automáticamente
class CodigoRendimientoResponse(BaseModel):
    status: str
    autorizado_para: str
    modulo: str
    codigo_fuente: str

@app.get("/", tags=["Estado"])
def read_root():
    return {"mensaje": "Servidor de API Keys activo y operando correctamente."}

@app.get("/api/v1/rendimiento", response_model=CodigoRendimientoResponse, tags=["Rendimiento"])
def obtener_codigo_rendimiento(nombre_cliente: str = Security(verificar_api_key)):
    """
    Endpoint protegido que entrega el código de rendimiento optimizado 
    solo a las aplicaciones que presenten una API Key válida.
    """
    script_rendimiento = """
import time

def ejecutar_benchmark_estelar():
    inicio = time.perf_counter()
    # Simulación de procesamiento de alto rendimiento
    total = sum(i * i for i in range(1000000))
    fin = time.perf_counter()
    return {"resultado": total, "tiempo_ejecucion_seg": fin - inicio}
    """.strip()

    return {
        "status": "success",
        "autorizado_para": nombre_cliente,
        "modulo": "Optimizador de Rendimiento V1",
        "codigo_fuente": script_rendimiento
    }