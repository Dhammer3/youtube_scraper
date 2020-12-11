global_var='k'

class df_obj:
    def __init__(self, filename):
        self.__filename=filename
    def get_filename(self):
        return self.__filename
    def set_filename(self, filename):
        self.__filename=filename
    