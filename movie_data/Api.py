'''.'''

from urlparse import urlunparse
import requests


class ApiUrl(object):  # pylint: disable=too-few-public-methods
    ''' Provides a class to generate URLs for APIs '''

    SCHEME = 'http'
    HOST = 'mySite.com'
    PATH = '/'

    def get_url(self, *args):
        '''
        Returns a URL, using any path arguments if specified.

        :param args:  Variable - Each argument will get substituted into the URL

        :return:  String - Url
        '''
        url_data = (
            self.SCHEME,
            self.HOST,
            self.PATH % (args),
            '',
            '',
            '',
        )
        url = urlunparse(url_data)
        return url


class HboApi(ApiUrl):
    ''' Provides a class to fetch data from an API to retrieve HBO movies '''

    HOST = 'api-public.guidebox.com'
    PATH = 'v1.43/US/%s/movies/all/%s/%s/hbo/web'

    def __init__(self, apiKey):
        self.__apikey = apiKey
        self.__fetch_count = 250
        self.__set_start()

    def movies(self):
        '''
        Iterator that returns IMDB identifiers for all HBO movies.

        :param:  None

        :yield:  String - IMDB identifier, eg, tt0090605
        '''

        while True:
            # Fetch the movie data from the API in json format
            response = requests.get(
                self.get_url(
                    self.__apikey,
                    self.__start,
                    self.__fetch_count,
                ),
            )
            json_data = response.json()

            for moviedata in json_data['results']:
                # Only return movies with valid IMDB identifiers
                if moviedata['imdb']:
                    yield moviedata['imdb']

            # Quit if no more entries returned or next batch will not yield any new results
            # or if the json structure doesn't have a total_returned key (prevents infinite loop)
            newstart = self.__start + self.__fetch_count

            if newstart >= json_data['total_results'] or \
                'total_returned' not in json_data or \
                json_data['total_returned'] == 0:

                # Reset the counter
                self.__set_start()

                raise StopIteration
            else:
                # Set the new fetching coordinates for the next batch (updates url)
                self.__set_start(newstart)

    def __set_start(self, start=0):
        self.__start = start


class MovieDataApi(ApiUrl):
    ''' Provides a class to fetch movie data from the omdb API '''

    SCHEME = 'https'
    HOST = 'omdbapi.com'

    def get_movie_data(self, movie=None, imdb_id=None):
        '''
        Returns a dictionary with movie metadata such as title, year, actors, etc
        Note:  Either movie or imdb_id must be passed

        :param movie:  String - The name of a movie (optional)
        :param imdb_id:  String - The IMDB identifier, eg, tt0090605 (optional)

        :return:  Dictionary - Json structure with movie metadata
        '''

        payload = {
            'tomatoes': False,
        }
        if movie:
            payload['t'] = movie
        elif imdb_id:
            payload['i'] = imdb_id
        else:
            raise Exception('Valid arguments missing: set t for movie or i for imdb_id.')

        response = requests.get(self.get_url(), params=payload)

        return response.json()


class ImdbApi(ApiUrl):  # pylint: disable=too-few-public-methods
    ''' Provides a class to create URLs for the IMDB website '''

    HOST = 'www.imdb.com'
    PATH = '/title/%s/'
