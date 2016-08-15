import unittest
from HboMovieData.modules.Api import ApiUrl, ImdbApi, MovieDataApi


class TestApiUrl(unittest.TestCase):
    def setUp(self):
        self.apiObj = ApiUrl()

    def test_get_url(self):
        self.assertEqual(
            self.apiObj.get_url(),
            'http://mySite.com/',
        )

    def test_get_url_with_path(self):
        class NewApi(ApiUrl):
            PATH = '/api/%s/names/'

        apiObj = NewApi()

        self.assertEqual(
            apiObj.get_url('Hello'),
            'http://mySite.com/api/Hello/names/',
        )

    def test_get_url_with_paths(self):
        class NewApi(ApiUrl):
            PATH = '/api/%s/names/%s/'

        apiObj = NewApi()

        self.assertEqual(
            apiObj.get_url('Hello', 3),
            'http://mySite.com/api/Hello/names/3/',
        )


class TestMovieDataApi(unittest.TestCase):
    def setUp(self):
        self.apiObj = MovieDataApi()

    def test_get_movie_data(self):
        imdb_id = 'tt0090605'
        movie = 'Aliens'

        data = self.apiObj.get_movie_data(imdb_id=imdb_id)
        self.__validateAliensData(data, imdb_id, movie)

        data = self.apiObj.get_movie_data(movie=movie)
        self.__validateAliensData(data, imdb_id, movie)

    def __validateAliensData(self, data, imdb_id, movie):
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
    def setUp(self):
        self.apiObj = ImdbApi()

    def test_get_url(self):
        self.assertEqual(
            self.apiObj.get_url('tt0090605'),
            'http://www.imdb.com/title/tt0090605/',
        )


if __name__ == '__main__':
    unittest.main()
