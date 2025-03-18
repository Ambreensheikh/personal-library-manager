import tkinter as tk
from tkinter import messagebox
import json
import os

data_file = 'library.txt'

# Load and save library functions
def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

# Add, remove, and search functions
def add_book(library):
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    genre = genre_entry.get()
    read = read_var.get()

    if title and author and year and genre:
        new_book = {
            'title': title,
            'author': author,
            'year': year,
            'genre': genre,
            'read': read
        }
        library.append(new_book)
        save_library(library)
        messagebox.showinfo("Success", f'Book "{title}" added successfully!')
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "All fields must be filled out!")

def remove_book(library):
    title = title_entry.get()
    if title:
        initial_length = len(library)
        library[:] = [book for book in library if book['title'].lower() != title.lower()]
        if len(library) < initial_length:
            save_library(library)
            messagebox.showinfo("Success", f'Book "{title}" removed successfully!')
        else:
            messagebox.showwarning("Not Found", f'Book "{title}" not found in the library!')
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please enter a title to remove.")

def search_library(library):
    search_by = search_by_var.get()
    search_term = search_term_entry.get().lower()

    result = [book for book in library if search_term in book[search_by].lower()]
    if result:
        result_text = "\n".join([f"{book['title']} by {book['author']} ({book['year']}) - {'Read' if book['read'] else 'Unread'}" for book in result])
        result_label.config(text=f"Results:\n{result_text}")
    else:
        result_label.config(text="No books found.")

def display_all_books(library):
    if library:
        result_text = "\n".join([f"{book['title']} by {book['author']} ({book['year']}) - {'Read' if book['read'] else 'Unread'}" for book in library])
        result_label.config(text=f"All Books:\n{result_text}")
    else:
        result_label.config(text="Library is empty.")

def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    search_term_entry.delete(0, tk.END)

# GUI Setup
def setup_ui():
    root = tk.Tk()
    root.title("Library Manager")
    root.geometry("800x600")  # Set window size to 800x600 for better readability

    # Sidebar Frame
    sidebar_frame = tk.Frame(root, bg='#8B0000', width=200, height=600)
    sidebar_frame.grid(row=0, column=0, rowspan=6, sticky='nsew')

    # Library Frame
    library_frame = tk.Frame(root)
    library_frame.grid(row=0, column=1, sticky='nsew')

    # Sidebar Buttons
    add_button = tk.Button(sidebar_frame, text="Add Book", command=lambda: add_book(library), bg='#800000', fg='white', font=("Arial", 16))
    add_button.pack(fill=tk.X, padx=10, pady=10)

    remove_button = tk.Button(sidebar_frame, text="Remove Book", command=lambda: remove_book(library), bg='#800000', fg='white', font=("Arial", 16))
    remove_button.pack(fill=tk.X, padx=10, pady=10)

    search_button = tk.Button(sidebar_frame, text="Search Library", command=lambda: search_library(library), bg='#800000', fg='white', font=("Arial", 16))
    search_button.pack(fill=tk.X, padx=10, pady=10)

    display_button = tk.Button(sidebar_frame, text="Display All Books", command=lambda: display_all_books(library), bg='#800000', fg='white', font=("Arial", 16))
    display_button.pack(fill=tk.X, padx=10, pady=10)

    # Library Form
    title_label = tk.Label(library_frame, text="Title:", font=("Arial", 14))
    title_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
    global title_entry
    title_entry = tk.Entry(library_frame, font=("Arial", 14), width=30)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    author_label = tk.Label(library_frame, text="Author:", font=("Arial", 14))
    author_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)
    global author_entry
    author_entry = tk.Entry(library_frame, font=("Arial", 14), width=30)
    author_entry.grid(row=1, column=1, padx=10, pady=10)

    year_label = tk.Label(library_frame, text="Year:", font=("Arial", 14))
    year_label.grid(row=2, column=0, sticky='w', padx=10, pady=10)
    global year_entry
    year_entry = tk.Entry(library_frame, font=("Arial", 14), width=30)
    year_entry.grid(row=2, column=1, padx=10, pady=10)

    genre_label = tk.Label(library_frame, text="Genre:", font=("Arial", 14))
    genre_label.grid(row=3, column=0, sticky='w', padx=10, pady=10)
    global genre_entry
    genre_entry = tk.Entry(library_frame, font=("Arial", 14), width=30)
    genre_entry.grid(row=3, column=1, padx=10, pady=10)

    global read_var
    read_var = tk.BooleanVar()
    read_check = tk.Checkbutton(library_frame, text="Read", variable=read_var, font=("Arial", 14))
    read_check.grid(row=4, column=0, columnspan=2, pady=10)

    search_by_label = tk.Label(library_frame, text="Search by:", font=("Arial", 14))
    search_by_label.grid(row=5, column=0, sticky='w', padx=10, pady=10)
    global search_by_var
    search_by_var = tk.StringVar(value="title")
    search_by_menu = tk.OptionMenu(library_frame, search_by_var, "title", "author")
    search_by_menu.grid(row=5, column=1, padx=10, pady=10)

    search_term_label = tk.Label(library_frame, text="Search Term:", font=("Arial", 14))
    search_term_label.grid(row=6, column=0, sticky='w', padx=10, pady=10)
    global search_term_entry
    search_term_entry = tk.Entry(library_frame, font=("Arial", 14), width=30)
    search_term_entry.grid(row=6, column=1, padx=10, pady=10)

    global result_label
    result_label = tk.Label(library_frame, text="Results will appear here", font=("Arial", 14))
    result_label.grid(row=7, column=0, columnspan=2, pady=10)

    return root

# Main execution
if __name__ == '__main__':
    library = load_library()
    root = setup_ui()
    root.mainloop()
