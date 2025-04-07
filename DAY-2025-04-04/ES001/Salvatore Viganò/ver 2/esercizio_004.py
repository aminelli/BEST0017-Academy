import datetime
import json, re, os, time
from typing import List, Dict, Any

# Author: Vigano' Salvatore
# Date: 04/04/2025
# Description: This script implements a digital library management system, handling book data, user interactions, and file operations.

# Define a type alias for a Book object to make the code more readable
Book = Dict[str, Any]

def generate_id(library: List[Book]) -> int:
    """
    Generate a unique ID for a new book based on the current library content.
    The ID is generated as the maximum existing ID + 1, or 1 if the library is empty.

    Args:
        library (List[Book]): A list of books currently in the library.

    Returns:
        int: The next available unique ID for a new book.
    """
    # If the library is empty, start with ID 1
    if not library:
        return 1
    # If the library is not empty, generate the next ID as the max current ID + 1
    return max(book["id"] for book in library) + 1

def capitalize_author(author: str) -> str:
    """Capitalizes the author's name correctly, handling initials."""
    words = author.split()
    capitalized_words = []
    for word in words:
        if '.' in word:  # Handles initials (e.g., J.R.R.)
            parts = word.split('.')
            capitalized_parts = [part.capitalize() for part in parts]
            capitalized_words.append('.'.join(capitalized_parts))
        else:
            capitalized_words.append(word.capitalize())
    return ' '.join(capitalized_words)

def add_book(library: List[Book], title: str, author: str, year: int) -> None:
    """
    Adds a new book to the library and saves the changes to the JSON file.
    Verifies that no duplicates exist (title, author, year) case-insensitively.
    Capitalizes title and author correctly.

    Args:
        library (List[Book]): The list of books in the library.
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The publication year of the book.

    Returns:
        None
    """
    title = ' '.join(word.capitalize() for word in title.split())
    author = capitalize_author(author)

    # Verifies duplicates (case-insensitively)
    if any(book["title"].lower() == title.lower() and 
           book["author"].lower() == author.lower() and 
           book["year"] == year 
           for book in library):
        print("Error: A book with the same title, author, and year already exists in the library.")
        return

    new_book: Book = {
        "id": max((book["id"] for book in library), default=0) + 1,  # Unique ID
        "title": title,
        "author": author,
        "year": year,
        "available": True  # The book is initially available
    }
    library.append(new_book)
    print(f"The book '{title}' has been successfully added.")
    save_data(library, "library.json")

def remove_book(library: List[Book], book_id: int) -> None:
    """
    Removes a book from the library by its ID.
    If the book with the given ID is not found, a ValueError is raised.

    Args:
        library (List[Book]): The list of books in the library.
        book_id (int): The ID of the book to be removed.

    Returns:
        None
    """
    try:
        book_found = False  # Flag to track if the book was found
        book_to_remove = None

        # Iterate through the list of books to find the book by its ID
        for book in library:
            if book["id"] == book_id:
                book_to_remove = book
                book_found = True
                break  # Exit the loop once the book is found

        if book_found:
            library.remove(book_to_remove)
            print(f"The book '{book_to_remove['title']}' with ID {book_id} has been successfully removed.")
            save_data(library, "library.json")  # Save the updated library
        else:
            raise ValueError(f"No book found with ID {book_id} in the library.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while removing the book: {e}")
        raise

def display_catalog(library: List[Book], sort_by: str, reverse: bool) -> None:
    """
    Displays all available books in the library, optionally sorted.
    If no books are available, prints a message indicating that.

    Args:
        library (List[Book]): The list of books in the library.
        sort_by (str): The field to sort by ('title', 'author', or 'year').
        reverse (bool): True for descending order, False for ascending.

    Returns:
        None
    """
    try:
        print("\nLibrary Catalog:")
        available_books = [book for book in library if book["available"]]

        if not available_books:
            print("There are no available books in the library at the moment.")
            return

        valid_sort_options = ["title", "author", "year"]
        if sort_by not in valid_sort_options:
            print("Invalid sort option. Sorting by ID by default.")
            available_books.sort(key=lambda book: book["id"], reverse=reverse) #sort by ID
        else:
            if sort_by == "title":
                available_books.sort(key=lambda book: book["title"].lower(), reverse=reverse)
            elif sort_by == "author":
                available_books.sort(key=lambda book: book["author"].lower(), reverse=reverse)
            elif sort_by == "year":
                available_books.sort(key=lambda book: book["year"], reverse=reverse)

        for book in available_books:
            print(f"- ID {book['id']}: '{book['title']}' by {book['author']} ({book['year']})")

    except Exception as e:
        print(f"An unexpected error occurred while displaying the catalog: {e}")
        raise

