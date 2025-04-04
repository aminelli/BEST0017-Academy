import json
import re

def add_book (books: list, title: str, author: str, year: int, available: bool = True):
    '''
    Adds a new book to the list.
    
    Parameters:
    books: List of dictionaries containing book information.
    title: Title of the book.
    author: Author of the book.
    year: Year of publication.
    '''
    book = {
        'id': len(books) + 1,
        'title': title,
        'author': author,
        'year': year,
        'available': available
    }
    books.append(book)
    print(f"Book '{title}' added to the catalogue.\n")

def show_catalogue (books: list, sorting: str = None):
    '''
    Displays the catalogue of books.
    
    Parameters:
    books: List of dictionaries containing book information.
    '''
    if not books:
        print("No books available in the catalogue.\n")
        return
    if sorting == 'title':
        books.sort(key=lambda x: x['title'])
    elif sorting == 'author':
        books.sort(key=lambda x: x['author'])
    elif sorting == 'year':
        books.sort(key=lambda x: x['year'])
    else:
        books.sort(key=lambda x: x['id'])
    print("Catalogue:")
    for book in books:
        print(f"{book['id']}: '{book['title']}' by {book['author']} ({book['year']}) - {'Available' if book['available'] else 'Unavailable'}")

def lend_book (books: list, book_id: int):
    '''
    Marks a book as lent out.
    
    Parameters:
    books: List of dictionaries containing book information.
    book_id: ID of the book to be lent out.
    '''
    if 0 < book_id <= len(books):
        if books[book_id - 1]['available']:
            books[book_id - 1]['available'] = False
            print(f"You have lent out '{books[book_id - 1]['title']}'.\n")
        else:
            print(f"'{books[book_id - 1]['title']}' is already lent out.\n")
    else:
        print("Invalid book ID. Please try again.\n")

def return_book (books: list, book_id: int):
    '''
    Marks a book as returned.
    
    Parameters:
    books: List of dictionaries containing book information.
    book_id: ID of the book to be returned.
    '''
    if 0 < book_id <= len(books):
        if not books[book_id - 1]['available']:
            books[book_id - 1]['available'] = True
            print(f"You have returned '{books[book_id - 1]['title']}'.\n")
        else:
            print(f"'{books[book_id - 1]['title']}' was not lent out.\n")
    else:
        print("Invalid book ID. Please try again.\n")

def find_book (books: list, search_term: str, regex: bool = False):
    '''
    Searches for a book by title or author.
    
    Parameters:
    books: List of dictionaries containing book information.
    search_term: Term to search for in the title or author.
    '''
    print("Search Results:")
    if not books:
        print("No books available in the catalogue.\n")
        return
    if regex:
        pattern = re.compile(search_term[3:], re.IGNORECASE)
        for book in books:
            if pattern.search(book['title']) or pattern.search(book['author']):
                print(f"{book['id']}: '{book['title']}' by {book['author']} ({book['year']}) - {'Available' if book['available'] else 'Unavailable'}")
    else:
        for book in books:
            if any(search_term.lower() in book[field].lower() for field in ('title', 'author')):
                print(f"{book['id']}: '{book['title']}' by {book['author']} ({book['year']}) - {'Available' if book['available'] else 'Unavailable'}")

def export_data (books: list, file_path: str):
    '''
    Saves the list of books to a JSON file. 

    Parameters:
    books: List of dictionaries containing book information.
    file_path: Path to the JSON file where the data will be saved.
    '''
    try:
        with open(file_path, 'w') as file:
            json.dump(books, file, indent=4)
        print(f"Data exported to file path successfully.\n")
    except IOError:
        print(f"Error writing to the specified file. Please check the file path and permissions.\n")


def import_data (file_path: str) -> list:
    '''
    Loads book data from a JSON file.

    Parameters:
    file_path: Path to the JSON file containing book information.

    Returns:
    List of dictionaries containing book information.
    '''
    try:
        with open(file_path, 'r') as file:
            books = json.load(file)
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Returning empty list.")
        return []
    
def show_statistics (books: list):
    '''
    Displays statistics about the books.

    Parameters:
    books: List of dictionaries containing book information.
    '''
    total_books = len(books)
    available_books = len([book for book in books if book['available']])
    lent_books = total_books - available_books
    print(f"Total books: {total_books}")
    print(f"Available books: {available_books}")
    print(f"Lent books: {lent_books}\n")



bookshelf = []
add_book(bookshelf, "1984", "George Orwell", 1949, available=False)
add_book(bookshelf, "The Lord of the Rings", "J.R.R. Tolkien", 1954)
add_book(bookshelf, "To Kill a Mockingbird", "Harper Lee", 1960)
add_book(bookshelf, "The Great Gatsby", "F. Scott Fitzgerald", 1925, available=False)
add_book(bookshelf, "Pride and Prejudice", "Jane Austen", 1813)
add_book(bookshelf, "War and Peace", "Leo Tolstoy", 1869, available=False)
add_book(bookshelf, "The Hobbit", "J.R.R. Tolkien", 1937)
add_book(bookshelf, "Fahrenheit 451", "Ray Bradbury", 1953)
add_book(bookshelf, "Brave New World", "Aldous Huxley", 1932)

while True:
    try:
        selection = int(input(
            "Select an option:\n\
            1. Add book\n\
            2. Show catalogue\n\
            3. Lend book\n\
            4. Return book\n\
            5. Find book\n\
            6. Export data\n\
            7. Import data\n\
            8. Show statistics\n\
            0. Exit\n"))
        if not 0 <= selection <= 8:
            print("Invalid option. Please try again.")
            continue
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue
    
    match selection:
        case 1:
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            year = int(input("Enter year of publication: "))
            available = input("Is the book available? (y/n): ").lower() == 'y'
            add_book(bookshelf, title, author, year, available)
        case 2:
            sorting = input("Sort by (title, author, year) or leave blank for default: ").lower().strip()
            if sorting not in ['title', 'author', 'year']:
                print("Invalid sorting option. Default sorting will be used.")
                sorting = None
            show_catalogue(bookshelf, sorting)
        case 3:
            book_id = int(input("Enter book ID to lend: "))
            lend_book(bookshelf, book_id)
        case 4:
            book_id = int(input("Enter book ID to return: "))
            return_book(bookshelf, book_id)
        case 5:
            search_term = input("Enter title or author to search for. Start with 're:' for regex search: ")
            regex = search_term.startswith('re:')
            find_book(bookshelf, search_term, regex)
        case 6:
            file_path = input("Enter file path to export data: ")
            export_data(bookshelf, file_path)
        case 7:
            file_path = input("Enter file path to import data: ")
            bookshelf = import_data(file_path)
        case 8:
            show_statistics(bookshelf)
        case 0:
            print("Exiting...")
            break

"""
C:\PyProjects\prj001\esercizio002\bookshelf.json
"""