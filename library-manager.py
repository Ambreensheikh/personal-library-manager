import streamlit as st # type: ignore
import json
import os

# File to store the data
data_file = 'library.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

def add_book(library):
    title = st.text_input('Enter title of the book: ')
    author = st.text_input('Enter author of the book: ')
    year = st.text_input('Enter year of the book: ')
    genre = st.text_input('Enter genre of the book: ')
    read = st.radio('Have you read the book?', ['Yes', 'No'])
    
    if st.button('Add Book'):
        new_book = {
            'title': title,
            'author': author,
            'year': year,
            'genre': genre,
            'read': read == 'Yes'
        }
        library.append(new_book)
        save_library(library)
        st.success(f'Book {title} added successfully!')

def remove_book(library):
    title = st.text_input('Enter title of the book to remove from library: ')
    
    if st.button('Remove Book'):
        initial_length = len(library)
        library = [book for book in library if book['title'].lower() != title.lower()]
        if len(library) > initial_length:
            save_library(library)
            st.success(f'Book {title} removed successfully!')
        else:
            st.error(f'Book {title} not found in library!')

def search_library(library):
    search_by = st.selectbox('Search by', ['Title', 'Author'])
    search_term = st.text_input(f'Enter the {search_by}: ')
    
    if st.button('Search'):
        search_term = search_term.lower()
        result = [book for book in library if search_term in book[search_by.lower()].lower()]
        
        if result:
            for book in result:
                status = 'Read' if book['read'] else 'Unread'
                st.write(f"{book['title']} by {book['author']} published in {book['year']} is {status}")
        else:
            st.error(f'No books found for {search_term} in the {search_by} field')

def display_all_books(library):
    if library:
        for book in library:
            status = 'Read' if book['read'] else 'Unread'
            st.write(f"{book['title']} by {book['author']} published in {book['year']} is {status}")
    else:
        st.info('Library is empty')

def main():
    # Set up Streamlit UI styling
    st.set_page_config(page_title="Personal Library Manager", page_icon="📚")
    
    st.markdown("""
    <style>
        body {
            background-color: #D3A6FF;
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: #ADD8E6;
            color: white;
        }
        .stButton>button {
            background-color: #6A5ACD;
            color: white;
        }
        .stRadio>div>div>label {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    library = load_library()

    st.title("Personal Library Manager")
    st.header("Library Manager")

    menu = ["Add Book", "Remove Book", "Search Library", "Display All Books", "Exit"]
    choice = st.sidebar.selectbox("Choose an option", menu)

    if choice == 'Add Book':
        add_book(library)
    elif choice == 'Remove Book':
        remove_book(library)
    elif choice == 'Search Library':
        search_library(library)
    elif choice == 'Display All Books':
        display_all_books(library)
    elif choice == 'Exit':
        st.write("See You Again!")

if __name__ == '__main__':
    main()