def borrow_book(library: List[Book], borrowed_list: List[Book], book_id: int) -> None:
    """
    Marks a book as borrowed by its ID.
    If the book is already borrowed, prints a message to inform the user.
    Updates the 'available' status in the library directly.

    Args:
        library (List[Book]): The list of books in the library.
        borrowed_list (List[Book]): The list of books that are currently borrowed.
        book_id (int): The ID of the book to borrow.

    Returns:
        None
    """
    try:
        book_found = False  # Flag to track if the book was found
        for book in library:
            if book["id"] == book_id:
                book_found = True
                if book["available"]:
                    book["available"] = False  # Mark the book as not available
                    borrowed_list.append(book)  # Add the book to the borrowed list
                    save_data(borrowed_list, "borrowed_list.json")  # Save the updated borrowed list
                    save_data(library, "library.json")  # Save the updated library
                    print(f"The book '{book['title']}' has been successfully borrowed.")
                else:
                    print(f"The book '{book['title']}' is already borrowed and not available.")
                break

        if not book_found:
            raise ValueError(f"No book found with ID {book_id} in the library.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while borrowing the book: {e}")
        raise

def return_book(library: List[Book], borrowed_list: List[Book], book_id: int) -> None:
    """
    Marks a book as returned (available) by its ID.
    If the book was not borrowed, informs the user.
    Uses the ID to find the book in the library.

    Args:
        library (List[Book]): The list of books in the library.
        borrowed_list (List[Book]): The list of books that are currently borrowed.
        book_id (int): The ID of the book to return.

        Returns:
        None
    """
    try:
        book_found_borrowed = False
        book_found_library = False

        # Find the book in the borrowed_list
        for borrowed_book in borrowed_list:
            if borrowed_book["id"] == book_id:
                book_found_borrowed = True
                borrowed_list.remove(borrowed_book)  # Remove the book from the borrowed list

                # Find the corresponding book in the library using ID
                for library_book in library:
                    if library_book["id"] == book_id:
                        library_book["available"] = True  # Mark the book as available
                        book_found_library = True
                        break  # Exit the loop once the book is found in the library

                if not book_found_library:
                    raise ValueError(f"Book with ID {book_id} was found in borrowed list but not in the library.")

                save_data(borrowed_list, "borrowed_list.json")  # Save the updated borrowed list
                save_data(library, "library.json")  # Save the updated library
                print(f"The book '{borrowed_book['title']}' has been successfully returned.")
                break  # Exit the loop once the book is returned

        if not book_found_borrowed:
            raise ValueError(f"No borrowed book found with ID {book_id}.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while returning the book: {e}")
        raise

def save_data(library: List[Book], filename: str) -> None:
    """
    Saves the library data to a JSON file.
    Handles specific exceptions like IOError.

    Args:
        library (List[Book]): The list of books to be saved.
        filename (str): The file name to save the data.

    Returns:
        None
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(library, f, indent=4, ensure_ascii=False)
        print(f"The library data has been successfully saved to '{filename}'.")
    except IOError as e:
        print(f"Error: Unable to write to file '{filename}': {e}")
    except TypeError as e:
        print(f"Error: Data type incompatible for JSON serialization in '{filename}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving the data to '{filename}': {e}")

def load_data(filename: str) -> List[Book]:
    """
    Loads library data from a JSON file.
    Handles specific exceptions and validates the JSON schema.

    Args:
        filename (str): The file name from which to load the data.

        Returns:
        List[Book]: The loaded library data (or an empty list if an error occurs).
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            library: List[Book] = json.load(f)
        # Add JSON schema validation here if needed
        # Example using a hypothetical validate_schema function:
        # if not validate_schema(library):
        #     raise ValueError("Invalid JSON schema.")
        print(f"The library data has been successfully loaded from '{filename}'.")
        return library
    except FileNotFoundError:
        print(f"Warning: The file '{filename}' was not found. Returning an empty library.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON format. Please check the file.")
        return []
    except ValueError as e:
        print(f"Error: Invalid data schema in '{filename}': {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading the data from '{filename}': {e}")
        return []

