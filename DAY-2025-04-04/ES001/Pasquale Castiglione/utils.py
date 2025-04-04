import json
import re

def add_book(library: list, title: str, author: str, year: int):
    """
    Adds a new book to the library.

    Args:
        library (list): The list of books in the library.
        title (str): The title of the book to be added.
        author (str): The author of the book to be added.
        year (int): The publication year of the book to be added.

    Returns:
        None
    """

    # Generate a new ID for the book
    new_id = max([book['id'] for book in library], default=0) + 1

    book = {
        'id': new_id,
        'title': title,
        'author': author,
        'year': year,
        'available': True,
    }

    # Append the new book to the library
    library.append(book)
    print(f"Book '{title}' added.")


def remove_book(library: list, book_id):
    """
    Removes a book from the library based on its ID.

    Args:
        library (list): The list of books in the library.
        book_id: The ID of the book to be removed.

    Returns:
        None
    """

    for book in library:
        if book['id'] == book_id:
            library.remove(book)
            print(f"Book '{book['title']}' removed.")
            return
    print("Book not found.")

def search_book(library: list, keyword: str, available_only=False):
    """
    Searches for books in the library based on a keyword.

    Args:
        library (list): The list of books in the library.
        keyword (str): The keyword to search for in book titles or authors.
        available_only (bool, optional): If True, only available books are returned. Defaults to False.

    Returns:
        None
    """

    # Use regex to search for the keyword in titles and authors
    result = [book for book in library if re.search(keyword, book['title'], re.IGNORECASE) or re.search(keyword, book['author'], re.IGNORECASE)]

    # Filter results based on availability if specified
    if available_only:
        results = [book for book in results if book['available']]

    for book in result:
        print(f"Found: {book['title']} by {book['author']}, id {book['id']}")
    if not result:
        print("No books found.")


def lend_book(library: list, book_id: int):
    """
    Lends a book from the library if it is available.

    Args:
        library (list): The list of books in the library.
        book_id (int): id of the book to be lent.

    Returns:
        None
    """

    for book in library:
        if book['id'] == book_id:
            if book['available']:
                book['available'] = False
                print(f"Book '{book['title']}' lent out.")
                return
            else:
                print(f"Book '{book['title']}' is not available.")
                return
    print("Book not found.")


def return_book(library: list, book_id: int):
    """
    Marks a book as returned in the library if it matches the given book ID
    and is currently not available.

    Args:
        library (list): The list of books in the library.
        book_id (int): id of the book to be returned.

    Returns:
        None
    """

    for book in library:
        if book['id'] == book_id and not book['available']:
            book['available'] = True
            print(f"Book '{book['title']}' returned.")
            return
    print("Book not found or already available.")


def display_catalog(library: list, criterion: str = 'title'):
    """
    Displays a catalog of books in a formatted table, sorted by a specified criterion.

    Args:
        library (list): The list of books in the library.
        criterion (str, optional): The key by which to sort the catalog. Defaults to "title".

    Returns:
        None: This function prints the catalog to the console.
    """

    # Sort the library based on the specified criterion
    sorted_catalog = sorted(library, key=lambda x: x[criterion])

    # Print the header
    print("\n{:<7} | {:<35} | {:<35} | {:<4} | {:<10}".format('ID', 'Title', 'Author', 'Year', 'Available'))
    print("-" * 100)

    # Print each book in the catalog
    for book in sorted_catalog:
        #print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, Available: {'Yes' if book['available'] else 'No'}")
        print("{:<7} | {:<35} | {:<35} | {:<4} | {:<10}".format(book['id'], book['title'][:20], book['author'][:20], book['year'], 'Yes' if book['available'] else 'No'))


def save_data(library, file_name):
    """
    Saves the given library data to a file in JSON format.

    Args:
        library (dict): The data to be saved, typically a dictionary.
        file_name (str): The name of the file where the data will be saved.

    Raises:
        Exception: If an error occurs during the file writing process, 
                   an exception is caught and an error message is printed.
    """
    try:
        with open(file_name, 'w') as file:
            json.dump(library, file)
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data(file_name: str) -> list:
    """
    Loads data from a JSON file.

    Args:
        file_name (str): The path to the JSON file to be loaded.

    Returns:
        list: The data loaded from the JSON file. Returns an empty list if the file
              is not found or if an error occurs during loading.

    Raises:
        Exception: Prints an error message if an unexpected error occurs while loading the file.
    """
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


def library_statistics(library):
    """
    Prints statistics about a library's book collection.

    Args:
        library (list of dict): A list of dictionaries where each dictionary 
            represents a book. Each dictionary should have an 'available' key 
            with a boolean value indicating whether the book is available.

    Prints:
        A summary of the total number of books, the number of available books, 
        and the number of checked-out books.
    """

    total = len(library)

    checked_out = sum(1 for book in library if not book['available'])
    
    available = total - checked_out
    print(f"Total books: {total}, Available: {available}, Checked out: {checked_out}")