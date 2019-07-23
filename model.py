from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

########################################################################
#Data tables

class User(db.Model):
    """User of website"""
    #TODO: Hash passwords

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(64), nullable = False, unique = True)
    password = db.Column(db.String(64), nullable = False)

    def __repr__(self):
        """Provide more useful info when printed"""
        
        return "<User user_id= {} username = {}>".format(self.user_id, self.username)


class Movie(db.Model):
    """Movie from IMDB stored in website"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    title = db.Column(db.String(200), nullable = False) #, unique = True)
    release_date = db.Column(db.DateTime, nullable = True)
    imdb_url = db.Column(db.String(200), nullable = True) #, unique = True)

    def __repr__(self):
        """Provide more useful info when printed"""

        return "<Movie title= {}>".format(self.title)

class MetaMovieList(db.Model):
    """ List of movies for one particular user """

    __tablename__ = "meta_movie_lists"

    list_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    list_name = db.Column(db.String(100), nullable = False)

    user = db.relationship("User", backref=db.backref("user", order_by=user_id))


    def __repr__(self):
        """Provide more useful info when printed"""

        return "<MetaMovieList list_id = {} list_name = {}>".format(self.list_id, self.list_name)

class InstanceMovieList(db.Model):
    """ The instance of one movie being on a list """

    __tablename__ = "instance_movie_list"

    instance_id = db.Column(db.Integer, primary_key = True)
    list_id = db.Column(db.Integer, db.ForeignKey('meta_movie_lists.list_id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))

    def __repr__(self):
        """Provide more useful info when printed"""

        return "<InstanceMovieList list_id = {} movie_id = {}>".format(self.movie_id, self.movie_id)

class Rating(db.Model):
    """Rating from a user for a movie"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer, nullable=False)

    movie = db.relationship("Movie", backref=db.backref("ratings", order_by=rating_id))
    user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Provide more useful info when printed"""

        return "<Rating rating_id = {} user_id = {} movie_id = {}>".format(self.rating_id, self.user_id, self.movie_id)



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

    
if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
