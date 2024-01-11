# Name       : Dhiya Abdurrahman
# Student Id : 202352200028

import csv
from dataclasses import dataclass

from prettytable import PrettyTable
from user import get_users


# Define the data structure for a book using dataclasses
@dataclass
class Book:
    # Book structure
    id: str
    isbn: str
    title: str
    description: str

    # Method to convert Book object to a string
    def to_str(self) -> str:
        return ",".join([
            self.id,
            self.isbn,
            self.title,
            self.description,
        ])

    def as_list(self) -> list[str]:
        return [
            self.id,
            self.isbn,
            self.title,
            self.description,
        ]


# Function to get books from a file and store them in a dictionary
def get_books() -> dict[str, Book]:
    books = {}
    with open("data/books.txt", 'r') as f:
        reader = csv.reader(f)
        _ = next(reader)  # Remove first row
        for id, isbn, title, description in reader:
            # Create a Book object for each line in the file
            book = Book(
                id=id,
                isbn=isbn,
                title=title,
                description=description,
            )
            books[id] = book
    return books


# Function to write books to a file
def write_books(books: dict[str, Book]):  # Write a book data/books.txt file
    book_str = [
        "id,isbn,title,description"
    ]
    for book in books.values():
        book_str.append(book.to_str())  # Convert each Book object to a string

    with open("data/books.txt", "w+") as f:
        f.write("\n".join(book_str))  # Write the book data to the file


# Function to print book data
def print_books_data(books: dict[str, Book]):
    print("ID - ISBN - Title - Description")
    for b in books.values():  # Iterate through the books
        print(b.id, b.isbn, b.title, b.description)  # Print book information








    # users["102"]= User(
    #     id="102",
    #     username="varen",
    #     password="varen",
    #     role="admin"
    # )
    #
    # write_users(users)
    # for u in users.values():
    #     print(u.id, u.username)
    #
    # books["101"] = Book(
    #     id="107",
    #     isbn="1909",
    #     title="hi",
    #     description="hello"
    # )
    #
    # write_books(books)
    # for b in books.values():
    #     print(b.id, b.isbn)
