from jinja2 import StrictUndefined
from flask import (Flask, flash, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension
from model import Movie, User, MetaMovieList, InstanceMovieList, Rating, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "Supersecurepassword"
app.jinja_env.undefined = StrictUndefined

#################################################################################
#Routes

@app.route("/")
def index():
    """ Homepage """

    # new_list = MovieList(user_id = 1, list_name = 'test', movie_id = 1299)
    # db.session.add(new_list)
    # db.session.commit()

    return render_template("homepage.html")


@app.route('/new-user')
def add_user_form():
    """Show new user form"""

    return render_template("add_user.html")




@app.route('/login')
def login_page():
    """Show login form"""

    return render_template('login.html')


@app.route('/logout')
def logout_page():
    """Log user out"""

    return render_template('logout.html')

@app.route("/new-list")
def new_list_form():
    """ New List form"""

    movies = Movie.query.order_by('title').all()

    return render_template('new_list.html', movies = movies)


@app.route("/my-lists")
def user_lists():
    """ A user can see all their lists """

    user_id = session["user_id"]
    lists = MetaMovieList.query.filter(MetaMovieList.user_id == user_id).all()

    meta_lists = []
    for l in lists:
        movies = db.session.query(InstanceMovieList).join(Movie).filter(InstanceMovieList.list_id == l.list_id).all()
        meta_lists.append((l, len(movies)))

    return render_template('my_lists.html', meta_lists = meta_lists)

@app.route("/list/<list_name>")
def list_info(list_name):
    
    #TODO: Make this one big query with a lot of joins
    user_id = session["user_id"]
    list_id = MetaMovieList.query.filter(MetaMovieList.user_id == user_id, MetaMovieList.list_name == list_name).first().list_id
    movie_ids = InstanceMovieList.query.filter(InstanceMovieList.list_id == list_id).all()
    movies = []
    for _id in movie_ids:
        movie = Movie.query.filter(Movie.movie_id == _id.movie_id).first()
        rating = Rating.query.filter(User.user_id == user_id, Movie.movie_id == _id.movie_id).first()
        if rating:
            movies.append((movie, rating.score))
        else:
            movies.append((movie, None))

    return render_template("list_info.html", movies = movies)


########################################################################
#Functions

@app.route('/add_user', methods=["POST"])
def add_user():
    """Add new user to database."""
    

    username = request.form.get("username")
    password = request.form.get("password")

    username_match = User.query.filter(User.username == username).first()

    if username_match:
        flash('You already exist.')
        return redirect('/login')
    else:
        new_user = User(username = username, 
                        password = password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.user_id

        flash("You've been added!")

        return redirect('/')


@app.route('/login-do', methods=["POST"])
def user_login():
    """Log user in"""

    username = request.form.get('username')
    password = request.form.get('password')

    user_info = User.query.filter(User.username == username).first()

    if user_info is None:
        #flash you don't exist 
        flash("""You don't exist. Are you a ghost?
                Or did you type your username wrong?""")
        return redirect('/')

    elif user_info.password == password:
        # go to homepage
        flash("You're logged in!")
        
        session['user_id'] = user_info.user_id
        
        return redirect('/')

    else:
        flash("Wrong password. Try again. Be careful. Jeeeeezeeee")
        return redirect('/login')


@app.route('/logout-do')
def user_logout():
    """Log user out"""

    del session['user_id']

    flash("You're logged out. See you next time.")
    return redirect('/')


@app.route('/make-list', methods = ["POST"])
def make_list():
    """ create new list """

    list_name = request.form.get("list_name")
    movies = request.form.getlist("movies")
    user_id = session['user_id']

    new_list = MetaMovieList(user_id = user_id, list_name = list_name)
    db.session.add(new_list)
    db.session.commit()

    
    for movie_id in movies:

        new_instance = InstanceMovieList(list_id = new_list.list_id, movie_id = movie_id)
        db.session.add(new_instance)
        db.session.commit()

    return redirect('/')

@app.route('/add-rating', methods = ["POST"])
def add_rating(movie_id):
    """ add new rating to database """

    print("IT WORKED")
    user_id = session["user_id"]
    return redirect('/')
    # new_rating = Rating(movie_id = movie_id, score = score, user_id = user_id)
    # db.session.add(new_rating)
    # db.session.commit()



#######################################################################

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(port=5000, host='0.0.0.0')
