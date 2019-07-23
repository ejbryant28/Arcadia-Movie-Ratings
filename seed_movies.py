from model import User, Rating, Movie, connect_to_db, db

from server import app

from datetime import datetime

def load_movies(movie_filename):
    """Load movies from u.item into database."""

    print("Movies")

    with open(movie_filename) as f:
        for line in f:
            line = line.rstrip()

            movie_id, title, released_str, junk, imdb_url = line.split("|")[:5]

            # convert date to datetime
            if released_str:
                released_date = datetime.strptime(released_str, "%d-%b-%Y")
            else:
                released_date = None

            #remove year from end of title
            title = title[:-7]

            movie = Movie(title = title, imdb_url = imdb_url)

            db.session.add(movie)

        db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    print('connected to db')
    load_movies('movies.item')
    print('loaded movies')

