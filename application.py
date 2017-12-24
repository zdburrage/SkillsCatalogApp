from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User, ItemCategory
from flask import session as login_session
import random, string


# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog App"

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/categories/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    itemCategories = session.query(ItemCategory).filter_by(
        category_id=category_id).all()
    return jsonify(Skills=[i.serialize for i in itemCategories])

@app.route('/items/<int:item_id>/JSON')
def singleItemJSON(item_id):
    item = session.query(Item).filter_by(
        id=item_id).one()
    return jsonify(Item=item.serialize)


# ADD JSON ENDPOINT HERE
@app.route('/catalog/JSON')
def allCatalogItems():
    allItems = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in allItems])

#LOGIN STUFF
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = '  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"' 
    output+= 'integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'
    output += '<link rel=stylesheet type=text/css href={{ url_for("static", filename="styles.css") }}">'
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    return output


@app.route('/logout')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You are now logged out")
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        flash('Failed to revoke token for given user.')
        return redirect('/')

#APP ROUTING STUFF
@app.route('/')
def displayCategories():
    categories = session.query(Category).all()
    return render_template(
        'catalog.html', categories = categories)

@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
            newCategory = Category(name=name,user_id=login_session['user_id'])
            session.add(newCategory)
            session.commit()
        if request.form.getlist('item_value'):
            category = session.query(Category).filter_by(name=name).first()
            for item in request.form.getlist('item_value'):
                newItemCategory = ItemCategory(category_id=category.id,item_id=item)
                session.add(newItemCategory)
                session.commit()
            return redirect('/')
    else:
        items = session.query(Item).all()
        user_id = login_session['user_id']
        return render_template('newcategory.html', items = items, user_id=user_id)

@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToEdit = session.query(Category).filter_by(id=category_id).one()
    if categoryToEdit.user_id != login_session['user_id']:
        flash("You cannot edit this item because you did not create it.")
        return redirect('/')
    itemCategoryIds = session.query(ItemCategory.item_id).filter_by(category_id=category_id).all()
    l = []
    for i in itemCategoryIds:
        l.append(i[0])
    items =session.query(Item).all()
    checked = []
    unchecked = []
    print itemCategoryIds
    for i in items:
        if i.id in l:
            checked.append(i)
        else:
            unchecked.append(i)
    if request.method == 'POST':
        if request.form['name']:
            categoryToEdit.name = request.form['name']
        if request.form.getlist('item_value'):
            intList = []
            for x in request.form.getlist('item_value'):
                intList.append(int(x))
            for i in items:
                if i.id in l and i.id not in intList:
                    icToDelete = session.query(ItemCategory).filter_by(category_id=categoryToEdit.id,item_id=i.id).first()
                    session.delete(icToDelete)
                    session.commit()
                currentSkill = session.query(ItemCategory).filter_by(category_id=categoryToEdit.id,item_id=i.id).first()
                if currentSkill is None and int(i.id) in intList:
                    newItemCategory = ItemCategory(category_id=categoryToEdit.id,item_id=i.id)
                    session.add(newItemCategory)
                    session.commit()

        session.add(categoryToEdit)
        session.commit()
        return redirect(url_for('displayItemsInCategory', category_id=categoryToEdit.id))
    else:
        return render_template('editcategory.html', category=categoryToEdit, checked=checked,unchecked=unchecked)    



@app.route('/items/all')
def allItems():
    items = session.query(Item).all()
    return render_template('allitems.html', items = items)


@app.route('/categories/<int:category_id>/items')
def displayItemsInCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(ItemCategory).filter_by(category_id = category_id).all()
    return render_template('categoryitems.html', items = items, category = category)


@app.route('/items/<int:item_id>')
def displayIndividualItem(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', item = item)



@app.route('/items/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form[
                           'description'], user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        return redirect('/')
    else:
        categories = session.query(Category).all()
        return render_template('newitem.html', categories=categories)


@app.route('/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if editedItem.user_id != login_session['user_id']:
        flash("You cannot edit this item because you did not create it.")
        return redirect(url_for('allItems'))
    categories = session.query(Category).all()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('allItems'))
    else:
        return render_template(
            'edititem.html', editedItem=editedItem)

@app.route('/category/<int:category_id>/items/<int:item_id>/remove')
def removeItemFromCategory(category_id,item_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemCategory = session.query(ItemCategory).filter(and_(ItemCategory.item_id==item_id, ItemCategory.category_id==category_id)).one()
    if itemCategory.category.user_id != login_session['user_id']:
        flash("You cannot edit this category because you did not create it.")
        return redirect(url_for('displayItemsInCategory', category_id=category_id))
    session.delete(itemCategory)
    session.commit()
    return redirect(url_for('displayItemsInCategory', category_id=category_id))


@app.route('/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        flash("You cannot delete this item because you did not create it.")
        return redirect('/')
    if request.method == 'POST':
        itemCategories = session.query(ItemCategory).filter_by(item_id=item_id).all()
        for item in itemCategories:
            session.delete(item)
            session.commit()
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('allItems'))
    else:
        return render_template('delete.html', itemToDelete=itemToDelete)


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

if __name__ == '__main__':
    app.secret_key = 'v0RNg7e4ft3VUR61D2MebuIq'
    app.debug = True
    logged_in_user = None
    app.run(host='0.0.0.0', port=5000)
