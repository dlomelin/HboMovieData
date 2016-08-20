'''.'''

from movie_data.Api import ImdbApi


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
                key=lambda imdb_id: float(self.__data[imdb_id]['imdb_rating']),
                reverse=True,
            ):
            yield imdb_id

    def get_data(self, imdb_id):
        '''
        Returns movie metadata for the specified IMDB identifier

        :param imdb_id:  String - IMDB identifier, eg, tt0090605

        :return:  Dictionary - Movie metadata (title, year, score, ...)
        '''

        try:
            return self.__data[imdb_id]
        except KeyError as error:
            raise KeyError('No data found for IMDB identifier: %s' % (error))

    def get_data_string(self, imdb_id):
        '''
        Returns movie metadata for the specified IMDB identifier as a string.
        This string is guaranteed to be parseable by this module.

        :param imdb_id:  String - IMDB identifier, eg, tt0090605

        :return:  String - Movie metadata in tab delimited format
        '''

        data = self.get_data(imdb_id)

        string = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
            data['title'],
            data['year'],
            data['genre'],
            data['actors'],
            data['plot'],
            data['imdb_rating'],
            data['metacritic'],
            data['status'],
            data['imdb_id'],
            self.__imdb_api.get_url(data['imdb_id']),
        )

        return string

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

    def exists(self, imdb_id):
        '''
        Returns boolean if the imdb_id has been loaded into an instance of this class

        :param imdb_id:  String - Imdb identifier, eg, tt0090605

        :return:  Boolean - Has the identifier been loaded
        '''
        return imdb_id in self.__data

    def add(self, **kwargs):
        '''
        Adds a new movie entry with the user's arguments

        :return:  None
        '''

        self.__data[kwargs['imdb_id']] = {
            'imdb_id': kwargs['imdb_id'],
            'title': kwargs['title'],
            'imdb_rating': kwargs['imdb_rating'],
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
