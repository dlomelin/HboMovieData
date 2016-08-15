'''.'''  #pylint: disable=invalid-name

import unittest
from HboMovieData.modules.Api import ApiUrl, ImdbApi, MovieDataApi


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


class TestMovieDataApi(unittest.TestCase):
    ''' Test the MovieDataApi class '''

    def setUp(self):
        ''' Runs this before all tests '''
        self.api = MovieDataApi()

    def test_get_movie_data_exception(self):
        ''' Test the get_movie_data method without any arguments '''

        with self.assertRaises(Exception):
            self.api.get_movie_data()

    def test_get_movie_data(self):
        ''' Test the get_movie_data method using imdb_id and movie arguments '''
        imdb_id = 'tt0090605'
        movie = 'Aliens'

        data = self.api.get_movie_data(imdb_id=imdb_id)
        self.__validate_aliens_data(data, imdb_id, movie)

        data = self.api.get_movie_data(movie=movie)
        self.__validate_aliens_data(data, imdb_id, movie)

    def __validate_aliens_data(self, data, imdb_id, movie):
        self.assertEqual(
            data['Title'],
            movie,
        )
        self.assertEqual(
            data['Year'],
            '1986',
        )
        self.assertEqual(
            data['imdbID'],
            imdb_id,
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


if __name__ == '__main__':
    unittest.main()
