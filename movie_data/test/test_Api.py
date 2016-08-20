'''.'''  #pylint: disable=invalid-name

import unittest
import mock
from movie_data.Api import ApiUrl, ImdbApi, HboApi, MovieDataApi


class TestApiUrl(unittest.TestCase):
    ''' Test the ApiUrl class '''

    def setUp(self):
        ''' Runs this before all tests '''
        self.api = ApiUrl()

    def test_get_url(self):
        ''' Test the get_url method using no arguments '''
        self.assertEqual(
            self.api.get_url(),
            'http://mySite.com/',
        )

    def test_get_url_with_path(self):
        ''' Test the get_url method using 1 argument '''
        class NewApi(ApiUrl):  # pylint: disable=too-few-public-methods
            ''' Testing child class '''
            PATH = '/api/%s/names/'

        api = NewApi()

        self.assertEqual(
            api.get_url('Hello'),
            'http://mySite.com/api/Hello/names/',
        )

    def test_get_url_with_paths(self):
        ''' Test the get_url method using 2 arguments of mixed type '''
        class NewApi(ApiUrl):  # pylint: disable=too-few-public-methods
            ''' Testing child class '''
            PATH = '/api/%s/names/%s/'

        api = NewApi()

        self.assertEqual(
            api.get_url('Hello', 3),
            'http://mySite.com/api/Hello/names/3/',
        )


class TestHboApi(unittest.TestCase):
    ''' Test the HboApi class '''

    def setUp(self):
        ''' Runs this before all tests '''
        api_key = 'fakekey'
        self.api = HboApi(api_key)

    @mock.patch('movie_data.Api.requests.get')
    def test_movies_iter(self, mock_get):
        # Mocks requests.get().json() to return a custom dictionary
        mock_get.return_value.json.return_value = {
            'total_results': 300,
            'total_returned': 2,
            'results': [
                {'imdb': 'tt0090605'},
            ],
        }
        self.assertListEqual(
            list(self.api.movies()),
            ['tt0090605', 'tt0090605'],
        )


class TestMovieDataApi(unittest.TestCase):
    ''' Test the MovieDataApi class '''

    def setUp(self):
        ''' Runs this before all tests '''
        self.api = MovieDataApi()

    def test_get_movie_data_exception(self):
        ''' Test the get_movie_data method without any arguments '''

        with self.assertRaises(Exception):
            self.api.get_movie_data()

    @mock.patch('movie_data.Api.requests.get')
    def test_get_movie_data(self, mock_get):

        ''' Test the get_movie_data method using imdb_id and movie arguments '''
        imdb_id = 'tt0090605'
        movie = 'Aliens'

        data = self.api.get_movie_data(imdb_id=imdb_id)
        mock_get.assert_called_with(
            'https://omdbapi.com/',
            params={'tomatoes': False, 'i': 'tt0090605'},
        )

        data = self.api.get_movie_data(movie=movie)
        mock_get.assert_called_with(
            'https://omdbapi.com/',
            params={'tomatoes': False, 't': 'Aliens'},
        )


class TestImdbApi(unittest.TestCase):
    ''' Test the ImdbApi class '''

    def setUp(self):
        ''' Runs this before all tests '''
        self.api = ImdbApi()

    def test_get_url(self):
        ''' Test get_url method with standard arguments '''
        self.assertEqual(
            self.api.get_url('tt0090605'),
            'http://www.imdb.com/title/tt0090605/',
        )
