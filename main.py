"""

Portfolio: CoffeeWiFi
#100DaysOfCode with Python
Day: 87
Date: 2023-07-15
Author: MC

"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # pobieranie nazw kolumn bezpośrednio z bazy danych
    def to_dict(self):
        dictionary = {}

        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)

        return dictionary


class CaffeForm_Add(FlaskForm):
    name = StringField("Cafe name:", validators=[DataRequired()])
    map_url = StringField("Map url:", validators=[DataRequired()])
    img_url = StringField("Image url:", validators=[DataRequired()])
    location = StringField("Location:", validators=[DataRequired()])
    seats = StringField("Seats:", validators=[DataRequired()])
    has_toilet = BooleanField("Has toilet:", validators=[DataRequired()])
    has_wifi = BooleanField("Has wifi:", validators=[DataRequired()])
    has_sockets = BooleanField("Has sockets:", validators=[DataRequired()])
    can_take_calls = BooleanField("Can take calls", validators=[DataRequired()])
    coffee_proce = StringField("Coffee proce:", validators=[DataRequired()])

    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    """
    get all cafes
    :return:
    """
    cafes_list = db.session.query(Cafe).all()

    return render_template('cafes.html', cafes=cafes_list)


@app.route('/delete')
def delete_cafe():
    cafe_id = int(request.args.get('id'))

    try:

        cafe_to_del = Cafe.query.get(cafe_id)

        db.session.delete(cafe_to_del)
        db.session.commit()
    except Exception as e:
        print(e.__str__())

    return redirect(url_for('cafes'))


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CaffeForm_Add()
    print("do add form")

    if request.method == 'POST':
        h_wifi = False
        if request.form.get('has_wifi') == 'y':
            h_wifi = True

        h_toilet = False
        if request.form.get('has_toilet') == 'y':
            h_toilet = True

        h_sockets = False
        if request.form.get('has_sockets') == 'y':
            h_sockets = True

        calls = False
        if request.form.get('can_take_calls') == 'y':
            calls = True

        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get('map_url'),
            img_url=request.form.get('img_url'),
            location=request.form.get('location'),
            seats=request.form.get('seats'),
            # has_toilet=request.form.get('has_toilet'),
            has_toilet=h_toilet,
            # has_wifi=request.form.get('has_wifi'),
            has_wifi=h_wifi,
            # has_sockets=request.form.get('has_sockets'),
            has_sockets=h_sockets,
            # can_take_calls=request.form.get('can_take_calls'),
            can_take_calls=calls,
            coffee_price=request.form.get('coffee_price')
        )
        # new_cafe = Cafe(
        #     name=request.form.name.data,
        #     map_url=request.form.map_url.data,
        #     img_url=request.form.img_url.data,
        #     location=request.form.location.data,
        #     seats=request.form.seats.data,
        #     has_toilet=request.form.has_toilet.data,
        #     has_wifi=request.form.has_wifi.data,
        #     has_sockets=request.form.has_sockets.data,
        #     can_take_calls=request.form.can_take_calls.data,
        #     coffee_price=request.form.coffee_price.data
        # )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
        # Exercise:

    return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
