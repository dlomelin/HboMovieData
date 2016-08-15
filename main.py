'''.'''

import os
from ConfigParser import ConfigParser
from HboMovieData.modules.MovieData import MovieData
from HboMovieData.modules.Api import HboApi, MovieDataApi


def main():
    ''' Queries HBO for its movies, looks up movie metadata, and writes it to a file '''

    # Instantiate API objects
    api_key = get_api_key(os.path.join('config', 'hboRatings.cfg'))
    hbo = HboApi(api_key)
    movies = MovieDataApi()

    # Instantiate movie data object to store movie metadata
    out_file = os.path.join('output', 'hboMovieRatings.txt')
    movie_data = MovieData(out_file)

    new_movie_count = 0
    # Iterate through all movies currently available on HBO GO
    for imdb_id in hbo.movies():

        # Check if the movie is new
        if movie_data.exists(imdb_id):
            # Movie is old so update it as such
            movie_data.update_status(imdb_id, 'Old')
        else:
            # Get the metadata for this new movie
            new_movie_count += 1
            data = movies.get_movie_data(imdb_id=imdb_id)

            print 'New movie added: %s %s %s' % (
                data['Title'],
                data['Year'],
                data['imdbRating'],
            )

            # Add it to the movie data store
            movie_data.add(
                imdb_id=imdb_id,
                title=data['Title'],
                imdb_rating=data['imdbRating'],
                metacritic=data['Metascore'],
                year=data['Year'],
                genre=data['Genre'],
                actors=data['Actors'],
                plot=data['Plot'],
                status='New',
            )

    # Write out a new movie data file
    movie_data.update_file()

    print '%s/%s new movies.' % (new_movie_count, len(movie_data))


def get_api_key(file_name):
    '''
    Parses the API key from the specified file.

    :param file_name:  String - Name of the config file

    :return:  String - The api key for the HBO api
    '''
    config = ConfigParser()
    config.read(file_name)
    api_key = config.get('hbo', 'api-key')
    return api_key


if __name__ == '__main__':
    main()
