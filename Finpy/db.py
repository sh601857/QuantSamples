#coding=utf-8

from sqlalchemy import Column, ForeignKey, Float, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class b_sec(Base):
    __tablename__ = 'b_sec'
    secID = Column(String(32), primary_key=True, nullable=False)
    ticker = Column(String(32), nullable=False)
    exchangeCD = Column(String(32), nullable=False)
    sectype = Column(String(32), nullable=False)
    valid = Column(Boolean, default=True)


class d_equdiv(Base):
    __tablename__ = 'd_equdiv'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    secID = Column(String(32), primary_key=True, nullable=False)
    exDivDate = Column(DateTime, primary_key=True, nullable=False)
    sch = Column(Float, default=0.0)
    perCashDiv = Column(Float, default = 0.0)
    
class d_ev(Base):
    __tablename__ = 'd_ev'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    secID = Column(String(32), primary_key=True, nullable=False)
    endDateRep = Column(DateTime, primary_key=True, nullable=False)
    ev = Column(Float, default = 0.0)
    exDiv = Column(Float, default = 0.0)
    
class d_quote(Base):
    __tablename__ = 'd_quote'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    secID = Column(String(32), primary_key=True, nullable=False)
    tradeDate = Column(DateTime, primary_key=True, nullable=False)    
    closePrice = Column(Float, default = None) 
    openPrice  = Column(Float, default = None) 
    highestPrice = Column(Float, default = None) 
    lowestPrice = Column(Float, default = None) 
    turnoverVol = Column(Float, default = None) 
    chgPct =  Column(Float, default = None) 

def create_tables():
    
    DB_CONNECT_STRING = u'sqlite:///D:\\yun\\百度云\\db\\Finpy.db'
    
    engine = create_engine(DB_CONNECT_STRING, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    
create_tables()