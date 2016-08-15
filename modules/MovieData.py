'''.'''

import os
from HboMovieData.modules.Api import ImdbApi


class MovieData(object):
    ''' Stores movie metadata to a file and provides access to the data '''

    def __init__(self, fileName=None):
        self.__file_name = fileName
        self.__parse_file()
        self.__imdb_api = ImdbApi()

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        for imdb_id in sorted(
                self.__data,
                key=lambda imdb_id: float(self.__data[imdb_id]['imdbRating']),
                reverse=True,
            ):
            yield imdb_id

    def update_status(self, imdb_id, status):
        '''
        Updates the status of the IMDB entry

        :param imdb_id:  String - IMDB identifier, eg, tt0090605
        :param status:  String - The new status of the IMDB entry

        :return:  None
        '''
        try:
            self.__data[imdb_id]['status'] = status
        except KeyError as error:
            raise KeyError('Invalid IMDB identifier specified: %s' % (error))

    def update_file(self):
        '''
        Creates a new file with all the movie entries and their metadata

        :param:  None

        :return:  None
        '''

        self.__create_backup()

        fh_out = open(self.__file_name, 'w')
        for imdb_id in self:

            try:
                fh_out.write(
                    '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
                        self.__data[imdb_id]['title'],
                        self.__data[imdb_id]['year'],
                        self.__data[imdb_id]['genre'],
                        self.__data[imdb_id]['actors'],
                        self.__data[imdb_id]['plot'],
                        self.__data[imdb_id]['imdbRating'],
                        self.__data[imdb_id]['metacritic'],
                        self.__data[imdb_id]['status'],
                        imdb_id,
                        self.__imdb_api.get_url(imdb_id),
                    )
                )
            except UnicodeEncodeError:
                fh_out.write(
                    '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
                        self.__data[imdb_id]['title'].encode('utf-8'),
                        self.__data[imdb_id]['year'].encode('utf-8'),
                        self.__data[imdb_id]['genre'].encode('utf-8'),
                        self.__data[imdb_id]['actors'].encode('utf-8'),
                        self.__data[imdb_id]['plot'].encode('utf-8'),
                        self.__data[imdb_id]['imdbRating'].encode('utf-8'),
                        self.__data[imdb_id]['metacritic'].encode('utf-8'),
                        self.__data[imdb_id]['status'].encode('utf-8'),
                        imdb_id.encode('utf-8'),
                        self.__imdb_api.get_url(imdb_id.encode('utf-8')),
                    )
                )

        fh_out.close()

    def exists(self, imdb_id):
        '''
        Returns boolean if the imdb_id has been loaded into an instance of this class

        :imdb_id String:  Imdb identifier, eg, tt0090605

        :return Boolean:  Has the identifier been loaded
        '''
        return imdb_id in self.__data

    def add(self, **kwargs):
        '''
        Adds a new movie entry with the user's arguments

        :return:  None
        '''

        self.__data[kwargs['imdb_id']] = {
            'imdbId': kwargs['imdb_id'],
            'title': kwargs['title'],
            'imdbRating': kwargs['imdb_rating'],
            'metacritic': kwargs['metacritic'],
            'year': kwargs['year'],
            'genre': kwargs['genre'],
            'actors': kwargs['actors'],
            'plot': kwargs['plot'],
            'status': kwargs['status'],
        }

    def __parse_file(self):
        # Internal data structure
        self.__data = {}

        try:
            fh_in = open(self.__file_name, 'rU')
            for line in fh_in:
                file_data = line.rstrip().split('\t')
                self.add(
                    imdb_id=file_data[8],
                    title=file_data[0],
                    imdb_rating=file_data[5],
                    metacritic=file_data[6],
                    year=file_data[1],
                    genre=file_data[2],
                    actors=file_data[3],
                    plot=file_data[4],
                    status='Deleted',  # Assume all these movies are no longer available.
                )
            fh_in.close()
        except TypeError:
            # No file specified, skip parsing
            pass
        except IOError:
            # Older file not found, skip parsing
            pass

    def __create_backup(self):
        try:
            backup_file = '%s~' % (self.__file_name)
            os.rename(self.__file_name, backup_file)
        except OSError:
            # File not found, skip renaming
            pass
