
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
	        'creator': self.user.name
	    }

class Item(Base):
	__tablename__ = 'item'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(1000), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
	    """Return object data in easily serializeable format"""
	    return {
	        'name': self.name,
	        'description': self.description,
	        'id': self.id,
	        'creator': self.user.name
	    }

class ItemCategory(Base):
	__tablename__ = 'itemcategory'
	id = Column(Integer, primary_key=True)
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	item_id = Column(Integer, ForeignKey('item.id'))
	item = relationship(Item)

	@property
	def serialize(self):
	    """Return object data in easily serializeable format"""
	    return {
	        'name': self.item.name,
	        'description': self.item.description,
	        'id': self.item.id,
	        'creator': self.item.user.name
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

	Item(name="Object Oriented Programming", description="OOP", user_id=1),
	Item(name="Relational Databases", description="A relational database is a digital database based on the"
	 "relational model of data, as proposed by E. F. Codd in 1970."
	 "A software system used to maintain relational databases"
	 "is a relational database management system (RDBMS). Virtually all relational database" 
	 "systems use SQL (Structured Query Language) for querying and maintaining the database.",user_id=1),
	Item(name="JavaScript", description="A front end dynamic language used to manipulate HTML and CSS as well as send API calls", user_id=1),
	Item(name="HTML", description="HyperText Markup Language, used for setting the structure of your web page", user_id=1),
	Item(name="SQL", description="RDB", user_id=1),
	Item(name="Oracle", description="RDB", user_id=1),
	Item(name="Kanban", description="RDB",user_id=1),
	Item(name="Agile Methodology", description="RDB", user_id=1),
	Item(name="Budgeting", description="RDB", user_id=1),
	Item(name="Tough Conversations", description="RDB", user_id=1),
	Item(name="Six Sigma", description="RDB", user_id=1),
	Item(name="Operations Management", description="RDB", user_id=1),
	Item(name="Shell Scripting", description="RDB", user_id=1),
	Item(name="Bash Scripting", description="RDB", user_id=1),
	Item(name="CSS", description="Cascading Style Sheet, used to style the HTML you write", user_id=1),


]

ITEMCATEGORIES = [

ItemCategory(category_id=1,item_id=1),
ItemCategory(category_id=1,item_id=2),
ItemCategory(category_id=2,item_id=3),
ItemCategory(category_id=2,item_id=4),
ItemCategory(category_id=3,item_id=5),
ItemCategory(category_id=3,item_id=6),
ItemCategory(category_id=4,item_id=7),
ItemCategory(category_id=4,item_id=8),
ItemCategory(category_id=5,item_id=9),
ItemCategory(category_id=5,item_id=10),
ItemCategory(category_id=6,item_id=11),
ItemCategory(category_id=6,item_id=12),
ItemCategory(category_id=7,item_id=13),
ItemCategory(category_id=7,item_id=14),
ItemCategory(category_id=2,item_id=15),


ItemCategory(category_id=1,item_id=15),
ItemCategory(category_id=1,item_id=6),
ItemCategory(category_id=2,item_id=10),
ItemCategory(category_id=3,item_id=1)








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

def addItemCategories():
	session.bulk_save_objects(ITEMCATEGORIES)
	session.commit()


if __name__ == '__main__':
    addUsers()
    addCategories()
    addItems()
    addItemCategories()