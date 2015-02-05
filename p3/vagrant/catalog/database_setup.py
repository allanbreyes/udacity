import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Provider(Base):
    __tablename__ = 'provider'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    homepage_url = Column(String(255))

    @property
    def serialize(self):
        """ JSON serializer method """
        return {
            'id': self.id,
            'name': self.name,
            'homepage_url': self.homepage_url
        }

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    course_url = Column(String(255))
    thumbnail_url = Column(String(255))
    course_number = Column(String(20))
    description = Column(String(1000))
    start_date = Column(Date)
    featured = Column(Boolean, default=False)
    provider_id = Column(Integer, ForeignKey('provider.id'))
    provider = relationship(Provider)

    @property
    def serialize(self):
        """ JSON serializer method """
        return {
            'id': self.id,
            'name': self.name,
            'course_url': self.course_url,
            'thumbnail_url': self.thumbnail_url,
            'course_number': self.course_number,
            'description': self.description,
            'start_date': str(self.start_date.isoformat()),
            'featured': self.featured,
            'provider_id': self.provider_id
        }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
