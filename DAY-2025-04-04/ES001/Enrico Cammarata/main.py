from functions import *

def main():
    """Main function to run the library program in loop."""
    filename = "library.json"
    library = load_data(filename)

    while True:
        print("\n--- Library Menu ---")
        print("1. Add book")
        print("2. Remove book")
        print("3. Search for book")
        print("4. Borrow book")
        print("5. Return book")
        print("6. Show available books")
        print("7. Show stats")
        print("8. Sort books")
        print("9. Advanced search")
        print("10. Load data")
        print("11. Save data")
        print("0. Exit")

        # Enter choice
        choice = input("\nEnter your choice (0/11): ")
        print()

        # Add book
        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            year = int(input("Year: "))
            print(add_book(library, title, author, year))

        # Remove book
        elif choice == "2":
            book_id = int(input("Book ID to remove: "))
            print(remove_book(library, book_id))

        # Search for book
        elif choice == "3":
            keyword = input("Enter keyword (title/author): ")
            results = search_book(library, keyword)
            if results:
                for book in results:
                    print(book)
            else:
                print("No matching books found.")

        # Borrow book
        elif choice == "4":
            book_id = int(input("Book ID to borrow: "))
            print(borrow_book(library, book_id))

        # Return book
        elif choice == "5":
            book_id = int(input("Book ID to return: "))
            print(return_book(library, book_id))

        # Show available books
        elif choice == "6":
            available = show_catalog(library)
            if available:
                for book in available:
                    print(book)
            else:
                print("No books available.")

        # Show stats
        elif choice == "7":
            stats = library_stats(library)

            print(f"Total: {stats['total_books']}\n" +
                  f"Borrowed: {stats['borrowed_books']}\n" +
                  f"Available: {stats['available_books']}")
            
        # Sort books
        elif choice == "8":
            key = input("Sort by (title/author/year): ")
            try:
                sorted_library = sort_books(library, key)
                for book in sorted_library:
                    print(book)
            except ValueError as e:
                print(e)

        # Advanced search
        elif choice == "9":
            pattern = input("Enter a regular expression: ")
            results = regex_search(library, pattern)
            if results:
                for book in results:
                    print(book)
            else:
                print("No matches found.")
            
        # Load data
        elif choice == "10":
            library = load_data(filename)
            print("Data loaded!")

        # Save data
        elif choice == "11":
            print(save_data(library, filename))

        # Exit
        elif choice == "0":
            print("Saving and exiting...")
            save_data(library, filename)
            break

        # Invalid choice
        else:
            print("Invalid choice. Please try again.")

    # End of program message
    print("\n[END]\n")

if __name__ == "__main__":
    main()
