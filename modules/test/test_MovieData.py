'''.'''  #pylint: disable=invalid-name

import unittest
from HboMovieData.modules.MovieData import MovieData


class TestMovieData(unittest.TestCase):
    ''' Test the MovieData class '''

    def setUp(self):
        ''' Runs this before all tests '''
        self.movie_data = MovieData()

    def test_missing_file(self):
        ''' Make sure exception is checked but passed for missing file '''
        obj = MovieData('missing_file.txt')
        self.assertEqual(
            len(obj),
            0,
        )

    def test_len_empty(self):
        ''' Test the len function on the object '''
        self.assertEqual(
            len(self.movie_data),
            0,
        )

    def test_iter(self):
        ''' Load movies and make sure the iterator returns the movies in the correct order '''
        self.__add_movies()
        imdbList = list(self.movie_data)
        self.assertListEqual(
            imdbList,
            ['tt0110912', 'tt0090605', 'tt0268978'],
        )

    def test_update_status(self):
        ''' Ensure invalid IMDB identifier raises a KeyError exception '''
        with self.assertRaises(KeyError):
            self.movie_data.update_status('invalid_id', 'Ok')

    def test_exists_false(self):
        ''' Validate that invalid keys do not exist. '''
        self.assertFalse(self.movie_data.exists('invalid_id'))

    def test_exists_true(self):
        ''' Add data to the object and validate that it exists. '''
        self.__add_movies()
        self.assertTrue(self.movie_data.exists('tt0090605'))

    def __add_movies(self):
        dataList = [
            {
                'imdb_id': 'tt0268978',
                'title': 'A Beautiful Mind',
                'imdb_rating': '8.2',
                'metacritic': '72',
                'year': '2001',
                'genre': 'Biography, Drama',
                'actors': 'Russell Crowe, Ed Harris, Jennifer Connelly, Christopher Plummer',
                'plot': 'After John Nash, a brilliant but asocial mathematician, accepts secret ' \
                        'work in cryptography, his life takes a turn for the nightmarish.',
                'status': 'New',
            },
            {
                'imdb_id': 'tt0110912',
                'title': 'Pulp Fiction',
                'imdb_rating': '8.9',
                'metacritic': '94',
                'year': '1994',
                'genre': 'Crime, Drama',
                'actors': 'Tim Roth, Amanda Plummer, Laura Lovelace, John Travolta',
                'plot': 'The lives of two mob hit men, a boxer, a gangster\'s wife, and a ' \
                        'pair of diner bandits intertwine in four tales of violence and redemption.',
                'status': 'New',
            },
            {
                'imdb_id': 'tt0090605',
                'title': 'Aliens',
                'imdb_rating': '8.4',
                'metacritic': '87',
                'year': '1986',
                'genre': 'Action, Adventure, Sci-Fi',
                'actors': 'Sigourney Weaver, Carrie Henn, Michael Biehn, Paul Reiser',
                'plot': 'The planet from Alien (1979) has been colonized, but contact is lost. ' \
                        'This time, the rescue team has impressive firepower, but will it be enough?',
                'status': 'New',
            },
        ]

        for data in dataList:
            self.movie_data.add(**data)


if __name__ == '__main__':
    unittest.main()
