
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()
engine = create_engine('sqlite:///itemcatalog.db')


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)

class Category(Base):
	__tablename__ = 'category'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
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
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
	    """Return object data in easily serializeable format"""
	    return {
	        'name': self.name,
	        'description': self.description,
	        'id': self.id,
	        'creator': self.user.name,
	        'job category': self.category.name
	    }

class ItemCategory(Base):
	__tablename__ = 'itemcategory'
	id = Column(Integer, primary_key=True)
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	item_id = Column(Integer, ForeignKey('item.id'))
	item = relationship(Item)



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

USERS = [
	User(name='Zachary Burrage', email='zac.burrage@gmail.com')

]

CATEGORIES = [

	Category(name='Back End Virtuoso', user_id=1),
	Category(name='Front End Guru', user_id=1),
	Category(name='Database Monster', user_id=1),
	Category(name='Master of Scrums', user_id=1),
	Category(name='Project Czar', user_id=1),
	Category(name='Systems Engi-nerd', user_id=1),
	Category(name='Script Flipper', user_id=1),
]

ITEMS = [

	Item(name="Object Oriented Programming", description="OOP", category_id=1, user_id=1),
	Item(name="Relational Databases", description="A relational database is a digital database based on the"
	 "relational model of data, as proposed by E. F. Codd in 1970."
	 "A software system used to maintain relational databases"
	 "is a relational database management system (RDBMS). Virtually all relational database" 
	 "systems use SQL (Structured Query Language) for querying and maintaining the database.", category_id=1, user_id=1),
	Item(name="JavaScript", description="A front end dynamic language used to manipulate HTML and CSS as well as send API calls", category_id=2, user_id=1),
	Item(name="HTML", description="HyperText Markup Language, used for setting the structure of your web page", category_id=2, user_id=1),
	Item(name="SQL", description="RDB", category_id=3, user_id=1),
	Item(name="Oracle", description="RDB", category_id=3, user_id=1),
	Item(name="Kanban", description="RDB", category_id=4, user_id=1),
	Item(name="Agile Methodology", description="RDB", category_id=4, user_id=1),
	Item(name="Budgeting", description="RDB", category_id=5, user_id=1),
	Item(name="Tough Conversations", description="RDB", category_id=5, user_id=1),
	Item(name="Six Sigma", description="RDB", category_id=6, user_id=1),
	Item(name="Operations Management", description="RDB", category_id=6, user_id=1),
	Item(name="Shell Scripting", description="RDB", category_id=7, user_id=1),
	Item(name="Bash Scripting", description="RDB", category_id=7, user_id=1),
	Item(name="CSS", description="Cascading Style Sheet, used to style the HTML you write", category_id=2, user_id=1),


]
def addUsers():
	for user in USERS:
		session.add(user)
	session.commit()
def addCategories():
    session.bulk_save_objects(CATEGORIES)
    session.commit()

def addItems():
	session.bulk_save_objects(ITEMS)
	session.commit()

if __name__ == '__main__':
    addUsers()
    addCategories()
    addItems()