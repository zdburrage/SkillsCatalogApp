
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()
engine = create_engine('sqlite:///itemcatalog.db')


class Category(Base):
	__tablename__ = 'category'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)

	@property
	def serialize(self):
	    """Return object data in easily serializeable format"""
	    return {
	        'name': self.name,
	        'id': self.id,
	    }

class Item(Base):
	__tablename__ = 'item'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(1000), nullable=False)
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)

	@property
	def serialize(self):
	    """Return object data in easily serializeable format"""
	    return {
	        'name': self.name,
	        'description': self.description,
	        'id': self.id,
	    }




DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

Base.metadata.create_all(engine)

CATEGORIES = [

	'Back End Virtuoso',
	'Front End Guru',
	'Database Monster',
	'Master of Scrums',
	'Project Czar',
	'Systems Engi-nerd',
	'Script Flipper'
]

ITEMS = [

	Item(name="Object Oriented Programming", description="OOP", category_id=1),
	Item(name="Relational Databases", description="A relational database is a digital database based on the"
	 "relational model of data, as proposed by E. F. Codd in 1970."
	 "A software system used to maintain relational databases"
	 "is a relational database management system (RDBMS). Virtually all relational database" 
	 "systems use SQL (Structured Query Language) for querying and maintaining the database.", category_id=1),
	Item(name="JavaScript", description="RDB", category_id=2),
	Item(name="HTML", description="RDB", category_id=2),
	Item(name="SQL", description="RDB", category_id=3),
	Item(name="Oracle", description="RDB", category_id=3),
	Item(name="Kanban", description="RDB", category_id=4),
	Item(name="Agile Methodology", description="RDB", category_id=4),
	Item(name="Budgeting", description="RDB", category_id=5),
	Item(name="Tough Conversations", description="RDB", category_id=5),
	Item(name="Six Sigma", description="RDB", category_id=6),
	Item(name="Operations Management", description="RDB", category_id=6),
	Item(name="Shell Scripting", description="RDB", category_id=7),
	Item(name="Bash Scripting", description="RDB", category_id=7),
	Item(name="CSS", description="RDB", category_id=2),


]

def addCategories():
    for category in CATEGORIES:
        session.add(Category(name=category))
    session.commit()

def addItems():
	session.bulk_save_objects(ITEMS)
	session.commit()

if __name__ == '__main__':
    addCategories()
    addItems()