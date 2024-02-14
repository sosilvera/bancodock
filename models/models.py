from pydantic import BaseModel
from typing import List

# Modelos Pydantic para las solicitudes y respuestas
class LoginRequest(BaseModel):
    user: str
    passw: str

class SaldoResponse(BaseModel):
    saldoPesos: float
    saldoDolar: float

class Movimiento(BaseModel):
    tipo: str
    descripcion: str
    monto: float

class MovimientoTC(BaseModel):
    tipo: str
    descripcion: str
    monto: float
    cuotaActual: int
    cuotasRestantes: int

class DetailRequest(BaseModel):
    idTarjeta: int
    fecha: str

class MovimientosResponse(BaseModel):
    listaMovimientos: List[Movimiento]

class TarjetaResponse(BaseModel):
    idTarjeta: int
    tipo: str
    digitos: int

class DetallesTarjetaResponse(BaseModel):
    cierreCiclo: str
    montoCicloActual: float
    movimientos: List[MovimientoTC]

class TarjetaSolicitud(BaseModel):
    idTipoTarjeta: int
    Descripcion: str
    MaximoLimite: int


class TarjetaAprobacionResponse(BaseModel):
    estado: str
    tipo: str
    limite: float

class PrestamoResponse(BaseModel):
    montoTotal: float
    montoProxCuota: float
    cantCuotas: int
    cuotaActual: int
    tipoPrestamo: str

class SimulacionSolicitud(BaseModel):
    monto: int
    cuotas: int
    tipo: int

class SimulacionResponse(BaseModel):
    idSimulacion: int
    estado: str
    cantCuotas: int
    montoADevolver: float
    valorCuota: float

class PaymentSolicitud(BaseModel):
    monto: float
    formaPago: str

class PaymentResponse(BaseModel):
    estado: str