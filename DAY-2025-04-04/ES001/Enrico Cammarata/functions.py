import json
import re


def add_book(library: list[dict], title: str, author: str, year: int) -> str:
    """Adds a book to the library.

    Args:
        library (list[dict]): The library to which the book will be added.
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The year of publication.

    Returns:
        str: A message indicating the result of the operation.
    """
    # Sort the library by ID before assigning the ID based on the last book
    library.sort(key = lambda x: x["id"])
    book_id = library[-1].get("id") + 1 if len(library) > 0 else 1
    
    # Add the new book to the library
    library.append({
        "id": book_id, 
        "title": title,
        "author": author,
        "year": year,
        "available": True
    })

    return "Book added!"


def remove_book(library: list[dict], book_id: int) -> str:
    """Removes a book from the library given its ID.

    Args:
        library (list[dict]): The library from which the book will be removed.
        book_id (int): The ID of the book to be removed.

    Returns:
        str: A message indicating the result of the operation.
    """
    for book in library:
        if book.get("id") == book_id:
            library.remove(book)
            return "Book removed!"
    return "Book not found!"


def search_book(library: list[dict], keyword: str) -> list:
    """Searches for a book in the library.

    Args:
        library (list[dict]): The library to search in.
        keyword (str): The keyword to search for in the book title or author.

    Returns:
        list[dict]: A list of books that match the keyword.
    """
    results = []
    # If no keyword is provided, return all books
    if not keyword:
        return results
    
    # Search for books that match the keyword in title or author
    for book in library:
        if (keyword.lower() in book.get("title").lower() or
            keyword.lower() in book.get("author").lower()):
            results.append(book)
    return results


def borrow_book(library: list[dict], book_id: int) -> str:
    """Borrows a book from the library.

    Args:
        library (list[dict]): The library from which the book will be borrowed.
        book_id (int): The ID of the book to be borrowed.

    Returns:
        str: A message indicating the result of the operation.
    """
    for book in library:
        if book.get("id") == book_id:
            # Check if the book is available
            if book.get("available"):
                book["available"] = False
                return "Book borrowed!"
            else:
                return "Book not available!"
    return "Book not found!"


def return_book(library: list[dict], book_id: int) -> str:
    """Marks a book as available after being returned.

    Args:
        library (list[dict]): The library to which the book will be returned.
        book_id (int): The ID of the book to be returned.

    Returns:
        str: A message indicating the result of the operation.
    """
    for book in library:
        if book.get("id") == book_id:
            book["available"] = True
            return "Book returned!"
    return "Book not found!"


def show_catalog(library: list[dict]) -> list[dict]:
    """Shows all available books in the library.

    Args:
        library (list[dict]): The library to show.

    Returns:
        list[dict]: A list of all available books.
    """
    # Filter the library to show only available books
    return list(filter(lambda x: x.get("available"), library))

    # I could also use a list comprehension:
    # return [book for book in library if book.get("available")]


def save_data(library: list[dict], filename: str) -> str:
    """Saves the library data to a JSON file.

    Args:
        library (list[dict]): The library to save.
        filename (str): The name of the file to save the data to.

    Returns:
        str: A message indicating the result of the operation.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(library, file, ensure_ascii=False, indent=4)
        return "Data saved!"
    except Exception as e:
        return f"Error during saving data: {e}"


def load_data(filename: str) -> list[dict]:
    """Loads library data from a JSON file.

    Args:
        filename (str): The name of the file to load the data from.

    Returns:
        list[dict]: A list of books loaded from the file.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def library_stats(library: list[dict]) -> dict:
    """Returns statistics about the library.

    Args:
        library (list[dict]): The library to analyze.

    Returns:
        dict: A dictionary containing the books
    """
    total = len(library)
    borrowed = len([book for book in library if not book.get("available")])
    available = total - borrowed
    return {
        "total_books": total,
        "borrowed_books": borrowed,
        "available_books": available
    }


def sort_books(library: list[dict], key: str = "title") -> list[dict]:
    """Sorts the library by a given key ('title', 'author', or 'year')

    Args:
        library (list[dict]): The library to sort.
        key (str, optional): The key to sort by. Can be 'title', 'author', or 'year'. Defaults to "title".

    Raises:
        ValueError: If the key is not one of the allowed values.

    Returns:
        list[dict]: The sorted library.
    """
    # Check if the key is valid
    if key not in {"title", "author", "year"}:
        raise ValueError("Invalid sort key.")
    # Sort the library by the given key
    return sorted(library, key=lambda x: x[key])


def regex_search(library: list[dict], pattern: str) -> list[dict]:
    """Searches using a regular expression in titles and authors.

    Args:
        library (list[dict]): The library to search in.
        pattern (str): The regex pattern to search for.

    Returns:
        list[dict]: A list of books that match the regex pattern.
    """
    try:
        # Compile the regex pattern, with case insensitivity
        reg_pattern = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        raise ValueError("Invalid regex: {e}")
    
    # Filter the library using the regex pattern
    return [book for book in library if (reg_pattern.search(book["title"]) or reg_pattern.search(book["author"]))]
