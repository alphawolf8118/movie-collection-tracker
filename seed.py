# seed.py
from app import app, db, auto_seed

with app.app_context():

    # Pirates of the Caribbean (5 movies)
    auto_seed("Pirates of the Caribbean", [
        ("The Curse of the Black Pearl", "2003-07-09"),
        ("Dead Man's Chest", "2006-07-07"),
        ("At World's End", "2007-05-25"),
        ("On Stranger Tides", "2011-05-20"),
        ("Dead Men Tell No Tales", "2017-05-26"),
    ])

    # Middle-earth (Peter Jackson’s 6-film saga)
    auto_seed("Middle-earth", [
        ("The Fellowship of the Ring", "2001-12-19"),
        ("The Two Towers", "2002-12-18"),
        ("The Return of the King", "2003-12-17"),
        ("An Unexpected Journey", "2012-12-14"),
        ("The Desolation of Smaug", "2013-12-13"),
        ("The Battle of the Five Armies", "2014-12-17"),
    ])

    # DC Extended Universe (DCEU) – theatrical order
    auto_seed("DC Extended Universe", [
        ("Man of Steel", "2013-06-14"),
        ("Batman v Superman: Dawn of Justice", "2016-03-25"),
        ("Suicide Squad", "2016-08-05"),
        ("Wonder Woman", "2017-06-02"),
        ("Justice League", "2017-11-17"),
        ("Aquaman", "2018-12-21"),
        ("Shazam!", "2019-04-05"),
        ("Birds of Prey", "2020-02-07"),
        ("Wonder Woman 1984", "2020-12-25"),
        ("The Suicide Squad", "2021-08-06"),
        ("Black Adam", "2022-10-21"),
        ("Shazam! Fury of the Gods", "2023-03-17"),
        ("The Flash", "2023-06-16"),
        ("Blue Beetle", "2023-08-18"),
        ("Aquaman and the Lost Kingdom", "2023-12-22"),
    ])

    print("\nAll collections seeded successfully!")

    auto_seed("DC Elseworlds", [
        ("Joker", "2019-10-04"),
        ("The Batman", "2022-03-04"),
        ("Joker: Folie à Deux", "2024-10-04"),
        ("Aztec Batman: Clash of Empires", "2025-09-18"),   # animated
        ("The Batman Part II", "2027-10-01"),
    ])

    # DC Universe – main connected universe (Gunn/Safran)
    # Only films with confirmed exact release dates
    auto_seed("DC Universe", [
        ("Superman", "2025-07-11"),          # already released — you can check it off!
        ("Supergirl: Woman of Tomorrow", "2026-06-26"),
        ("Clayface", "2026-09-11"),
    ])

    print("\nDC Elseworlds and DC Universe collections seeded perfectly!")
    print("   • DC Elseworlds: 5 movies (Joker, The Batman, etc.)")
    print("   • DC Universe: 3 movies (Superman, Supergirl, Clayface)")

    auto_seed("Dark Knight Trilogy", [
        ("Batman Begins", "2005-06-15"),
        ("The Dark Knight", "2008-07-18"),
        ("The Dark Knight Rises", "2012-07-20"),
    ])

    auto_seed("Avatar", [
        ("Avatar", "2009-12-18"),
        ("Avatar: The Way of Water", "2022-12-16"),
        ("Avatar: Fire and Ash", "2025-12-19"),
    ])