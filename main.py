from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

"""SQLALchemy"""
"""DB CREATION: Connection between sqlite and SQLALchemy. by naming and allocating the db """
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///top10movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
"""class with a structure and condition of the db"""
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(400), nullable=False)
    img_url = db.Column(db.String(400), nullable=False)
"""creation of the db with the containt from the class """
db.create_all()
# """After ending the class form, introduce data in the Movie class to verify that the db it's work well. So,
#  I create an Object of the Movie class introduce data and Run it => Open de db and verify is it Ok and them
#  comment-out the Object new_movie and its all content (if there is an error in the bd, verify that the key are the same
#  that in the class)"""
# dbmovie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
#
# def __repr__(self):
#     return '<Movie %r>' % self.title
# """TO RUN AND ACTIVATE THE DB"""
# db.session.add(dbmovie)
# db.session.commit()

"""class form to edit: "rating' and "review" of a existing movie on the db """


@app.route("/")
def home():
    """all the data contain in the db convert in a variable to send the data to the template """
    movie = Movie.query.all()
    return render_template("index.html", movies=movie)

"""class form to edit: "rating' and "review" of a existing movie on the db """
class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


# @app.route('/edit', methods=['GET','POST'])
# def rate_movie():
#     global movie
#     form = RateMovieForm()
#     if request.method == 'POST' :
#         """the id of the element as  reference"""
#         movie_id = request.args.get('id')
#         movie = Movie.query.get(movie_id)
#         """data that will be updated"""
#         if form.validate_on_submit():
#             movie.rating = form.rating.data
#             movie.review = form.review.data
#             db.session.add(movie)
#             db.session.commit()
#             return redirect(url_for('home'))
#     return render_template("edit.html",movie=movie, form=form)


if __name__ == '__main__':
    app.run(debug=True)
