import uvicorn
from typing import List
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.models import (LoginRequest,
    SaldoResponse, Movimiento, MovimientosResponse,
    TarjetaResponse, DetallesTarjetaResponse,
    TarjetaSolicitud, TarjetaAprobacionResponse,
    PrestamoResponse, PaymentResponse, PaymentSolicitud,
    SimulacionResponse, SimulacionSolicitud, DetailRequest
)


from commons.querys import Querys
import data as t

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar CORS para desarrollo
origins = ["*"]  # Esto permitirá cualquier origen (solo para desarrollo)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar la conexión a la base de datos
q = Querys()

prefix_router = APIRouter(prefix="/elegion")

@prefix_router.get("/")
async def read_root():
    return FileResponse("static/index.html")

# Rutas de la API
@prefix_router.post("/login")
async def login(l: LoginRequest):
    canLog = q.login(l.user, l.passw)

    if canLog != -1:
        return canLog
    else:
        return 'Usuario invalido o password incorrecta'


@prefix_router.get("/getSaldo/{idCliente}")
async def get_saldo(idCliente: int):
    saldo = q.querySaldo(idCliente)
    return saldo

@prefix_router.get("/getMovimientos/{idCliente}")
async def get_movimientos(idCliente):
    movimientos = q.queryMovimientos(idCliente)
    return {"listaMovimientos": movimientos}

@prefix_router.get("/getTarjetas/{idCliente}")
async def get_tarjetas(idCliente):
    tarjetas = q.queryTarjetas(idCliente)
    return tarjetas

@prefix_router.get("/getDetallesTarjeta/{idCliente}")
async def get_detalles_tarjeta(idCliente, d: DetailRequest):
    detalles = q.queryDetallesTarjeta(d.idTarjeta, d.fecha)

    return detalles

@prefix_router.get("/getPrestamosActivos/{idCliente}")
async def get_prestamos_activos(idCliente):
    prestamos = q.queryPrestamos(idCliente)
    return prestamos

@prefix_router.get("/solicitarTarjeta/{idCliente}")
async def solicitar_tarjeta(idCliente):
    # Se va a mostrar la tarjeta con maximo limite disponible segun el score
    result = q.queryTarjetaAprobada(idCliente)

    return result

@prefix_router.post("/confirmarTarjeta/{idCliente}")
async def solicitar_tarjeta(idCliente, tarjetaAprobada: TarjetaSolicitud):
    alta = q.insertTarjeta(idCliente, tarjetaAprobada)
    return alta
@prefix_router.get("/simularPrestamo/{idCliente}")
def simularPrestamo(idCliente, simulacion_solicitud: SimulacionSolicitud):
    # Lógica para realizar la simulación (simulado)
    # Con el id de tipo prestamo, obtengo la tasa de interes
    tasa = q.queryTasaInteres(simulacion_solicitud.tipo)

    # Multiplico la tasa de interes por el monto
    incremento = (tasa/100) * simulacion_solicitud.monto
    montoTotal = incremento + simulacion_solicitud.monto

    # Lo divido por la cantidad de cuotas
    montoCuota = montoTotal / simulacion_solicitud.cuotas

    # Con el idCliente, obtengo el limite disponble para pedir
    limiteCliente = q.queryLimiteCliente(idCliente)
    print(limiteCliente)
    # Comparo el monto final con el limite disponible
    if limiteCliente > montoTotal:
        resultado = {
            "estado": "APROBADO",
            "montoDevolver": montoTotal,
            "montoCuota": montoCuota
        }
    else:
        resultado = {
            "estado": "DENEGADO"
        }

    # Devuelvo el resultado

    return resultado

@prefix_router.post("/confirmarPrestamo/{idCliente}")
async def confirmar_prestamo(idCliente, simulacion_solicitud: SimulacionSolicitud):
    simulacion = simularPrestamo(idCliente, simulacion_solicitud)
    print(simulacion)
    if simulacion["estado"] == "APROBADO":
        result = q.insertPrestamo(idCliente, simulacion_solicitud, simulacion)
    else:
        result = "DENEGADO"
    return result

@prefix_router.post("/doPayment/{idCliente}")
async def do_payment(idCliente, payment_solicitud: PaymentSolicitud):
    # Lógica para realizar el pago (simulado)
    return t.payment_resultado

app.include_router(prefix_router)