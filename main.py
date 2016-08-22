'''.'''

import os
from ConfigParser import ConfigParser
from movie_data.MovieData import MovieData
from movie_data.Api import HboApi, MovieDataApi


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

    # Make a backup of the current file
    create_backup(out_file)

    # Write out a new movie data file
    fh_out = open(out_file, 'w')
    for imdb_id in movie_data:
        data_string = movie_data.get_data_string(imdb_id)
        try:
            fh_out.write('%s\n' % (data_string))
        except UnicodeEncodeError:
            fh_out.write('%s\n' % (data_string.encode('utf-8')))

    fh_out.close()

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


def create_backup(file_name):
    '''
    Renames file_name to allow a new file to be made with the same name

    :param file_name:  String - Name of a file

    :return:  None
    '''

    try:
        backup_file = '%s~' % (file_name)
        os.rename(file_name, backup_file)
    except OSError:
        # File not found, skip renaming
        pass

if __name__ == '__main__':
    main()
