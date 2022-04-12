from sqlalchemy import Column, func, Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

# base class for all of our tables
Base = declarative_base()


# company tables
class Company(Base):
    __tablename__ = 'companies'

    company_uid = Column(String(6), primary_key=True)
    name = Column(String(256))
    location = Column(String(256))
    website = Column(String(256))
    db_time_created = Column(DateTime(timezone=True), server_default=func.now())
    db_time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    positions = relationship("Position", back_populates="company", cascade="all, delete-orphan")
    descriptions = relationship("CompanyDescription", back_populates="company", cascade="all, delete-orphan")
    extra_info = relationship("ExtraCompanyInfo", backref="company", cascade="all, delete-orphan")


class ExtraCompanyInfo(Base):
    __tablename__ = 'extra_company_info'

    id = Column(Integer, primary_key=True)
    company_uid = Column(String(6), ForeignKey('companies.company_uid'), nullable=False)
    employee_count = Column(Integer)
    founded = Column(DateTime)
    headline = Column(Text)
    industry = Column(String(256))
    profiles = Column(Text)
    company_type = Column(String(50))

    db_time_created = Column(DateTime(timezone=True), server_default=func.now())
    db_time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="extra_info")


# extra descriptions from API
class CompanyDescription(Base):
    __tablename__ = 'company_description'

    id = Column(Integer, primary_key=True)
    company_uid = Column(String(6), ForeignKey('companies.company_uid'), nullable=False)
    description = Column(Text)
    db_time_created = Column(DateTime(timezone=True), server_default=func.now())
    db_time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="descriptions")


# positions tables

class Position(Base):
    __tablename__ = 'positions'

    position_uid = Column(String(6), primary_key=True)
    pos_name = Column(String(256), nullable=False)
    department = Column(String(256))
    is_remote = Column(Boolean)
    location = Column(Text)
    employment_type = Column(String(256))
    experience_level = Column(String(256))
    time_updated = Column(DateTime)
    comeet_pos_url = Column(String(500))
    company_pos_url = Column(String(500))
    company_uid = Column(String(6), ForeignKey('companies.company_uid'), nullable=False)
    db_time_created = Column(DateTime(timezone=True), server_default=func.now())
    db_time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="positions")
    descriptions = relationship("PositionDescription", back_populates="position", cascade="all, delete-orphan")


class PositionDescription(Base):
    __tablename__ = 'position_description'

    id = Column(Integer, primary_key=True)
    position_uid = Column(String(6), ForeignKey('positions.position_uid'), nullable=False)
    description_title = Column(String(256))
    description = Column(Text)
    db_time_created = Column(DateTime(timezone=True), server_default=func.now())
    db_time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    position = relationship("Position", back_populates="descriptions")
