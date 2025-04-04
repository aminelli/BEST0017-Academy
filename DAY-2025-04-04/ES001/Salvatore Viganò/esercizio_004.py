import json, re, os, time
from typing import List, Dict, Any

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

def add_book(library: List[Book], title: str, author: str, year: int) -> None:
    """
    Add a new book to the library and save the updated library to the JSON file.
    Ensure that no two books have the same title, author, and year (case-insensitive).
    Capitalize the first letter of each word in title and author, including initials with dots.

    Args:
        library (List[Book]): The list of books in the library.
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The publication year of the book.

    Returns:
        None
    """
    # Capitalize the first letter of each word in title and author, including initials with dots
    title = ' '.join(word.capitalize() for word in title.split())
    author_words = author.split()
    capitalized_author_words = []
    for word in author_words:
        if '.' in word:  # Check if the word is an initial (e.g., J.R.R.)
            parts = word.split('.')
            capitalized_parts = [part.capitalize() for part in parts]
            capitalized_author_words.append('.'.join(capitalized_parts))
        else:
            capitalized_author_words.append(word.capitalize())
    author = ' '.join(capitalized_author_words)

    # Check if a book with the same title, author, and year already exists (case-insensitive)
    for book in library:
        if book["title"].lower() == title.lower() and book["author"].lower() == author.lower() and book["year"] == year:
            print("Error: A book with the same title, author, and year already exists.")
            return

    # Create a new book dictionary with an ID, title, author, publication year, and availability status
    new_book: Book = {
        "id": generate_id(library),
        "title": title,
        "author": author,
        "year": year,
        "available": True  # Initially, the book is available
    }
    # Append the new book to the library list
    library.append(new_book)
    # Print a success message
    print(f"The book '{title}' has been successfully added.")
    # save the updated library
    save_data(library, "library.json")

def remove_book(library: List[Book], book_id: int) -> None:
    """
    Remove a book from the library by its ID.
    If the book with the given ID is not found, a ValueError is raised.

    Args:
        library (List[Book]): The list of books in the library.
        book_id (int): The ID of the book to be removed.

    Returns:
        None
    """
    try:
        # Iterate through the list of books to find the book by its ID
        for book in library:
            # If the book is found, remove it from the library
            if book["id"] == book_id:
                # Get the title of the book
                title = book["title"]
                library.remove(book)
                # Print a success message with the book title
                print(f"The book '{title}' with ID {book_id} has been removed.")
                # Exit the function after removing the book
                return
        # If the book is not found, raise an exception
        raise ValueError(f"No book found with ID {book_id}.")
    # Handle the error if the book ID is not found
    except ValueError as e:
        print(f"Error: {e}")
    # Handle other exceptions
    except Exception as e:
        print(f"An error occurred while removing the book: {e}")
        raise

def display_catalog(library: List[Book], sort_by: str, reverse: bool) -> None:
    """
    Display all available books in the library that are marked as available, optionally sorted.
    If no books are available, print a message indicating that.

    Args:
        library (List[Book]): The list of books in the library.
        sort_by (str): The field to sort by ('title', 'author', or 'year').
        reverse (bool): True for descending order, False for ascending.

    Returns:
        None
    """
    try:
        # Print the catalog header
        print("\nLibrary Catalog:")
        # Filter out books that are available using lambda and filter()
        available_books = list(filter(lambda book: book["available"], library))
        # If no books are available, print a message
        if not available_books:
            print("There are no available books at the moment.")
            return

        # Sort the available books
        valid_sort_options = ["title", "author", "year"]
        while sort_by not in valid_sort_options:
            print("Invalid sort option.")
            sort_by = input("Sort by (title, author, year): ").lower()

        if sort_by == "title":
            available_books.sort(key=lambda book: book["title"].lower(), reverse=reverse)
        elif sort_by == "author":
            available_books.sort(key=lambda book: book["author"].lower(), reverse=reverse)
        elif sort_by == "year":
            available_books.sort(key=lambda book: book["year"], reverse=reverse)

        # Print all available books
        for book in available_books:
            print(f"- ID {book['id']}: '{book['title']}' by {book['author']} ({book['year']})")
    # Handle exceptions
    except Exception as e:
        print(f"An error occurred while displaying the catalog: {e}")
        raise

