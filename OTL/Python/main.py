from flask import Flask
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime, timedelta


Base = declarative_base()
engine = create_engine('postgresql://user:password@localhost/dbname')
Session = sessionmaker(bind=engine)


class OneTimeLink(Base):
    __tablename__ = "one_time_links"
    
    token = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    expiry = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    

class OTLManager:
    def __init__(self, base_url, expiry_hours=24):
        self.base_url = base_url
        self.expiry_hours = expiry_hours
        
    def generate_otl(self, user_id):
        session = Session()
        token = uuid4().hex
        expiry = datetime.now() + timedelta(hours=self.expiry_hours)
        
        otl = OneTimeLink(
            token=token,
            user_id=user_id,
            expiry=expiry
        )
        session.add(otl)
        session.commit()
        
        return f"{self.base_url}/reset-password/{token}"
    
    def verify_otl(self, token):
        session = Session()
        otl = session.query(OneTimeLink).filter_by(
            token=token,
            used=False
        ).first()
        
        if otl and otl.expiry > datetime.now():
            otl.used = True
            session.commit()
            return otl.user_id
        return None