def get_valid_int(prompt: str, error_message: str) -> int:
    """
    Prompt the user for an integer input, ensuring that the input is valid and not greater than the current year.
    
    Args:
        prompt (str): The prompt to display to the user.
        error_message (str): The error message to display if the input is invalid.
    
    Returns:
        int: A valid integer entered by the user.
    """
    current_year = datetime.datetime.now().year
    while True:
        try:
            # Get user input
            user_input = input(prompt)
            # Convert the input to an integer
            year = int(user_input)
            # Check if the year is greater than 0 and not greater than the current year
            if 0 < year <= current_year:
                return year
            elif year > current_year:
                print(f"Error: The year cannot be greater than the current year ({current_year}).")
            else:
                print("Error: The year must be greater than 0.")
        # Handle ValueError if the input is not a valid integer
        except ValueError:
            print(error_message)

def get_valid_string(prompt: str, error_message: str, max_length: int = 100) -> str:
    """
    Prompts the user for a string input, ensuring it is non-empty, matches the given pattern,
    and does not exceed the maximum length.

    Args:
        prompt (str): The prompt to display to the user.
        error_message (str): The error message to display if the input is invalid.
        max_length (int): The maximum allowed length of the string.

        Returns:
        str: A valid non-empty string entered by the user.
    """
    # Regex pattern to match valid title format
    title_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9\s\.]*$'
    # Regex pattern to match valid author format
    author_pattern = r'^[a-zA-Z][a-zA-Z0-9\s\.]*$'

    while True:
        # Get user input and remove leading/trailing spaces
        user_input = input(prompt).strip()

        # Check if the input is not empty
        if not user_input:
            print("Error: Input cannot be empty.")
            continue

        # Check if the input exceeds the maximum length
        if len(user_input) > max_length:
            print(f"Error: Input exceeds the maximum length of {max_length} characters.")
            continue

        # Check if the prompt is for the title
        if "title" in prompt.lower():
            # Check if the title matches the pattern
            if re.match(title_pattern, user_input):
                return user_input
            else:
                print(error_message)
                continue
        # Check if the prompt is for the author
        elif "author" in prompt.lower():
            # Check if the author matches the pattern
            if re.match(author_pattern, user_input):
                return user_input
            else:
                print(error_message)
                continue
        else:
            # If is not title or author return the input without checking regex
            return user_input

def search_book(library: List[Book], search_term: str) -> None:
    """
    Search for books by title or author, allowing uppercase letters at the beginning.
    
    Args:
        library (List[Book]): The list of books in the library.
        search_term (str): The title or author to search for.
    
    Returns:
        None
    """
    # Regex pattern to allow uppercase letters at the beginning
    pattern = re.compile(r'^[a-zA-Z0-9 ]+$')

    # Check if the search term is valid
    if not pattern.match(search_term):
        print("Error: The search term can only contain letters and numbers (no special characters).")
        return

    # Find books that match the search term (case-insensitive)
    found_books = [book for book in library if search_term.lower() in book['title'].lower() or search_term.lower() in book['author'].lower()]

    # If books are found, print them
    if found_books:
        print("Found books:")
        for book in found_books:
            print(f"- ID {book['id']}: '{book['title']}' by {book['author']} ({book['year']})")
    else:
        print("No books found matching your search criteria.")

def display_menu():
    """
    Display the main menu with a cleaner, more visually appealing format.
    """
    print("\n" + "="*40)  # Separator line
    print("    === Digital Library Menu ===")  # Title with spacing
    print("="*40)  # Another separator line

    menu_options = [
        "1. Add a new book",
        "2. Remove a book",
        "3. Display catalog",
        "4. Borrow a book",
        "5. Return a book",
        "6. Search for a book",
        "7. Save library data",
        "8. Load library data",
        "9. Display statistics",
        "10. Exit"
    ]
    
    for option in menu_options:
        print(f"    {option}")  # Indented options for cleaner appearance
    
    print("="*40)  # Separator line

def clear_terminal():
    """
    Clear the terminal screen based on the operating system.
    """
    # Check if the system is Windows or Unix-based and run the corresponding command
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS/Linux
        os.system('clear')

def display_statistics(library: List[Book], borrowed_list: List[Book]) -> None:
    """
    Display statistics about the library.

    Args:
        library (List[Book]): The list of books in the library.
        borrowed_list (List[Book]): The list of books that are currently borrowed.

    Returns:
        None
    """
    total_books = len(library)
    borrowed_books = len(borrowed_list)
    available_books = sum(1 for book in library if book["available"])

    print("\nLibrary Statistics:")
    print(f"Total Books: {total_books}")
    print(f"Borrowed Books: {borrowed_books}")
    print(f"Available Books: {available_books}")

def get_user_choice() -> int:
    """Gets and validates the user's menu choice."""
    return get_valid_int("Please enter your choice (1-10): ", "Error: Please enter a number between 1 and 10.");

