from src.models import db, Movie
def refresh_db():
    Movie.query.delete()
    db.session.commit()

def create_movie(title='Dune',director = 'Denis Villeneuve', rating = 5)->Movie:
    test_movie = Movie(title=title, director=director, rating=rating)
    db.session.add(test_movie)
    db.session.commit()
    return test_movie