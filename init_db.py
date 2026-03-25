# init_db.py
from app import app, db, Collection, Movie
from datetime import datetime

def seed_data():
    mcu = Collection(name="Marvel Cinematic Universe")
    db.session.add(mcu)
    db.session.commit()

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

    for title, date_str in movies:
        movie = Movie(
            name=title,
            release_date=datetime.strptime(date_str, "%Y-%m-%d").date(),
            collection_id=mcu.id
        )
        db.session.add(movie)
    db.session.commit()

with app.app_context():
    db.create_all()
    if Collection.query.count() == 0:
        print("Database created – now seeding Marvel Cinematic Universe (34 movies)...")
        seed_data()
        print("All done! MCU is ready.")
    else:
        print("Database already exists – nothing done.")