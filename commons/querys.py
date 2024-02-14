from schema.models import (Cliente, SaldoCliente, TipoMoneda, MovimientosCliente, 
    TipoMovimiento, TarjetasCliente,MovimientosTarjeta,PeriodosTarjeta, TiposTarjeta, 
    TiposPrestamo, PrestamosCliente, Base
)
from sqlalchemy import create_engine, func, and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
import commons.env as env
class Querys():
    def __init__(self):
        # Ruta relativa o absoluta de la base de datos SQLite3
        ruta_db = "BancoElegion.db"

        # Crear la conexión a la base de datos SQLite3
        engine = create_engine(f"sqlite:///{ruta_db}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        self.session = Session()

    def login(self, user, passw):
        result = self.session.query(Cliente.idCliente, Cliente.passw).filter_by(Usuario = user).first()

        if result:
            # Usuario encontrado, ahora verifica la contraseña
            if result.passw == passw:
                return result.idCliente
            else:
                return -1
        else:
            # Usuario no encontrado
            return -1


        return result[0].Limite        

    def querySaldo(self, id):
        result = self.session.query(SaldoCliente.Monto, SaldoCliente.idTipoMoneda).filter_by(idCliente = id).all()
        saldoPesos = 0
        saldoDolar = 0

        for i in result:
            if i[1] == 1:
                saldoPesos = i[0]
            elif i[1] == 2:
                saldoDolar = i[0]
    
        print("Saldo Pesos: ", saldoPesos)
        print("Saldo Dolar: ", saldoDolar)

        return {"saldoPesos": saldoPesos, "saldoDolar": saldoDolar}

    def queryMovimientos(self, id):
        try:
            # Realizar la consulta
            result = (
                self.session.query(MovimientosCliente.idMovimiento,TipoMovimiento.Descripcion, MovimientosCliente.Descripcion, MovimientosCliente.Monto)
                .join(TipoMovimiento, MovimientosCliente.idTipoMovimiento == TipoMovimiento.idTipoMovimiento)
                .filter(MovimientosCliente.idCliente == id)
                .all()
            )

            # Formatear el resultado
            formatted_result = [
                {"id": str(row[0]), "tipo": str(row[1]), "descripcion": str(row[2]), "monto": float(row[3])}
                for row in result
            ]

            return formatted_result

        except Exception as e:
            print(f"Error: {e}")
        return None

    def queryTarjetas(self, id):
        try:
            # Realizar la consulta
            result = (
                self.session.query(TarjetasCliente.idTarjeta,TiposTarjeta.Descripcion, TarjetasCliente.NumeroTarjeta)
                .join(TarjetasCliente, TiposTarjeta.idTipoTarjeta == TarjetasCliente.idTipoTarjeta)
                .filter(TarjetasCliente.idCliente == id)
                .all()
            )

            # Formatear el resultado
            formatted_result = [
                {"id": str(row[0]), "tipo": str(row[1]), "numero": str(row[2][-4:])}
                for row in result
            ]

            return formatted_result

        except Exception as e:
            print(f"Error: {e}")
        return None        

    def queryDetallesTarjeta(self, idTarjeta, fechaCierre):
        try:
            # Consulta 1
            periodoTarjeta = (
                self.session.query(PeriodosTarjeta.idPeriodo, PeriodosTarjeta.FechaCierre, PeriodosTarjeta.MontoConsumos)
                .filter(PeriodosTarjeta.FechaCierre == fechaCierre)
                .all()
            )

            # Consulta 2
            movimientos_tarjeta = (
                self.session.query(
                    MovimientosTarjeta.idTarjeta,
                    TipoMovimiento.Descripcion.label("tipo"),
                    MovimientosTarjeta.descripcion,
                    MovimientosTarjeta.Monto,
                    MovimientosTarjeta.cuotaActual,
                    MovimientosTarjeta.cuotasTotales
                )
                .join(TipoMovimiento, TipoMovimiento.idTipoMovimiento == MovimientosTarjeta.idTipoMovimiento)
                .filter(and_(MovimientosTarjeta.idTarjeta == idTarjeta, MovimientosTarjeta.idPeriodo == periodoTarjeta[0].idPeriodo))
                .all()
            )

            # Formatear el resultado
            result = {
                "FechaCierre": periodoTarjeta[0].FechaCierre, 
                "montoCicloActual": periodoTarjeta[0].MontoConsumos,
                "movimientosPeriodo": [
                    {
                        "TipoMovimiento": m.tipo,
                        "DescripcionMovimiento": m.descripcion,
                        "Monto": float(m.Monto),
                        "CuotaActual": m.cuotaActual,
                        "CuotasTotales": m.cuotasTotales,
                    }
                    for m in movimientos_tarjeta
                ],
            }

            return result

        except Exception as e:
            print(f"Error: {e}")
            return None

    def queryPrestamos(self, idCliente):
        try:
            # Consulta
            prestamo_cliente = (
                self.session.query(
                    PrestamosCliente.MontoSolicitado,
                    PrestamosCliente.MontoProximaCuota,
                    PrestamosCliente.CantidadCuotasPagas,
                    PrestamosCliente.CantidadCuotas,
                    PrestamosCliente.VencimientoProximaCuota,
                    TiposPrestamo.Descripcion
                )
                .join(TiposPrestamo, PrestamosCliente.idTipoPrestamo == TiposPrestamo.idTipoPrestamo)
                .filter(PrestamosCliente.idCliente == idCliente)
                .all()
            )

            # Formatear el resultado
            result = [
                {
                    "MontoSolicitado": float(pc.MontoSolicitado),
                    "MontoProximaCuota": float(pc.MontoProximaCuota),
                    "cuotaActual": pc.CantidadCuotasPagas + 1,
                    "CantidadCuotas": pc.CantidadCuotas,
                    "VencimientoProximaCuota": pc.VencimientoProximaCuota,
                    "DescripcionTipoPrestamo": pc.Descripcion,
                }
                for pc in prestamo_cliente
            ]

            return result

        except Exception as e:
            print(f"Error: {e}")
            return None

    def queryTasaInteres(self, idTipoPrestamo):
        result = self.session.query(TiposPrestamo.Interes).filter_by(idTipoPrestamo = idTipoPrestamo).all()

        return result[0].Interes

    def queryLimiteCliente(self, idCliente):
        result = self.session.query(Cliente.Limite).filter_by(idCliente = idCliente).all()
        return result[0].Limite

    # idPrestamo, idCliente, idTipoPrestamo, MontoSolicitado, MontoADevolver, CantidadCuotas, CantidadCuotasPagas, MontoProximaCuota, VencimientoProximaCuota
    def insertPrestamo(self, idCliente, simulacionReq, simulacionResp):
        maximo_id = (self.session.query(func.max(PrestamosCliente.idPrestamo)).scalar())

        idPrestamoNuevo = maximo_id + 1

        prestamo = PrestamosCliente(
            idPrestamo = idPrestamoNuevo,
            idCliente = idCliente,
            idTipoPrestamo = simulacionReq.tipo,
            MontoSolicitado = simulacionReq.monto,
            MontoADevolver = simulacionResp["montoDevolver"],
            CantidadCuotas = simulacionReq.cuotas,
            CantidadCuotasPagas = 0,
            MontoProximaCuota = int(simulacionResp["montoCuota"]),
            VencimientoProximaCuota = datetime.now()
        )

        self.session.add(prestamo)
        self.session.commit()
        return "OK"

    def queryScoreCliente(self, idCliente):
        result = self.session.query(Cliente.Score).filter_by(idCliente = idCliente).all()
        return result[0].Score

    def queryTarjetaAprobada(self, idCliente):
        scoreCliente = self.queryScoreCliente(idCliente)

        try:
            # Consulta
            tarjeta = (
                self.session.query(
                    TiposTarjeta.idTipoTarjeta,
                    TiposTarjeta.Descripcion,
                    func.max(TiposTarjeta.Limite)
                )
                .filter(TiposTarjeta.ScoreMinimo < scoreCliente)
                .all()
            )

            # Formatear el resultado
            result = {
                        "idTipoTarjeta": tarjeta[0].idTipoTarjeta,
                        "Descripcion": tarjeta[0].Descripcion,
                        "MaximoLimite": float(tarjeta[0][2])
                    }

            return result

        except Exception as e:
            print(f"Error: {e}")
            return None


    def insertTarjeta(self, idCliente, tarjetaResp):
        maximo_id = (self.session.query(func.max(TarjetasCliente.idTarjeta)).scalar())

        idPTarjetaNueva = maximo_id + 1
        numeroTarjeta = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        tarjeta = TarjetasCliente(
            idTarjeta = idPTarjetaNueva,
            idCliente = idCliente,
            NumeroTarjeta = numeroTarjeta,
            Limite = tarjetaResp.MaximoLimite,
            idTipoTarjeta = tarjetaResp.idTipoTarjeta
        )

        self.session.add(tarjeta)
        self.session.commit()
        return "OK"

    # Cierro la sesion de la base
    def sessionClose(self):
        self.session.close()


