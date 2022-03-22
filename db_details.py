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

    def __repr__(self):
        return f'Company(id={self.company_uid!r}, name={self.name!r}, location={self.location!r}, website={self.website!r})'


class CompanyDescription(Base):
    __tablename__ = 'company_description'

    id = Column(Integer, primary_key=True)
    company_uid = Column(String(6), ForeignKey('companies.company_uid'), nullable=False)
    description = Column(Text)
    db_time_created = Column(DateTime(timezone=True), server_default=func.now())
    db_time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="descriptions")

    def __repr__(self):
        return f'CompanyDescription(company_id={self.company_uid!r}, description={self.description!r})'


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

    def __repr__(self):
        return f'Position(position_id={self.position_uid!r}, position_name={self.pos_name!r}, department={self.department!r}, location={self.location!r}, employment_type={self.employment_type!r}, experience={self.experience_level!r}, time_updated={self.time_updated!r}, company_id={self.company_uid!r})'


class PositionDescription(Base):
    __tablename__ = 'position_description'

    id = Column(Integer, primary_key=True)
    position_uid = Column(String(6), ForeignKey('positions.position_uid'), nullable=False)
    description_title = Column(String(256))
    description = Column(Text)
    db_time_created = Column(DateTime(timezone=True), server_default=func.now())
    db_time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    position = relationship("Position", back_populates="descriptions")

    def __repr__(self):
        return f'Position(id={self.id!r}, position_id={self.position_uid!r}, description_title={self.description_title!r}, description={self.description!r})'