def borrow_book(library: List[Book], borrowed_list: List[Book], book_id: int) -> None:
    """
    Mark a book as borrowed by its ID.
    If the book is already borrowed, print a message to inform the user.
    Update the 'available' status in the library directly.

    Args:
        library (List[Book]): The list of books in the library.
        borrowed_list (List[Book]): The list of books that are currently borrowed.
        book_id (int): The ID of the book to borrow.

    Returns:
        None
    """
    try:
        # Iterate through the library to find the book by ID
        for book in library:
            # If the book is found
            if book["id"] == book_id:
                # If the book is available, mark it as borrowed (not available)
                if book["available"]:
                    book["available"] = False
                    # Add the book to the borrowed list
                    borrowed_list.append(book)
                    # Save borrowed list to a file
                    with open("borrowed_list.json", "w", encoding="utf-8") as f:
                        json.dump(borrowed_list, f, indent=4, ensure_ascii=False)

                    # Update library list available status
                    for lib_book in library:
                        if lib_book['id'] == book_id:
                            lib_book['available'] = False
                            break

                    # Save library list to a file
                    with open("library.json", "w", encoding="utf-8") as f:
                        json.dump(library, f, indent=4, ensure_ascii=False)

                    # Print a success message
                    print(f"The book '{book['title']}' has been borrowed.")
                else:
                    # Print a message if the book is already borrowed
                    print(f"The book '{book['title']}' is currently borrowed.")
                # Exit the function after borrowing the book
                return
        # If the book is not found, raise an exception
        raise ValueError(f"No book found with ID {book_id}.")
    # Handle exceptions
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred while borrowing the book: {e}")
        raise

def return_book(library: List[Book], borrowed_list: List[Book], book_id: int) -> None:
    """
    Mark a book as returned (available) by its ID.
    If the book was not borrowed, inform the user.
    If the book ID changed in library, search by title, author, and year.

    Args:
        library (List[Book]): The list of books in the library.
        borrowed_list (List[Book]): The list of books that are currently borrowed.
        book_id (int): The ID of the book to return.

    Returns:
        None
    """
    try:
        # Find the book in the borrowed_list (the one that was borrowed)
        for book in borrowed_list:
            # If the book is found in the borrowed list
            if book["id"] == book_id:
                # Remove the book from the borrowed_list
                borrowed_list.remove(book)
                # Find the corresponding book in the library using title, author, and year
                for library_book in library:
                    if (library_book["title"].lower() == book["title"].lower() and
                        library_book["author"].lower() == book["author"].lower() and
                        library_book["year"] == book["year"]):
                        # Change its availability status to True (available)
                        library_book["available"] = True
                        break
                else:
                    raise ValueError(f"Book with ID {book_id} not found in library.")
                # Save the updated borrowed_list to the borrowed_list.json file
                with open("borrowed_list.json", "w", encoding="utf-8") as f:
                    json.dump(borrowed_list, f, indent=4, ensure_ascii=False)
                # Save the updated library to the library.json file
                with open("library.json", "w", encoding="utf-8") as f:
                    json.dump(library, f, indent=4, ensure_ascii=False)
                # Print a success message
                print(f"The book '{book['title']}' has been returned.")
                # Exit the function after returning the book
                return
        # If the book is not found in borrowed_list, raise an error
        raise ValueError(f"No borrowed book found with ID {book_id}.")
    # Handle exceptions
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred while returning the book: {e}")
        raise

def save_data(library: List[Book], filename: str) -> None:
    """
    Save the library data to a JSON file.

    Args:
        library (List[Book]): The list of books to be saved.
        filename (str): The file name to save the data.

    Returns:
        None
    """
    try:
        # Open the file in write mode and save the library data as JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(library, f, indent=4, ensure_ascii=False)
        # Print a success message
        print(f"The library data has been successfully saved to '{filename}'.")
    # Handle exceptions
    except Exception as e:
        print(f"An error occurred while saving the data: {e}")
        raise

def load_data(filename: str) -> List[Book]:
    """
    Load library data from a JSON file.
    If the file does not exist or is invalid, it returns an empty list.

    Args:
        filename (str): The file name from which to load the data.

    Returns:
        List[Book]: The loaded library data (or an empty list if an error occurs).
    """
    try:
        # Try to open the file and load the JSON data into a Python list
        with open(filename, "r", encoding="utf-8") as f:
            library: List[Book] = json.load(f)
        # Print a success message
        print(f"The library data has been successfully loaded from '{filename}'.")
        return library
    # If the file does not exist, print a warning and return an empty list
    except FileNotFoundError:
        print(f"Warning: The file '{filename}' was not found. Returning an empty library.")
        return []
    # If the file is not valid JSON, print an error message
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON format.")
        return []
    # Handle other exceptions
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        raise

def get_valid_int(prompt: str, error_message: str) -> int:
    """
    Prompt the user for an integer input, ensuring that the input is valid.
    
    Args:
        prompt (str): The prompt to display to the user.
        error_message (str): The error message to display if the input is invalid.
    
    Returns:
        int: A valid integer entered by the user.
    """
    while True:
        try:
            # Get user input
            user_input = input(prompt)
            # Convert the input to an integer
            year = int(user_input)
            # Check if the year is greater than 0
            if year > 0:
                return year
            else:
                print("The year must be greater than 0.")
        # Handle ValueError if the input is not a valid integer
        except ValueError:
            print(error_message)

