import functions


class Dataframe:
    _dataframe = None

    def get(self):
        if self._dataframe is None:
            self._dataframe = functions.open_file()

        return self._dataframe

    def __init__(self):
        self._dataframe = None