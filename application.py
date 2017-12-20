from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/categories/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


# # ADD JSON ENDPOINT HERE
# @app.route('/restaurants/<int:restaurant_id>/menu/JSON')
# def menuItemJSON(restaurant_id, menu_id):
#     menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
#     return jsonify(MenuItem=menuItem.serialize)


@app.route('/')
def displayCategories():
    categories = session.query(Category).all()
    return render_template(
        'catalog.html', categories = categories)

@app.route('/categories/<int:category_id>/items')
def displayItemsInCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return render_template('categoryitems.html', items = items, category = category)


@app.route('/items/<int:item_id>')
def displayIndividualItem(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', item = item)



@app.route('/items/new', methods=['GET', 'POST'])
def newItem():

    if request.method == 'POST':
        category_id=request.form['category_id']
        newItem = Item(name=request.form['name'], description=request.form[
                           'description'], category_id=request.form['category_id'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('displayItemsInCategory', category_id=category_id))
    else:
        categories = session.query(Category).all()
        return render_template('newitem.html', categories=categories)


@app.route('/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category_id']:
            editedItem.category_id = request.form['category_id']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('displayItemsInCategory', category_id=editedItem.category_id))
    else:

        return render_template(
            'edititem.html', editedItem=editedItem, categories = categories)


@app.route('/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        category_id = itemToDelete.category_id
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('displayItemsInCategory', category_id=category_id))
    else:
        return render_template('delete.html', itemToDelete=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
