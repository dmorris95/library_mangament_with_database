#Module for input validation
import book, author, user, genre #import classes for validation
import re
import database_functions

isbn_pattern = r"\d{13}"

#Create a new book
def book_create(cursor):
    publish_pattern = r"\d{4}-(0?[1-9]|1[0-2])-([012]\d|30|31)" #pattern matching for year, month, and day

    title_inp = input("Please enter the title of the new book you would like to add: ")
    while title_inp == "":
        title_inp = input("Please enter the title of the new book you would like to add: ")
    auth_inp = input("Please enter the name of the author of the book: ")
    while auth_inp == "":
        auth_inp = input("Please enter the author of the book: ")
    #database check
    if database_functions.author_check(auth_inp, cursor) == False:
        print("That Author is not in the database yet, try adding them first")
        return []

    isbn_inp = input("Please enter the ISBN of the book you would like to add: ")
    while True:
        if re.match(isbn_pattern, isbn_inp):
            if database_functions.isbn_check(isbn_inp, cursor) != False:
                isbn_inp = input("Please enter the unique ISBN of the book: ")
            else:
                break
        else:
            isbn_inp = input("Please enter the ISBN of the book(13 digit unique number): ")

    genre_inp = input("Please enter the genre of the book: ")
    while genre_inp == "":
        genre_inp = input("Please enter the genre of the book: ")
    #database check
    if database_functions.genre_check(genre_inp, cursor) == False:
        print("This genre is not in the database yet, please try adding the genre first!")
        return []

    publish_inp = input("Please enter the publish date of the book(yyyy-mm-dd): ")
    while True:
        if re.match(publish_pattern, publish_inp):
            break
        else:
            publish_inp = input("Please enter the publish date of the book(yyyy-mm-dd): ")
    
    #if statements to determine if the book needs to be put in a special category
    if genre_inp.lower == "fiction":
        new_book = book.FictionBook(title_inp, auth_inp, isbn_inp, genre_inp, publish_inp)
    elif genre_inp.lower == "mystery":
        new_book = book.MysteryBook(title_inp, auth_inp, isbn_inp, genre_inp, publish_inp)
    elif genre_inp.lower == "nonfiction":
        new_book = book.NonfictionBook(title_inp, auth_inp, isbn_inp, genre_inp, publish_inp)
    else:
        new_book = book.Book(title_inp, auth_inp, isbn_inp, genre_inp, publish_inp)

    #when all input is valid, return the new book object
    return new_book

#Book search function
def book_search(cursor):
    isbn_input = input("Please enter the ISBN of the book you would like more information on: ")
    while True:
        if re.match(isbn_pattern, isbn_input):
            break
        else:
            isbn_input = input("Please enter the ISBN of the book you would like more information on: ")
    result = database_functions.book_search_sql(isbn_input, cursor)

    if result == []:
        print("Sorry that book was not found in the library.")
    else:
        found_book = book.Book(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
        if result[0][5] == 0:
            found_book.change_availability()
        print(found_book)
    
#Create a new User
def new_user(cursor):
    id_pattern = r"\d{10}"
    name_input = input("Please enter the name of the new user: ")
    while name_input == "":
        name_input = input("Please enter the name of the new user: ")
    id_input = input("Please enter a library ID number for the user: ")
    while True:
        if re.match(id_pattern, id_input):
            #database check for unique library id
            if database_functions.library_id_check(id_input, cursor) != False:
                print("This Library ID is already in the system, please try again.")
            else:
                break
        else:
            id_input = input("Please enter a valid library ID: ")
    #once input is valid, add user to database
    new_user = user.User(name_input, id_input)
    database_functions.add_user(new_user, cursor)


    

#Borrow Book Function
def borrow_book(cursor):
    id_pattern = r"\d{10}"

    library_id_input = input("Please enter the user's library ID: ")
    while True:
        if re.match(id_pattern, library_id_input):
            break
        else:
            library_id_input = input("Enter the library ID in a proper format(only numbers): ")

    book_isbn = input("Please enter the book's ISBN they are borrowing: ")
    while True:
        if re.match(isbn_pattern, book_isbn):
            break
        else:
            book_isbn = input("Please enter the book's ISBN(13 digit number): ")
    return database_functions.borrow_book(library_id_input, book_isbn, cursor)


#Return book function
def return_book(cursor):
    id_pattern = r"\d{10}"
    library_id_input = input("Please enter the user's library ID: ")
    while True:
        if re.match(id_pattern, library_id_input):
            break
        else:
            library_id_input = input("Please enter the user's library ID: ")
    
    book_isbn = input("Please enter the book's ISBN they are returning: ")
    while True:
        if re.match(isbn_pattern, book_isbn):
            break
        else:
            book_isbn = input("Please enter the book's ISBN they are returning: ")

    #database function
    return database_functions.return_book(library_id_input, book_isbn, cursor)

#User search function
def search_user(cursor):
    id_pattern = r"\d{10}"
    id_input = input("Please enter the ID of the user you would like to view: ")
    while True:
        if re.match(id_pattern, id_input):
            if database_functions.library_id_check(id_input, cursor) != False:
                break
            else:
                id_input =input("That library id is not in the system, please try again: ")
        else:
            id_input = input("Please enter a valid ID")
    database_functions.search_user(id_input, cursor)
    
#add Author function
def add_author(cursor):
    author_name = input("Please enter the name of the new author: ")
    while True:
        if database_functions.author_check(author_name, cursor) != False: #Database check for existing author
            author_name = input("That author already exists, please try a different author's name: ")
        elif author_name == "":
            author_name = input("Please enter the author's name: ")
        else:
            break
    
    author_bio = input("Please enter a short bio of the author: ")
    while author_bio == "":
        author_name = input("Please enter a short bio for the author: ")
    
    new_author = author.Author(author_name, author_bio) #populate class
    return new_author


#Author search function
def search_author(cursor):
    find_author = input("Please enter the Author you would like more details on: ")
    while find_author == "":
        find_author = input("Please enter the name of the Author you would like more details on: ")
    if database_functions.author_check(find_author, cursor) == False:
        print("Sorry that author is not in the database.")
    else:
        database_functions.search_author(find_author, cursor)

#Add genre function
def add_genre(cursor):
    genre_name = input("Please enter the name of the genre: ")
    while True:
        if genre_name == "":
            genre_name = input("Please enter the name of the genre: ")
        elif database_functions.genre_check(genre_name, cursor) != False: #database check for existing genre
            genre_name = input("That genre already exists in the database. Please enter a different genre: ")
        else:
            break
    
    genre_desc = input("Enter a short description of the genre: ")
    while genre_desc == "":
        genre_desc = input("Please enter a short description of the genre: ")

    genre_cat = input("Please enter the cateogry this genre falls under: ")
    while genre_cat == "":
        genre_cat = input("Please enter the category this genre falls under: ")

    new_genre = genre.Genre(genre_name, genre_desc, genre_cat)
    return new_genre

#Genre search function
def search_genre(cursor):
    find_genre = input("Please enter the Genre you would like more details on: ")
    while find_genre == "":
        find_genre = input("Please enter the name of the Genre you would like more details on: ")
    if database_functions.genre_check(find_genre, cursor) == False:
        print("Could not find genre, Try adding to the library first!")
    else:
        database_functions.search_genre(find_genre, cursor)
