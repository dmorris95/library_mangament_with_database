from book import Book, NonfictionBook, FictionBook, MysteryBook
from author import Author
from genre import Genre
from user import User
import input_validators, database_functions
import mysql.connector


def menu_display():
    try:
        menu_choice = 0
        print("Welcome to the Library Management System!")
        while menu_choice != 5:
            menu_choice = menu_input()
    except ValueError as e:
        print(e)
    finally:
        print("Thank you for using the Library Management System!")


def menu_input():

    try:
        main_menu_string = "1. Book Operations\n2. User Operations\n3. Author Operations\n4. Genre Operations\n5. Quit"
        print("Main Menu:")
        print (main_menu_string)
        user_choice = int(input("Please enter the number of the option you would like to perform: "))

        #Establish connection to database
        library_db = mysql.connector.connect(
            database = "your_db",
            host="hostname",
            user="root",
            password="your_password"
        )
        cursor = library_db.cursor()
        

        #Book Operations
        if user_choice == 1:
            print("Book Operations: ")
            print("1. Add a new book\n2. Borrow a book\n3. Return a book\n4. Search for a book by ISBN\n5. Display all books")
            book_choice = int(input("Please enter the number of the option you would like to select: "))
            if book_choice == 1: #Add a book
                new_book = input_validators.book_create(cursor)
                if new_book != []:
                    database_functions.add_book(new_book, cursor)
                    library_db.commit()
                    print("Book successfully added!")

            elif book_choice == 2: #Borrow a book
                if input_validators.borrow_book(cursor) == True:
                    library_db.commit()
 
            elif book_choice == 3: #Return a book
                if input_validators.return_book(cursor) == True:
                    library_db.commit()

            elif book_choice == 4: #Search for a book by isbn
                input_validators.book_search(cursor)
                    
            elif book_choice == 5: #Display all books
                print("The following books are in the library: ")
                database_functions.book_display_sql(cursor)

        #User Operations
        elif user_choice == 2:
            print("User Operations: ")
            print("1. Add a new user\n2. View user details\n3. Display all users")
            user_oper_choice = int(input("Please enter the number of the option you would like to select: "))
            if user_oper_choice == 1:
                input_validators.new_user(cursor)
                library_db.commit()
                print("User successfully added!")

            elif user_oper_choice == 2:
                input_validators.search_user(cursor)
                
            elif user_oper_choice == 3:
                print("The following users are in the library:")
                database_functions.display_users(cursor)

        #Author Operations    
        elif user_choice == 3:
            print("Author Operations: ")
            print("1. Add a new author\n2. View author details\n3. Display all authors")
            author_choice = int(input("Please enter the number of the option you would like to select: "))
            if author_choice == 1: #Add an Author 
                new_author = input_validators.add_author(cursor)
                database_functions.add_author(new_author, cursor) #add author to database
                library_db.commit()
                print("Author successfully added!")
            elif author_choice == 2: #Search for an Author
                input_validators.search_author(cursor)

            elif author_choice == 3: #Display list of Authors
                print("Authors in the library: ")
                database_functions.display_all_author(cursor)

        #Genre Operations    
        elif user_choice == 4:
            print("Genre Operations: ")
            print("1. Add a new genre\n2. View genre details\n3. Display all genres")
            genre_choice = int(input("Please enter the number of the option you would like to select: "))
            if genre_choice == 1: #add genre
                new_genre = input_validators.add_genre(cursor)
                database_functions.add_genre(new_genre, cursor)
                library_db.commit()
                print("Genre successfully added!")
            elif genre_choice == 2: #search for a specific genre
                input_validators.search_genre(cursor)
            elif genre_choice == 3: #Display list of Genres
                print("Genres in the library: ")
                database_functions.display_all_genre(cursor)

        elif user_choice == 5:
            return user_choice
        else:
            raise ValueError
    except ValueError:
        print("Please enter a valid number choice")
        menu_display()

menu_display()