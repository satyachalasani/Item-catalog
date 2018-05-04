from flask import (Flask, render_template,
                   request, redirect,
                   jsonify,
                   url_for,
                   flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from setup import Base, BookSection, BooksS, User

#   Import Login session
from flask import session as login_session
import random
import string

#   imports for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

#   import login decorator
from functools import wraps

app = Flask(__name__)

CLIENT_ID = json.loads(open(
    'client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Fav Books App"

engine = create_engine('sqlite:///BooksCatalogwithusers.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()

#   create a state token to request forgery.
#   store it in the session for later validation


@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    #   validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application-json'
        return response
    #   Obtain authorization code
    code = request.data

    try:
        #   upgrade the authorization code in credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application-json'
        return response

    #   Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode("utf-8"))
    #   If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    #   Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #   Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    #   Access token within the app
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    #   Store the access token in the session for later use.

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Succesfully connected users', 200))

    #   Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #   See if user exists or if it doesn't make a new one
    print 'User email is' + str(login_session['email'])
    user_id = getUserID(login_session['email'])
    if user_id:
        print 'Existing user#  ' + str(user_id) + 'matches this email'
    else:
        user_id = createUser(login_session)
        print 'New user_id#  ' + str(user_id) + 'created'
    login_session['user_id'] = user_id
    print 'Login session is tied to :id#  ' + str(login_session['user_id'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 300px; height: 300px;border-radius:150px;- \
      webkit-border-radius:150px;-moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


#   Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).first()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session.
@app.route('/gdisconnect')
def gdisconnect():
    # only disconnect a connected User
    access_token = login_session.get('access_token')
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print'Access Token is None'
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is'
    print result
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showBookSections'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showBookSections'))


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


#   JSON APIs to view BookSection Information
@app.route('/Sections/<int:Sections_id>/book/JSON')
def SectionsBooksJSON(Sections_id):
    Sections = session.query(BookSection).filter_by(id=Sections_id).one()
    items = session.query(BooksS).filter_by(Sections_id=Sections_id).all()
    return jsonify(BooksSs=[i.serialize for i in items])


@app.route('/Sections/<int:Sections_id>/book/<int:book_id>/JSON')
def bookItemJSON(Sections_id, book_id):
    Books = session.query(BooksS).filter_by(id=book_id).one()
    return jsonify(Books=Books.serialize)


@app.route('/Sections/JSON')
def SectionssJSON():
    Sectionss = session.query(BookSection).all()
    return jsonify(Sectionss=[r.serialize for r in Sectionss])


#  show all Sectionss
@app.route('/')
@app.route('/Sections/')
def showBookSections():
    Sectionss = session.query(BookSection).order_by(asc(BookSection.name))
    if 'username' not in login_session:
        return render_template('publicSections.html', Sectionss=Sectionss)
    else:
        return render_template('Sectionss.html', Sectionss=Sectionss)


#  Create a new Sections
@app.route('/Sections/new/', methods=['GET', 'POST'])
def newBookSection():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newBookSection = BookSection(name=request.form['name'],
                                     user_id=login_session['user_id'])
        session.add(newBookSection)
        flash('New BookSection %s Successfully Created' % newBookSection.name)
        session.commit()
        return redirect(url_for('showBookSections'))
    else:
        return render_template('newSectionss.html')


#  Edit a Sections
@app.route('/Sections/<int:Sections_id>/edit/', methods=['GET', 'POST'])
def editBookSection(Sections_id):
    editedBookSection = session.query(BookSection).filter_by(
        id=Sections_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedBookSection.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized to edit \
       this Sections. please create your own Sections in order to edit.');} \
       </script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedBookSection.name = request.form['name']
            flash('BookSection Successfully Edited %s'
                  % editedBookSection.name)
            return redirect(url_for('showBookSections'))
    else:
        return render_template('editSectionss.html',
                               Sections=editedBookSection)


#  Delete a Sections
@app.route('/Sections/<int:Sections_id>/delete/',
           methods=['GET', 'POST'])
def deleteBookSection(Sections_id):
    SectionsToDelete = session.query(BookSection).filter_by(
        id=Sections_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if SectionsToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are not authorized to \
         delete this Sections.please create your own Sections to delete');}\
         </script><body onLoad='myFunction()''>"
    if request.method == 'POST':
        session.delete(SectionsToDelete)
        flash('%s Successfully Deleted' % SectionsToDelete.name)
        session.commit()
        return redirect(url_for('showBookSections',
                                Sections_id=Sections_id))
    else:
        return render_template('deleteSectionss.html',
                               Sections=SectionsToDelete)


#  Show a Sections book
@app.route('/Sections/<int:Sections_id>/')
@app.route('/Sections/<int:Sections_id>/book/')
def showBooks(Sections_id):
    Sections = session.query(BookSection).filter_by(id=Sections_id).first()
    creator = getUserInfo(Sections.user_id)
    items = session.query(BooksS).filter_by(Sections_id=Sections_id).all()

    if 'username' not in login_session or creator.id \
            != login_session['user_id']:
        return render_template('publicbook.html', items=items,
                               Sections=Sections, creator=creator)
    else:
        return render_template('book.html', items=items,
                               Sections=Sections, creator=creator)


#  Create a new book item
@app.route('/Sections/<int:Sections_id>/book/new/', methods=['GET', 'POST'])
def newBooksS(Sections_id):
    if 'username' not in login_session:
        return redirect('/login')
    Sections = session.query(BookSection).filter_by(id=Sections_id).one()
    if request.method == 'POST':
        newItem = BooksS(name=request.form['name'],
                         description=request.form['description'],
                         price=request.form['price'],
                         rating=request.form['rating'],
                         Sections_id=Sections_id, user_id=Sections.user_id)
        session.add(newItem)
        session.commit()
        flash('New Books %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showBooks',
                                Sections_id=Sections_id))
    else:
        return render_template('newbookitem.html',
                               Sections_id=Sections_id)


#  Edit a book item
@app.route('/Sections/<int:Sections_id>/book/<int:book_id>/edit',
           methods=['GET', 'POST'])
def editBooksS(Sections_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(BooksS).filter_by(id=book_id).one()
    Sections = session.query(BookSection).filter_by(id=Sections_id).one()
    if login_session['user_id'] != Sections.user_id:
        return "<script>function myFunction() {alert('You are not authorized to \
          edit book items to this Sections.Please create your own Sections in \
          order to edit items.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['rating']:
            editedItem.rating = request.form['rating']
        session.add(editedItem)
        session.commit()
        flash('Books Item Successfully Edited')
        return redirect(url_for('showBooks', Sections_id=Sections_id))
    else:
        return render_template('editbookitem.html',
                               Sections_id=Sections_id,
                               book_id=book_id, item=editedItem)


#  Delete a book item
@app.route('/Sections/<int:Sections_id>/book/<int:book_id>/delete',
           methods=['GET', 'POST'])
def deleteBooksS(Sections_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    Sections = session.query(BookSection).filter_by(id=Sections_id).one()
    itemToDelete = session.query(BooksS).filter_by(id=book_id).one()
    if login_session['user_id'] != Sections.user_id:
        return "<script>function myFunction() {alert ('you are not authorized to \
         delete book items to this Sections.please create your own Sections \
         in order to delete items');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Books Item Successfully Deleted')
        return redirect(url_for('showBooks', Sections_id=Sections_id))
    else:
        return render_template('deleteBooksS.html', item=itemToDelete)
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
