from flask.testing import FlaskClient
from src.models import Movie
from app import app
from tests.utils import create_movie, refresh_db

def test__get_all_movies(test_app: FlaskClient):
   


   
    refresh_db()
    test_movie = create_movie()

    res = test_app.get('/movies')
    page_data: str = res.data

    assert res.status_code== 200 
    assert f'<td><a href="/movies/(test_movie.movie_id)">Dune</a></td>' in page_data
    assert '<td>Denis Villeneuve</td>' in page_data
    assert '<td>5</td>' in page_data

def test__get_all_movies_empty(test_app: FlaskClient):
    refresh_db()
    res = test_app.get('/movies')
    page_data: str = res.data

    assert res.status_code == 200
    assert '<td>' not in page_data

def test__get_single_movie(test_app: FlaskClient):
    refresh_db()
    test_movie = create_movie()

    res = test_app.get(f'/movies{test_movie.movie_id}')
    page_data: str = res.data

    assert res.status_code == 200
    assert '<h1>Dune - 5</h1>' in page_data
    assert '<h2>Denis Villeneuve</h2>' in page_data

def test__get_single_movie_404(test_app: FlaskClient):
    refresh_db()
    res = test_app.get('/movies/1')

    assert res.status_code== 404

def test_create_movie(test_app: FlaskClient):
    refresh_db()

    res = test_app.post('/movies', data={
        'title': 'Dune',
        'director': 'Denis Villeneuve',
        'rating': 5
    
    }, follow_redirect = True)
    page_data = res.data.decode()
    assert res.status_code == 200
    assert '<h1>Dune - 5</h1>' in page_data
    assert '<h2>Denis Villeneuve</h2>' in page_data

    test_movie = Movie.query.filter_by(title = 'Dune').first()
    assert test_movie is not None
    assert test_movie.title =="Dune"
    assert test_movie.director =="Denis Villeneuve"
    assert test_movie.rating ==5

def test_create_movie_400(test_app:FlaskClient):
    refresh_db()
    res = test_app.post('/movies',data={},follow_redirect=True)

    assert res.status_code == 400