from funzioni import *

def mostra_menu():
    print("\n MENU BIBLIOTECA ")
    print("1. Aggiungi libro")
    print("2. Rimuovi libro")
    print("3. Visualizza catalogo")
    print("4. Presta libro")
    print("5. Restituisci libro")
    print("6. Cerca libro")
    print("7. Mostra statistiche")
    print("8. Salva dati")
    print("9. Carica dati")
    print("0. Esci")

def main():
    biblioteca = []
    nome_file = "biblioteca.json"

    while True:
        mostra_menu()
        scelta = input("Scegli un'opzione: ").strip()

        match scelta:
            case "1":
                titolo = input("Titolo: ")
                autore = input("Autore: ")
                anno = input("Anno: ")
                if not anno.isdigit():
                    print("L'anno deve essere un numero.")
                    continue
                add_book(biblioteca, titolo, autore, int(anno))
                print("Libro aggiunto!")

            case "2":
                try:
                    book_id = int(input("ID del libro da rimuovere: "))
                    if remove_book(biblioteca, book_id):
                        print("Libro rimosso.")
                except ValueError:
                    print("Inserisci un numero valido.")

            case "3":
                visualize_catalog(biblioteca)

            case "4":
                try:
                    book_id = int(input("ID del libro da prestare: "))
                    if lend_book(biblioteca, book_id):
                        print("📕 Libro prestato.")
                except ValueError:
                    print("Inserisci un numero valido.")

            case "5":
                try:
                    book_id = int(input("ID del libro da restituire: "))
                    if return_book(biblioteca, book_id):
                        print("📗 Libro restituito.")
                except ValueError:
                    print("Inserisci un numero valido.")

            case "6":
                parola = input("Parola chiave (titolo o autore): ")
                risultati = search_book(biblioteca, parola)
                if risultati:
                    for libro in risultati:
                        stato = "Disponibile" if libro["available"] else "In prestito"
                        print(f"{libro['id']}: {libro['title']} - {libro['author']} ({libro['year']}) - {stato}")
                else:
                    print("🔍 Nessun libro trovato.")

            case "7":
                show_statistics(biblioteca)

            case "8":
                save_data(biblioteca, nome_file)

            case "9":
                biblioteca = upload_data(nome_file)

            case "0":
                print("Arrivederci!")
                break

            case _:
                print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()
