
class User:
    def __init__(self, name, library_id):
        self.__name = name
        self.__library_id = library_id
        
    def get_user_name(self):
        return self.__name
    def set_user_name(self, user_name):
        self.__name = user_name

    def get_library_id(self):
        return self.__library_id
    def set_library_id(self, lib_id):
        self.__library_id = lib_id
        
    def display_user_info(self):
        print(f"Library ID: {self.get_library_id()}\nName: {self.get_user_name()}")

