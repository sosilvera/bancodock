from fastapi import APIRouter, HTTPException
from typing import List
from models.models import (LoginRequest,
    SaldoResponse, Movimiento, MovimientosResponse,
    TarjetaResponse, DetallesTarjetaResponse,
    TarjetaSolicitud, TarjetaAprobacionResponse,
    PrestamoResponse, PaymentResponse, PaymentSolicitud,
    SimulacionResponse, SimulacionSolicitud, DetailRequest
)
from commons.querys import Querys


# Configurar la conexión a la base de datos
q = Querys()

router = APIRouter(prefix="/elegion")

# Rutas de la API
@router.post("/login")
async def login(l: LoginRequest):
    canLog = q.login(l.user, l.passw)

    if canLog != -1:
        return {"userId": canLog}
    else:
        return 'Usuario invalido o password incorrecta'


@router.get("/getSaldo/{idCliente}")
async def get_saldo(idCliente: int):
    saldo = q.querySaldo(idCliente)
    return saldo

@router.get("/getMovimientos/{idCliente}")
async def get_movimientos(idCliente):
    movimientos = q.queryMovimientos(idCliente)
    return {"listaMovimientos": movimientos}

@router.get("/getTarjetas/{idCliente}")
async def get_tarjetas(idCliente):
    tarjetas = q.queryTarjetas(idCliente)
    return tarjetas

@router.get("/getDetallesTarjeta/{idCliente}")
async def get_detalles_tarjeta(idCliente, d: DetailRequest):
    detalles = q.queryDetallesTarjeta(d.idTarjeta, d.fecha)

    return detalles

@router.get("/getPrestamosActivos/{idCliente}")
async def get_prestamos_activos(idCliente):
    prestamos = q.queryPrestamos(idCliente)
    return prestamos

@router.get("/solicitarTarjeta/{idCliente}")
async def solicitar_tarjeta(idCliente):
    # Se va a mostrar la tarjeta con maximo limite disponible segun el score
    result = q.queryTarjetaAprobada(idCliente)

    return result

@router.post("/confirmarTarjeta/{idCliente}")
async def solicitar_tarjeta(idCliente, tarjetaAprobada: TarjetaSolicitud):
    alta = q.insertTarjeta(idCliente, tarjetaAprobada)
    return alta

@router.get("/simularPrestamo/{idCliente}")
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

@router.post("/confirmarPrestamo/{idCliente}")
async def confirmar_prestamo(idCliente, simulacion_solicitud: SimulacionSolicitud):
    simulacion = simularPrestamo(idCliente, simulacion_solicitud)
    print(simulacion)
    if simulacion["estado"] == "APROBADO":
        result = q.insertPrestamo(idCliente, simulacion_solicitud, simulacion)
    else:
        result = "DENEGADO"
    return result

@router.post("/doPayment/")
async def do_payment(payment_solicitud: PaymentSolicitud):
    ### Lógica para realizar el pago (simulado)
    idUsuario = payment_solicitud.idUsuario
    alias = payment_solicitud.alias
    monto = payment_solicitud.monto
    formaPago = payment_solicitud.formaPago
    moneda = payment_solicitud.moneda

    # Valido que el usuario tenga el monto
    tieneMonto = q.tieneMonto(idUsuario, monto, moneda)

    # Valido que el alias sea un cliente
    esCliente = q.esCliente(alias)
    
    if tieneMonto and esCliente["result"]:
        # Incremento el saldo del cliente destino
        print("Incremento saldo")
        q.incrementarSaldo(esCliente["idCliente"], monto, moneda)

        print("Decremento saldo")
        # Decremento el saldo del cliente actual
        q.restarSaldo(idUsuario, monto, moneda)

        print("Inserto movimiento")
        # Guardo un movimiento en la tabla de movimientos
        q.insertMovimiento(idUsuario, esCliente["idCliente"], alias, monto, moneda)
        
        return{"result": "OK"}
    elif not tieneMonto:
        return {"result": "Saldo insuficiente"}
    elif not esCliente:
        raise HTTPException(status_code=404, detail="Alias inexistente")