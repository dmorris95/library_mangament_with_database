from author import Author
from genre import Genre
from user import User
from book import Book
import mysql.connector
from mysql.connector import Error

#checks
def author_check(auth, cursor):
    auth_sql = "SELECT id FROM authors WHERE name = %s"
    auth_tuple = (auth, )
    cursor.execute(auth_sql, auth_tuple)
    auth_id = cursor.fetchall()
    if auth_id == []:
        return False
    else:
        return auth_id
    
def isbn_check(isbn, cursor):
    isbn_sql = "SELECT * FROM books WHERE isbn = %s"
    isbn_tuple = (isbn, )
    cursor.execute(isbn_sql, isbn_tuple)
    isbn_id = cursor.fetchall()
    if isbn_id == []:
        return False
    else:
        return isbn_id
    
def genre_check(gen, cursor):
    genre_sql = "SELECT id FROM genres WHERE name = %s"
    genre_tuple = (gen, )
    cursor.execute(genre_sql, genre_tuple)
    genre_id = cursor.fetchall()
    if genre_id == []:
        return False
    else:
        return genre_id

def add_book(new_book, cursor):
    try:
        #get author id & genre id
        auth_check_sql = "SELECT id FROM authors WHERE name = %s"
        auth_tuple = (new_book.author, )
        cursor.execute(auth_check_sql, auth_tuple)
        auth_id = cursor.fetchone()[0]
        genr_check_sql = "SELECT id FROM genres WHERE name = %s"
        genre_tuple = (new_book.genre, )
        cursor.execute(genr_check_sql, genre_tuple)
        gen_id = cursor.fetchone()[0]

        book_info = new_book.title, auth_id, gen_id, new_book.isbn, new_book.publish_date
        add_sql = "INSERT INTO books (title, author_id, genre_id, isbn, publication_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(add_sql, book_info)
    except Error as e:
        print(e)
    
def borrow_book(library_id, isbn, cursor):
    try:
        #get user id
        get_id_sql = "SELECT id FROM users WHERE library_id = %s"
        library_tuple = (library_id, )
        cursor.execute(get_id_sql, library_tuple)
        user_id = cursor.fetchall()
        if user_id == []:
            print("Sorry this user does not exist yet!")
        else:
            #check if book is already being borrowed
            book_id_sql = "SELECT id, availability FROM books WHERE isbn = %s"
            isbn_tuple = (isbn, )
            cursor.execute(book_id_sql, isbn_tuple)
            book_id = cursor.fetchall()
            if book_id == []:
                print("Sorry this book is not in the library.")
            else:
                cursor.execute(book_id_sql, isbn_tuple)
                available = cursor.fetchone()[1]
                if available == 1:
                    #insert into table once all checks have been made
                    insert_sql = "INSERT INTO borrowed_books (user_id, book_id) VALUES (%s, %s)"
                    ids = user_id[0][0], book_id[0][0] 
                    cursor.execute(insert_sql, ids)
                    #update status
                    update_sql = "UPDATE books SET availability = '0' WHERE id = %s"
                    book_id_tuple = (book_id[0][0], )
                    cursor.execute(update_sql, book_id_tuple)
                    print("Book successfully borrowed!")
                    return True
                else:
                    print("Sorry that book is already being borrowed.")

    except Error as e:
        print(e)

def return_book(library_id, isbn, cursor):
    try:
        #get user id
        get_id_sql = "SELECT id FROM users WHERE library_id = %s"
        library_tuple = (library_id, )
        cursor.execute(get_id_sql, library_tuple)
        user_id = cursor.fetchall()
        if user_id == []:
            print("Sorry this user does not exist yet!")
        else:
            #check if book is being borrowed
            book_id_sql = "SELECT id, availability FROM books WHERE isbn = %s"
            isbn_tuple = (isbn, )
            cursor.execute(book_id_sql, isbn_tuple)
            book_id = cursor.fetchall()
            if book_id == []:
                print("Sorry this book is not in the library.")
            else:
                cursor.execute(book_id_sql, isbn_tuple)
                available = cursor.fetchone()[1]
                if available == 0:
                    #Delete from borrowed books table once all checks have been made
                    delete_sql = "DELETE FROM borrowed_books WHERE user_id = %s AND book_id = %s"
                    select_sql = "SELECT * FROM borrowed_books WHERE user_id = %s AND book_id = %s"
                    ids = user_id[0][0], book_id[0][0]
                    cursor.execute(select_sql, ids)
                    book_found = cursor.fetchall()
                    if book_found == []:
                        print("This user does not have this book in their possesion")
                    else:
                        cursor.execute(delete_sql, ids)
                        #update status
                        update_sql = "UPDATE books SET availability = '1' WHERE id = %s"
                        book_id_tuple = (book_id[0][0], )
                        cursor.execute(update_sql, book_id_tuple)
                        print("Book successfully returned!")
                        return True
                else:
                    print("Sorry that book has already been returned.")

    except Error as e:
        print(e)

