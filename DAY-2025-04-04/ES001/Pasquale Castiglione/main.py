from utils import *

def menu():
    library = []
    # library = load_data("library.json")
    while True:
        print("\nLibrary Management")
        print("1. Add book")
        print("2. Remove book")
        print("3. Search book")
        print("4. Lend book")
        print("5. Return book")
        print("6. Display catalog")
        print("7. Save data")
        print("8. Load data")
        print("9. Statistics")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":  # Add book
            title = input("Title: ")
            author = input("Author: ")
            year = int(input("Year: "))
            add_book(library, title, author, year)

        elif choice == "2":  # Remove book
            book_id = int(input("ID of the book to remove: "))
            remove_book(library, book_id)

        elif choice == "3":  # Search book

            keyword = input("Enter keyword: ")
            search_book(library, keyword)

        elif choice == "4":  # Lend book
            book_id = int(input("ID of the book to lend: "))
            lend_book(library, book_id)

        elif choice == "5":  # Return book
            book_id = int(input("ID of the book to return: "))
            return_book(library, book_id)

        elif choice == "6":  # Display catalog
            criterion = input("Sort by (id/title/author/year): ")

            while criterion not in ["id", "title", "author", "year"]:
                print(
                    "Invalid criterion. Please choose 'id', 'title', 'author', or 'year'."
                )
                criterion = input("Sort by (id/title/author/year): ")

            display_catalog(library, criterion)

        elif choice == "7":  # Save data
            file_name = input("Enter file name to save data to: ")
            save_data(library, file_name)

        elif choice == "8":  # Load data
            file_name = input("Enter file name to load data from: ")
            library = load_data(file_name)

        elif choice == "9":  # Statistics
            library_statistics(library)

        elif choice == "0":  # Exit
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()