def get_valid_string(prompt: str, error_message: str) -> str:
    """
    Prompt the user for a string input, ensuring that the input is non-empty and matches the given pattern (if provided).
    
    Args:
        prompt (str): The prompt to display to the user.
        error_message (str): The error message to display if the input is invalid.
    
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
        if user_input:
            # Check if the prompt is for the title
            if "title" in prompt.lower():
                # Check if the title matches the pattern
                if re.match(title_pattern, user_input):
                    return user_input
                else:
                    print(error_message)
            # Check if the prompt is for the author
            elif "author" in prompt.lower():
                # Check if the author matches the pattern
                if re.match(author_pattern, user_input):
                    return user_input
                else:
                    print(error_message)
            else:
                # If is not title or author return the input without checking regex
                return user_input
        else:
            print("Input cannot be empty.")

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
        print("No books found matching your search.")

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

def main_menu() -> None:
    """
    Display the main menu and handle user interactions with input validation.

    This function loops indefinitely, presenting the menu and handling user choices
    until the user chooses to exit the program.

    Returns:
        None
    """
    # Initialize the library as an empty list
    library: List[Book] = []
    # Initialize the borrowed list as an empty list
    borrowed_list: List[Book] = []
    # Set the filename for saving/loading library data
    filename: str = "library.json"

    # Load existing data from the JSON files (if available)
    library = load_data(filename)
    borrowed_list = load_data("borrowed_list.json")

    while True:
        clear_terminal()
        display_menu()
        # Get the user's choice with validation
        choice = get_valid_int("Please enter your choice (1-10): ", "Please enter a number between 1 and 10.")

        try:
            # Add a new book
            if choice == 1:
                title = get_valid_string("Enter the title: ", "The title must start with a letter or number, and can only contain letters, numbers, spaces, and periods.")
                author = get_valid_string("Enter the author: ", "The author must start with a letter, and can only contain letters, numbers, spaces, and periods.")
                year = get_valid_int("Enter the publication year: ", "Please enter a valid year.")
                add_book(library, title, author, year)
                time.sleep(3)

            # Remove a book
            elif choice == 2:
                book_id = get_valid_int("Enter the book ID to remove: ", "The book ID must be a valid number.")
                remove_book(library, book_id)
                time.sleep(3)

            # Display the catalog
            elif choice == 3:
                sort_option = get_valid_string(
                    "Sort by (title, author, year): ",
                    "Invalid sort option. Please enter 'title', 'author', or 'year'."
                ).lower()

                valid_sort_options = ["title", "author", "year"]
                while sort_option not in valid_sort_options:
                    print("Invalid sort option. Please enter 'title', 'author', or 'year'.")
                    sort_option = get_valid_string(
                        "Sort by (title, author, year): ",
                        "Invalid sort option. Please enter 'title', 'author', or 'year'."
                    ).lower()

                reverse_option = get_valid_string(
                    "Descending order? (yes/no): ",
                    "Invalid input. Please enter 'yes' or 'no'."
                ).lower()

                valid_reverse_options = ["yes", "no"]
                while reverse_option not in valid_reverse_options:
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    reverse_option = get_valid_string(
                        "Descending order? (yes/no): ",
                        "Invalid input. Please enter 'yes' or 'no'."
                    ).lower()

                reverse = reverse_option == "yes"
                display_catalog(library, sort_option, reverse)
                input("Press Enter to continue...")

            # Borrow a book
            elif choice == 4:
                book_id = get_valid_int("Enter the book ID to borrow: ", "The book ID must be a valid number.")
                borrow_book(library, borrowed_list, book_id)
                time.sleep(3)

            # Return a book
            elif choice == 5:
                book_id = get_valid_int("Enter the book ID to return: ", "The book ID must be a valid number.")
                return_book(library, borrowed_list, book_id)
                time.sleep(3)

            # Search for a book
            elif choice == 6:
                search_term = input("Enter the title or author to search: ")
                search_book(library, search_term)
                input("Press Enter to continue...")

            # Save the library data
            elif choice == 7:
                save_data(library, filename)
                time.sleep(3)

            # Load the library data
            elif choice == 8:
                library = load_data(filename)
                time.sleep(3)

            # Display statistics
            elif choice == 9:
                display_statistics(library, borrowed_list)
                input("Press Enter to continue...")
                clear_terminal()
                continue

            # Exit the program
            elif choice == 10:
                # Ask the user if they want to save changes before exiting
                save_changes = input("Do you want to save changes before exiting? (y/n): ").strip().lower()
                
                # If the user wants to save changes, save the library data
                if save_changes == 'y':
                    save_data(library, filename)
                    save_data(borrowed_list, "borrowed_list.json")
                    print("Changes have been saved.")

                # Exit the program
                print("Exiting the program...")
                time.sleep(3)
                clear_terminal()
                break

            # Handle invalid choices
            else:
                print("Invalid choice. Please choose a valid option.")

        # Handle exceptions
        except Exception as e:
            print(f"An error occurred: {e}")
    
if __name__ == '__main__':
    main_menu()