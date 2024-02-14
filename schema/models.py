from sqlalchemy import Boolean, Column , ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# db = SQLAlchemy()

# El que es llamado, define las relaciones, entonces:
# Cliente tiene que definir relaciones con:
# SaldoCliente, TarjetasCliente, MovimientosCliente y PrestamoCliente
class Cliente(Base):
    __tablename__ = 'Cliente'
    idCliente = Column(Integer, primary_key=True)
    Nombre = Column(String(255))
    DNI = Column(String(20))
    Direccion = Column(String(255))
    Usuario = Column(String(255))
    passw = Column(String(255))
    Limite = Column(Integer)
    Score = Column(Integer)
    SaldoCliente = relationship('SaldoCliente', backref="Cliente", overlaps='Cliente,SaldoCliente')
    MovimientosCliente = relationship('MovimientosCliente', backref="Cliente", overlaps='Cliente,MovimientosCliente')
    PrestamosCliente = relationship('PrestamosCliente', backref="Cliente", overlaps='Cliente,PrestamosCliente')
    TarjetasCliente = relationship('TarjetasCliente', backref="Cliente", overlaps='Cliente,TarjetasCliente')

class SaldoCliente(Base):
    __tablename__ = 'SaldoCliente'
    idSaldo = Column(Integer, primary_key=True)
    idCliente = Column(Integer, ForeignKey('Cliente.idCliente'))
    Monto = Column(DECIMAL(10, 2))
    idTipoMoneda = Column(Integer, ForeignKey('TipoMoneda.idTipoMoneda'))
    

class TipoMoneda(Base):
    __tablename__ = 'TipoMoneda'
    idTipoMoneda = Column(Integer, primary_key=True)
    Descripcion = Column(String(255))
    Logo = Column(String(10))
    ValorPesos = Column(DECIMAL(10, 2))
    SaldoCliente = relationship('SaldoCliente', backref="TipoMoneda", overlaps='TipoMoneda,SaldoCliente')

class MovimientosCliente(Base):
    __tablename__ = 'MovimientosCliente'
    idMovimiento = Column(Integer, primary_key=True)
    idCliente = Column(Integer, ForeignKey('Cliente.idCliente'))
    idTipoMovimiento = Column(String(50), ForeignKey('TipoMovimiento.idTipoMovimiento'))
    Descripcion = Column(String(50))
    Monto = Column(DECIMAL(10, 2))

class TipoMovimiento(Base):
    __tablename__ = 'TipoMovimiento'
    idTipoMovimiento = Column(Integer, primary_key=True)
    Descripcion = Column(String(255))
    Operacion = Column(String(50))
    MovimientosCliente = relationship('MovimientosCliente', backref="TipoMovimiento", overlaps='TipoMovimiento,MovimientosCliente')
    MovimientosTarjeta = relationship('MovimientosTarjeta', backref="TipoMovimiento", overlaps='TipoMovimiento,MovimientosTarjeta')

class TarjetasCliente(Base):
    __tablename__ = 'TarjetasCliente'
    idTarjeta = Column(Integer, primary_key=True)
    idCliente = Column(Integer, ForeignKey('Cliente.idCliente'))
    idTipoTarjeta = Column(Integer, ForeignKey('TiposTarjeta.idTipoTarjeta'))
    NumeroTarjeta = Column(String(20))
    Limite = Column(DECIMAL(10, 2))
    MovimientosTarjeta = relationship('MovimientosTarjeta', backref='TarjetasCliente', overlaps='TarjetasCliente,MovimientosTarjeta')
    PeriodosTarjeta = relationship('PeriodosTarjeta', backref='TarjetasCliente', overlaps='TarjetasCliente,PeriodosTarjeta')

class TiposTarjeta(Base):
    __tablename__ = 'TiposTarjeta'
    idTipoTarjeta = Column(Integer, primary_key=True)
    Descripcion = Column(String(255))
    ScoreMinimo = Column(Integer)
    Limite = Column(Integer)
    TarjetasCliente = relationship('TarjetasCliente', backref="TiposTarjeta", overlaps='TiposTarjeta,TarjetasCliente')

class MovimientosTarjeta(Base):
    __tablename__ = 'MovimientosTarjeta'
    idMovimientoTarjeta = Column(Integer, primary_key=True)
    idTarjeta = Column(Integer, ForeignKey('TarjetasCliente.idTarjeta'))
    idTipoMovimiento = Column(Integer, ForeignKey('TipoMovimiento.idTipoMovimiento'))
    idPeriodo = Column(Integer, ForeignKey('PeriodosTarjeta.idPeriodo'))
    descripcion = Column(String(50))
    cuotaActual = Column(Integer)
    cuotasTotales = Column(Integer)
    Monto = Column(DECIMAL(10, 2))

class PeriodosTarjeta(Base):
    __tablename__ = 'PeriodosTarjeta'
    idPeriodo = Column(Integer, primary_key=True)
    idTarjeta = Column(Integer, ForeignKey('TarjetasCliente.idTarjeta'))
    FechaCierre = Column(DateTime(timezone=True))
    MontoConsumos = Column(DECIMAL(10, 2))
    MovimientosTarjeta = relationship('MovimientosTarjeta', backref="PeriodosTarjeta", overlaps='PeriodosTarjeta,MovimientosTarjeta')


class TiposPrestamo(Base):
    __tablename__ = 'TiposPrestamo'
    idTipoPrestamo = Column(Integer, primary_key=True)
    Descripcion = Column(String(255))
    Interes = Column(DECIMAL(5, 2))
    PrestamosCliente = relationship('PrestamosCliente', backref="TiposPrestamo", overlaps='TiposPrestamo,PrestamosCliente')

class PrestamosCliente(Base):
    __tablename__ = 'PrestamosCliente'
    idPrestamo = Column(Integer, primary_key=True)
    idCliente = Column(Integer, ForeignKey('Cliente.idCliente'))
    idTipoPrestamo = Column(Integer, ForeignKey('TiposPrestamo.idTipoPrestamo'))
    MontoSolicitado = Column(DECIMAL(10, 2))
    MontoADevolver = Column(DECIMAL(10, 2))
    CantidadCuotas = Column(Integer)
    CantidadCuotasPagas = Column(Integer)
    MontoProximaCuota = Column(DECIMAL(10, 2))
    VencimientoProximaCuota = Column(DateTime(timezone=True))
