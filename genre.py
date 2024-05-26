
class Genre:
    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category

    def display_genre(self):
        print(f"Genre Name: {self.name}\nDescription: {self.description}")
        print(f"Genre's Category: {self.category}")