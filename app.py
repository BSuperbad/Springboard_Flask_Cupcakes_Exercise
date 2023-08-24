# pip3 install psycopg2-binary
# pip3 install flask-sqlalchemy
# pip3 install flask-wtf

"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake, DEFAULT_IMAGE_URL
from forms import AddCupcakeForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/', methods=['GET', 'POST'])
def add_cupcake():
    form = AddCupcakeForm()
    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        form.size.choices = size
        rating = form.rating.data
        image = form.image.data
        cupcake = Cupcake(
            flavor=flavor,
            size=size,
            rating=rating,
            image=image)
        db.session.add(cupcake)
        db.session.commit()
        return redirect('/')

    else:
        return render_template("home.html", form=form)


@app.route('/api/cupcakes')
def list_cupcakes():
    """Lists all cupcakes in the database in JSON"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Retrieves specific cupcake in db based on existing id and returns JSON"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Creates and adds new cupcake to the db, responds with JSON"""
    flavor = request.json.get('flavor')
    size = request.json.get('size')
    rating = request.json.get('rating')
    image = request.json.get('image', DEFAULT_IMAGE_URL)
    cupcake = Cupcake(flavor=flavor, size=size,
                      rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()
    resp_json = jsonify(cupcake=cupcake.serialize())
    return (resp_json, 201)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Updates section of cupcake depending on what the user wants. Cannot change flavor or id."""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Deletes a cupcake from the database"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='cupcake deleted')
