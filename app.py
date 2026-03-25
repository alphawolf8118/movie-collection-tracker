from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collections.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    movies = db.relationship('Movie', backref='collection', lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    collected = db.Column(db.Boolean, default=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)

# Create the DB (run this once in a Python shell or add to app)
with app.app_context():
    db.create_all()

def seed_data():
    mcu = Collection(name="Marvel Cinematic Universe")
    db.session.add(mcu)
    db.session.commit()  # Commit to get ID

    movies = [
        ("Iron Man", "2008-05-02"),
        ("The Incredible Hulk", "2008-06-13"),
        ("Iron Man 2", "2010-05-07"),
        ("Thor", "2011-05-06"),
        ("Captain America: The First Avenger", "2011-07-22"),
        ("The Avengers", "2012-05-04"),
        ("Iron Man 3", "2013-05-03"),
        ("Thor: The Dark World", "2013-11-08"),
        ("Captain America: The Winter Soldier", "2014-04-04"),
        ("Guardians of the Galaxy", "2014-08-01"),
        ("Avengers: Age of Ultron", "2015-05-01"),
        ("Ant-Man", "2015-07-17"),
        ("Captain America: Civil War", "2016-05-06"),
        ("Doctor Strange", "2016-11-04"),
        ("Guardians of the Galaxy Vol. 2", "2017-05-05"),
        ("Spider-Man: Homecoming", "2017-07-07"),
        ("Thor: Ragnarok", "2017-11-03"),
        ("Black Panther", "2018-02-16"),
        ("Avengers: Infinity War", "2018-04-27"),
        ("Ant-Man and the Wasp", "2018-07-06"),
        ("Captain Marvel", "2019-03-08"),
        ("Avengers: Endgame", "2019-04-26"),
        ("Spider-Man: Far From Home", "2019-07-02"),
        ("Black Widow", "2021-07-09"),
        ("Shang-Chi and the Legend of the Ten Rings", "2021-09-03"),
        ("Eternals", "2021-11-05"),
        ("Spider-Man: No Way Home", "2021-12-17"),
        ("Doctor Strange in the Multiverse of Madness", "2022-05-06"),
        ("Thor: Love and Thunder", "2022-07-08"),
        ("Black Panther: Wakanda Forever", "2022-11-11"),
        ("Ant-Man and the Wasp: Quantumania", "2023-02-17"),
        ("Guardians of the Galaxy Vol. 3", "2023-05-05"),
        ("The Marvels", "2023-11-10"),
        ("Deadpool & Wolverine", "2024-07-26"),
    ]

    for name, date_str in movies:
        release_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        movie = Movie(name=name, release_date=release_date, collection_id=mcu.id)
        db.session.add(movie)
    db.session.commit()

def auto_seed(collection_name, movie_list):
    """
    Usage example:
    auto_seed("Star Wars", [
        ("A New Hope", "1977-05-25"),
        ("The Empire Strikes Back", "1980-05-21"),
        ("Return of the Jedi", "1983-05-25"),
        # ... add the rest
    ])
    """
    from datetime import datetime

    existing = Collection.query.filter_by(name=collection_name).first()
    if existing:
        print(f'"{collection_name}" already exists — skipping')
        return

    coll = Collection(name=collection_name)
    db.session.add(coll)
    db.session.commit()

    for title, date_str in movie_list:
        movie = Movie(
            name=title,
            release_date=datetime.strptime(date_str, "%Y-%m-%d").date(),
            collected=False,
            collection_id=coll.id
        )
        db.session.add(movie)
    db.session.commit()
    print(f'"{collection_name}" seeded with {len(movie_list)} movies!')
# Run this once: with app.app_context(): seed_data()

@app.route('/')
def index():
    collections = Collection.query.all()
    # Which collection should stay open after a toggle?
    open_id = request.args.get('open', type=int)
    return render_template('index.html', collections=collections, open_id=open_id)

@app.route('/collection/<int:collection_id>')
def view_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    movies = collection.movies
    total = len(movies)
    collected_count = sum(1 for m in movies if m.collected)
    progress = (collected_count / total * 100) if total > 0 else 0
    return render_template('collection.html', collection=collection, movies=movies, progress=progress, collected_count=collected_count, total=total)

@app.route('/delete_collection/<int:collection_id>', methods=['POST'])
def delete_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    
    # Safety confirmation (optional but nice)
    if request.form.get('confirm') != 'yes':
        return "Cancelled", 400
    
    # Delete all movies first (cascade would be better, but this is safe)
    Movie.query.filter_by(collection_id=collection_id).delete()
    db.session.delete(collection)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/toggle/<int:movie_id>', methods=['POST'])
def toggle_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    movie.collected = not movie.collected
    db.session.commit()

    # If it's an HTMX request → return just the updated card
    if request.headers.get('HX-Request'):
        collection = movie.collection
        # Re-calculate progress for this collection only
        total = len(collection.movies)
        collected_count = sum(1 for m in collection.movies if m.collected)
        progress = round(collected_count / total * 100, 1) if total > 0 else 0
        open_id = collection.id  # keep card open
        return render_template('partials/card.html',
                               collection=collection,
                               progress=progress,
                               open_id=open_id)

    # Normal form submit fallback
    return redirect(url_for('index', open=movie.collection_id))

@app.route('/add_collection', methods=['GET', 'POST'])
def add_collection():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            collection = Collection(name=name)
            db.session.add(collection)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add_collection.html')

@app.route('/add_movie/<int:collection_id>', methods=['GET', 'POST'])
def add_movie(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    if request.method == 'POST':
        name = request.form['name']
        release_date_str = request.form['release_date']
        if name and release_date_str:
            try:
                release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
            except ValueError:
                release_date = None
            movie = Movie(name=name, release_date=release_date, collection_id=collection_id)
            db.session.add(movie)
            db.session.commit()
            return redirect(url_for('view_collection', collection_id=collection_id))
    return render_template('add_movie.html', collection=collection)

if __name__ == '__main__':
    app.run(debug=True, port=5001)