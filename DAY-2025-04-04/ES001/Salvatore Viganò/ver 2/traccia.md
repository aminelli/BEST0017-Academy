### 🔥 **Esercizio Avanzato: Gestione di una Biblioteca con Funzioni in Python**  

#### **📌 Obiettivo**
Scrivere un programma che gestisca una **biblioteca digitale**, utilizzando **funzioni** per organizzare e manipolare i dati dei libri.  

---

### **🔹 Specifiche**
1. 📖 **Ogni libro** è rappresentato da un **dizionario** con le seguenti informazioni:
   - `id`: un codice numerico univoco.
   - `titolo`: il titolo del libro.
   - `autore`: il nome dell'autore.
   - `anno`: l'anno di pubblicazione.
   - `disponibile`: `True` se il libro è disponibile, `False` se è in prestito.

2. 📚 I libri sono memorizzati in una **lista di dizionari**.

3. 🔄 **Il programma deve implementare le seguenti funzioni:**
   - **`aggiungi_libro(biblioteca, titolo, autore, anno)`**  
     ➝ Aggiunge un nuovo libro alla biblioteca con un ID univoco.  
   - **`rimuovi_libro(biblioteca, id_libro)`**  
     ➝ Rimuove un libro dato il suo ID.  
   - **`cerca_libro(biblioteca, parola_chiave)`**  
     ➝ Cerca un libro per titolo o autore e restituisce i risultati.  
   - **`presta_libro(biblioteca, id_libro)`**  
     ➝ Segna un libro come "in prestito" se disponibile.  
   - **`restituisci_libro(biblioteca, id_libro)`**  
     ➝ Segna un libro come "disponibile" dopo la restituzione.  
   - **`visualizza_catalogo(biblioteca)`**  
     ➝ Mostra tutti i libri disponibili.  
   - **`salva_dati(biblioteca, nome_file)`**  
     ➝ Salva i dati della biblioteca in un file JSON.  
   - **`carica_dati(nome_file)`**  
     ➝ Carica i dati da un file JSON.  

---

### **🔹 Esempio di Utilizzo**
```python
biblioteca = []

aggiungi_libro(biblioteca, "1984", "George Orwell", 1949)
aggiungi_libro(biblioteca, "Il Signore degli Anelli", "J.R.R. Tolkien", 1954)

visualizza_catalogo(biblioteca)

presta_libro(biblioteca, 1)
restituisci_libro(biblioteca, 1)

cerca_libro(biblioteca, "Orwell")

salva_dati(biblioteca, "biblioteca.json")
nuova_biblioteca = carica_dati("biblioteca.json")
```

---

### **💡 Requisiti Tecnici**
✅ Utilizzare **funzioni** per ogni operazione.  
✅ Utilizzare **JSON** per il salvataggio e caricamento dei dati.  
✅ Utilizzare **list comprehension** o **lambda functions** dove possibile.  
✅ Implementare un **controllo degli errori** (es. ID non trovato, file non esistente).  

---

### 🔥 **Sfida Extra**
1. 📊 **Aggiungere statistiche**, come il numero totale di libri o quelli in prestito.  
2. 📈 **Ordinare i libri per titolo, autore o anno** prima di mostrarli.  
3. 🔍 **Implementare una ricerca avanzata con espressioni regolari** (`re`).  
