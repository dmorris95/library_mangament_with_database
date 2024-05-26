Welcome to the Library Management System With Database

This program builds upon a previous program built on classes and populated dictionaries. This program usees databases to more efficiently communicate and manipulate data within the program. It has a database that holds information on the books, users, authors, and genres. It also has an in between table that keeps track of each users borrowed books.

1. Within the book operations there are several different options:

    Adding a book allows the user to add a book into the library with the ISBN of the book being each books unique identifier
    Borrowing a book allows the user to input the library id of the user that is borrowing the book and then the ISBN of the book they are trying to borrow. It provides feedback accordingly and will add the book to the borrowed books table if all input is successful.
    Returning a book allows the user to input the library of the id of the user that is returning the book and the ISBN of the book that is being returned. It will return the book if user input is valid and remove the book from the borrowed books table.
    Searching for a book based on the ISBN of the book. Provides the user with more details such a genre, author, publish date, and whether the book is available.
    Displaying all books titles and their ISBN within the library.

2. User Operations has the following options:

    Adding a new user allows the user to add a new user with the library id being a unique identifier.
    Searching for a user based on their ID number shows which books the user has currently borrowed
    Displaying all users and their IDs

3. Author Operations has the following options:

    Adding a new author with their name being the unique identifer being their name.
    Searching for a specific author based on their name will show a short biography of the author.
    Displaying all authors names within the library

4. Genre Operations has the following options:

    Adding a new genre with the genre name being the unique identifier.
    Searching for a specific genre will provide a short description of the genre as well as the category the genre falls under.
    Displays all genres within the library

5. Quits the program