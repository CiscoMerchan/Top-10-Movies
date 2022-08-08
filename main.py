from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_DB_API_KEY = '95c1069a66776024975aa20ac346d6e0'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

"""SQLALchemy"""
"""DB CREATION: Connection between sqlite and SQLALchemy. by naming and allocating the db """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top10movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
"""class with a structure and condition of the db"""

"""***************** F O R M S *****************************************"""
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(400), nullable=False)
    img_url = db.Column(db.String(400), nullable=False)
"""creation of the db with the containt from the class """
db.create_all()
"""Form that goes in 'add.html' for the user find a movie in api.themoviedb.org database. this class is in 'add_movie() """
class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

"""class form to edit: "rating' and "review" of a existing movie on the db. in  ' rate.movie()' and the form visible in
'edit.html' """
class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")
# """After ending the class form, introduce data in the Movie class to verify that the db it's work well. So,
#  I create an Object of the Movie class introduce data and Run it => Open de db and verify is it Ok and them
#  comment-out the Object new_movie and its all content (if there is an error in the bd, verify that the key are the same
#  that in the class)"""
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's
#     sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a
#     jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )

# """TO RUN AND ACTIVATE THE DB"""
# db.session.add(new_movie)
# db.session.commit()

"""*****************  *****************************************"""

"""Principal page were is visible the movie that exist in the local database"""
@app.route("/")
def home():
    """all the data contain in the db convert in a variable to send the data to the template """
    all_movies = Movie.query.order_by(Movie.rating.desc()).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - 1
    db.session.commit()
    return render_template("index.html", movies=all_movies)

"""After selected a new movie or an existent movie is posible to change through a Form rate and review  in the local 
database"""
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

"""Delete movie from the local database """
@app.route('/delete')
def delete_movie():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

"""Seach in the database for a the title of a movie and rendre a selecrtion of movies where is relevant the searched Title"""
@app.route('/add',methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    if form.validate_on_submit():
        search_title = form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": search_title})
        data = response.json()['results']
        return render_template("select.html", options=data)
    return render_template('add.html', form=form)

"""find movie : in the db through API requests after been selected and add it to the local database"""
@app.route('/find', methods=['GET','POST'])
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_API_KEY, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("rate_movie", id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
