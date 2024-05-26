class Book:
    def __init__(self, title, author, isbn, genre, publish_date):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.publish_date = publish_date
        self.availability = "Available"

    #function to change availability based on if the user is returning the book or borrowing it
    def change_availability(self):
        if self.availability == "Available":
            self.availability = "Borrowed"
        else:
            self.availability = "Available"    
    
    #str function for when called to print
    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Genre: {self.genre}, Publish Date: {self.publish_date}, Availability: {self.availability}"
    

#Book SubClasses
class FictionBook(Book):
    def ___init__(self, title, author, isbn, genre, publish_date):
        super().__init__(title, author, isbn, genre, publish_date)

    def __str__(self):
        return f"This book is not based on facts, everything in this book is based a fictional events and characters: \nTitle: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Genre: {self.genre}, Publish Date: {self.publish_date}, Availability: {self.availability}"
    

class MysteryBook(Book):
    def __init__(self, title, author, isbn, genre, publish_date):
        super().__init__(title, author, isbn, genre, publish_date)
    
    def __str__(self):
        return f"This book has a shroud of mystery with twists and turns:\nTitle: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Genre: {self.genre}, Publish Date: {self.publish_date}, Availability: {self.availability}"
    

class NonfictionBook(Book):
    def __init__(self, title, author, isbn, genre, publish_date):
        super().__init__(title, author, isbn, genre, publish_date)
    
    def __str__(self):
        return f"This book is based on real events and is based in facts:\nTitle: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Genre: {self.genre}, Publish Date: {self.publish_date}, Availability: {self.availability}"