def book_search_sql(isbn, cursor):
    try:
        search_sql = "SELECT b.title, a.name, b.isbn, g.name, b.publication_date, b.availability FROM books b, authors a, genres g WHERE b.author_id = a.id AND b.genre_id = g.id AND isbn = %s"
        isbn_tuple = (isbn, )
        cursor.execute(search_sql, isbn_tuple)
        found_book = cursor.fetchall()
        return found_book
    except Error as e:
        print(e)

def book_display_sql(cursor):
    try:
        select_all_sql = "SELECT title, isbn FROM books"
        cursor.execute(select_all_sql)
        books = cursor.fetchall()
        for book in books:
            print(f"Title: {book[0]}\nISBN: {book[1]}\n")
    except Error as e:
        print(e)


def library_id_check(library_id, cursor):
    library_sql = "SELECT id FROM users WHERE library_id = %s"
    libr_tuple = (library_id, )
    cursor.execute(library_sql, libr_tuple)
    lib_id = cursor.fetchall()
    if lib_id == []:
        return False
    else:
        return lib_id
    
def add_user(new_user, cursor):
    try:
        insert_sql = "INSERT INTO users (name, library_id) VALUES (%s, %s)"
        new_info = new_user.get_user_name(), new_user.get_library_id()
        cursor.execute(insert_sql, new_info)
    except Error as e:
        print(e)

def search_user(library_id, cursor): #search for user in the database by their library id
    try:
        user_info_sql = "SELECT u.name, u.library_id, b.title FROM books b, users u, borrowed_books c WHERE u.id = c.user_id AND b.id = c.book_id AND library_id = %s"
        library_tuple = (library_id, )
        cursor.execute(user_info_sql, library_tuple)
        user_info = cursor.fetchall()
        if len(user_info) > 1: #check if they have multiple books
            print(f"Name: {user_info[0][0]}, Library ID: {user_info[0][1]}")
            print("Books being borrowed:")
            for book in user_info: 
                print(book[2])
        elif len(user_info) == 1:
            print(f"Name: {user_info[0][0]}, Library ID: {user_info[0][1]}\nBook being borrowed: {user_info[0][2]}")
        else:
            print("That user has no books being borrowed at the moment.")
    except Error as e:
        print(e)

def display_users(cursor): #display all users in database
    try:
        show_users = "SELECT name, library_id FROM users"
        cursor.execute(show_users)
        users = cursor.fetchall()
        for user in users:
            print(f"Name: {user[0]}, Library ID: {user[1]}")
        print("\n")
    except Error as e:
        print(e)

def add_author(author, cursor):
    try:
        insert_sql = "INSERT INTO authors (name, biography) VALUES (%s, %s)"
        new_author = author.name, author.bio
        cursor.execute(insert_sql, new_author)
    except Error as e:
        print(e)

def display_all_author(cursor):
    try:
        show_authors = "SELECT name FROM authors"
        cursor.execute(show_authors)
        authors = cursor.fetchall()
        for auth in authors:
            print(auth[0])
        print("\n")
    except Error as e:
        print(e)

def add_genre(genre_inp, cursor):
    try:
        insert_sql = "INSERT INTO genres (name, description, category) VALUES (%s, %s, %s)"
        new_genre = genre_inp.name, genre_inp.description, genre_inp.category
        cursor.execute(insert_sql, new_genre)
    except Error as e:
        print(e)

def search_genre(genre_name, cursor):
    try:
        search_sql = "SELECT name, description, category FROM genres WHERE name = %s"
        genre_tuple = (genre_name, )
        cursor.execute(search_sql, genre_tuple)
        results = cursor.fetchall()
        if results == []:
            print("That genre does not exist yet, try adding them!")
        else:
            for x in results:
                found_genre = Genre(x[0], x[1], x[2])
                found_genre.display_genre()
    except Error as e:
        print(e)

def display_all_genre(cursor):
    try:
        show_genres = "SELECT name FROM genres"
        cursor.execute(show_genres)
        genres = cursor.fetchall()
        for gen in genres:
            print(gen[0])
        print("\n")
    except Error as e:
        print(e)


def search_author(auth_inp, cursor):
    try:
        search_sql = "SELECT name, biography FROM authors WHERE name = %s"
        auth_tuple = (auth_inp, )
        cursor.execute(search_sql, auth_tuple)
        results = cursor.fetchall()
        if results == []:
            print("That author does not exist yet, try adding them!")
        else:
            for x in results:
                found_auth = Author(x[0], x[1])
                found_auth.display_author()
    except Error as e:
        print(e)
