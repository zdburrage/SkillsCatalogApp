#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Category(Base):

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        return {'name': self.name, 'id': self.id,
                'creator': self.user.name}


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
            'creator': self.user.name,
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
            'creator': self.item.user.name,
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

USERS = [User(name='Zachary Burrage', email='zac.burrage@gmail.com')]

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
    Item(name='Object Oriented Programming', description='OOP',
         user_id=1),
    Item(name='Relational Databases',
         description="""A relational database is a digital database based
                        on therelational model of data, as proposed by E. F.
                        Codd in 1970.A software system used to maintain
                        relational databasesis a relational database
                        management system (RDBMS). Virtually all relational
                        databasesystems use SQL (Structured Query Language)
                        for querying and maintaining the database.""",
         user_id=1),
    Item(name='JavaScript',
         description="""A front end dynamic language used to
                     manipulate HTML and CSS as well as send API calls""",
         user_id=1),
    Item(name='HTML',
         description="""HyperText Markup Language, used for
                        setting the structure of your web page""",
         user_id=1),
    Item(name='SQL',
         description="""A very widely used database manipulation
                        language for creating databases and editing them.""",
         user_id=1),
    Item(name='Oracle', description='A company that owns Java...somehow',
         user_id=1),
    Item(name='Kanban',
         description="""A form of agile methodology that involves
                        moving user stories through stages from backlog
                        to User accepptance""",
         user_id=1),
    Item(name='Agile Methodology',
         description="""A methodology focused on delivering a product
                        in a timely manner rather than getting it
                        right the first time""",
         user_id=1),
    Item(name='Budgeting', description='Managing Money for projects',
         user_id=1),
    Item(name='Tough Conversations',
         description="""Being able to have conversations that
                        aren't easy but need to be done""",
         user_id=1),
    Item(name='Six Sigma',
         description="""a set of management techniques intended to
                        improve business processes by greatly reducing
                        the probability that an error or defect will occur.""",
         user_id=1),
    Item(name='Operations Management',
         description="""Operations management refers to the administration of
                        business practices to create
                        the highest level of efficiency
                        possible within an organization.""",
         user_id=1),
    Item(name='Shell Scripting',
         description="""Shell scripts allow us to program
                        commands in chains and
                        have the system execute them
                        as a scripted event, just like
                        batch files. They also allow for
                        far more useful functions,
                        such as command substitution.""",
         user_id=1),
    Item(name='Bash Scripting',
         description="""A Bash script is a plain text file which contains a series of
                        commands. These commands are a mixture
                        of commands we would normally
                        type ouselves on the command
                        line (such as ls or cp for example) and
                        commands we could type on the command
                        line but generally wouldn't""",
         user_id=1),
    Item(name='CSS',
         description="""Cascading Style Sheet, used to
                        style the HTML you write""",
         user_id=1),
]

ITEMCATEGORIES = [
    ItemCategory(category_id=1, item_id=1),
    ItemCategory(category_id=1, item_id=2),
    ItemCategory(category_id=2, item_id=3),
    ItemCategory(category_id=2, item_id=4),
    ItemCategory(category_id=3, item_id=5),
    ItemCategory(category_id=3, item_id=6),
    ItemCategory(category_id=4, item_id=7),
    ItemCategory(category_id=4, item_id=8),
    ItemCategory(category_id=5, item_id=9),
    ItemCategory(category_id=5, item_id=10),
    ItemCategory(category_id=6, item_id=11),
    ItemCategory(category_id=6, item_id=12),
    ItemCategory(category_id=7, item_id=13),
    ItemCategory(category_id=7, item_id=14),
    ItemCategory(category_id=2, item_id=15),
    ItemCategory(category_id=1, item_id=15),
    ItemCategory(category_id=1, item_id=6),
    ItemCategory(category_id=2, item_id=10),
    ItemCategory(category_id=3, item_id=1),
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
