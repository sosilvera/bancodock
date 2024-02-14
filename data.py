from datetime import date

# Datos simulados (deberías conectarlo con tu base de datos)
saldo_pesos = 1200.00
saldo_dolar = 20
movimientos = [
    {"tipo": "compra", "descripcion": "MercadoLibre", "monto": 20000.00},
    {"tipo": "transferencia", "descripcion": "Ximena Bazan", "monto": 20000.00},
    {"tipo": "ingreso", "descripcion": "Jose Perez", "monto": 20000.00}
]
tarjetas = [
    {"idTarjeta": 25, "tipo": "VISA Cred", "digitos": 430},
    {"idTarjeta": 26, "tipo": "VISA Deb", "digitos": 431},
    {"idTarjeta": 27, "tipo": "Master Cred", "digitos": 432},
]
detalles_tarjeta = {
    "numeroTarjeta": "4444",
    "cierreCiclo": str(date(2023, 12, 24)),
    "montoCicloActual": 120000,
    "movimientosPeriodo": [
        {"tipo":"COMPRA", "descripcion": "MercadoLibre", "monto": 300000, "cuotaActual": 2, "cutoasTotales": 6}
    ]
}
tarjeta_aprobacion = {"estado": "Aprobado", "tipo": "VISA Cred", "limite": 620000}
prestamos_activos = [
    {"montoTotal": 150000, "montoProxCuota": 4000, "cantCuotas": 24, "cuotaActual": 5, "tipoPrestamo": "Frances"}
]
simulacion_resultado = {"idSimulacion": 24, "estado": "Preaprobado", "cantCuotas": 12, "montoADevolver": 2000000, "valorCuota": 20000}
payment_resultado = {"estado": "OK"}
