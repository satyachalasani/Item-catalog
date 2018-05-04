import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class BookSection(Base):
    __tablename__ = 'Sections'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    Books = relationship('BooksS', cascade='all, delete-orphan')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
        }


class BooksS(Base):
        __tablename__ = 'Books'
        name = Column(String(80), nullable=False)
        id = Column(Integer, primary_key=True)
        description = Column(String(250))
        price = Column(String(8))
        rating = Column(String(250))
        Sections_id = Column(Integer, ForeignKey('Sections.id'))
        Sections = relationship('BookSection')
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship(User)

        @property
        def serialize(self):
            """Return object data in easily serializeable format"""
            return {
                'description': self.description,
                'name': self.name,
                'price': self.price,
                'id': self.id,
                'rating': self.rating,
                'Sections' : self.Sections
            }

engine = create_engine('sqlite:///BooksCatalogwithusers.db')
Base.metadata.create_all(engine)