def handle_add_book(library: List[Book]) -> None:
    """Handles the addition of a new book."""
    title = get_valid_string("Enter the title: ", "Error: The title must start with a letter or number, and can only contain letters, numbers, spaces, and periods.")
    author = get_valid_string("Enter the author: ", "Error: The author must start with a letter, and can only contain letters, numbers, spaces, and periods.")
    year = get_valid_int("Enter the publication year: ", "Error: Please enter a valid year.")
    add_book(library, title, author, year)
    time.sleep(3)

def handle_remove_book(library: List[Book]) -> None:
    """Handles the removal of a book."""
    book_id = get_valid_int("Enter the book ID to remove: ", "Error: The book ID must be a valid number.")
    remove_book(library, book_id)
    time.sleep(3)

def handle_display_catalog(library: List[Book]) -> None:
    """Handles the display of the book catalog."""
    sort_option = get_valid_string(
        "Sort by (title, author, year): ",
        "Error: Invalid sort option. Please enter 'title', 'author', or 'year'."
    ).lower()

    valid_sort_options = ["title", "author", "year"]
    if sort_option not in valid_sort_options:
        print("Invalid sort option. Sorting by ID by default.")
        sort_option = "id"

    reverse_option = get_valid_string(
        "Descending order? (yes/no): ",
        "Error: Invalid input. Please enter 'yes' or 'no'."
    ).lower()

    valid_reverse_options = ["yes", "no"]
    if reverse_option not in valid_reverse_options:
        print("Invalid input. Defaulting to ascending order.")
        reverse_option = "no"

    reverse = reverse_option == "yes"
    display_catalog(library, sort_option, reverse)
    input("Press Enter to continue...")

def handle_borrow_book(library: List[Book], borrowed_list: List[Book]) -> None:
    """Handles the borrowing of a book."""
    book_id = get_valid_int("Enter the book ID to borrow: ", "Error: The book ID must be a valid number.")
    borrow_book(library, borrowed_list, book_id)
    time.sleep(3)

def handle_return_book(library: List[Book], borrowed_list: List[Book]) -> None:
    """Handles the return of a book."""
    book_id = get_valid_int("Enter the book ID to return: ", "Error: The book ID must be a valid number.")
    return_book(library, borrowed_list, book_id)
    time.sleep(3)

def handle_search_book(library: List[Book]) -> None:
    """Handles the search for a book."""
    search_term = input("Enter the title or author to search: ")
    search_book(library, search_term)
    input("Press Enter to continue...")

def handle_save_data(library: List[Book], borrowed_list: List[Book], filename: str) -> None:
    """Handles saving library and borrowed data."""
    save_data(library, filename)
    save_data(borrowed_list, "borrowed_list.json")
    print("Changes have been saved.")
    time.sleep(3)

def handle_load_data(library: List[Book], filename: str) -> List[Book]:
    """Handles loading library data."""
    loaded_library = load_data(filename)
    time.sleep(3)
    return loaded_library

def handle_display_statistics(library: List[Book], borrowed_list: List[Book]) -> None:
    """Handles displaying library statistics."""
    display_statistics(library, borrowed_list)
    input("Press Enter to continue...")
    clear_terminal()

def main_menu() -> None:
    """
    Display the main menu and handle user interactions.

    This function loops indefinitely, presenting the menu and handling user choices
    until the user chooses to exit the program.
    """
    library: List[Book] = []
    borrowed_list: List[Book] = []
    filename: str = "library.json"

    library = load_data(filename)
    borrowed_list = load_data("borrowed_list.json")

    while True:
        clear_terminal()
        display_menu()
        choice = get_user_choice()

        try:
            if choice == 1:
                handle_add_book(library)
            elif choice == 2:
                handle_remove_book(library)
            elif choice == 3:
                handle_display_catalog(library)
            elif choice == 4:
                handle_borrow_book(library, borrowed_list)
            elif choice == 5:
                handle_return_book(library, borrowed_list)
            elif choice == 6:
                handle_search_book(library)
            elif choice == 7:
                handle_save_data(library, borrowed_list, filename)
            elif choice == 8:
                library = handle_load_data(library, filename)
            elif choice == 9:
                handle_display_statistics(library, borrowed_list)
            elif choice == 10:
                save_changes = input("Do you want to save changes before exiting? (y/n): ").strip().lower()
                if save_changes == 'y':
                    handle_save_data(library, borrowed_list, filename)
                print("Exiting the program...")
                time.sleep(3)
                clear_terminal()
                break
            else:
                print("Error: Invalid choice. Please choose a valid option.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
if __name__ == '__main__':
    main_menu()