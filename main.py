# Name       : Dhiya Abdurrahman
# Student Id : 202352200028
from datetime import datetime
from typing import Dict
from prettytable import PrettyTable, SINGLE_BORDER

from borrow import get_borrows, Borrow, write_borrow
from user import User, get_users, print_users_data, write_users, show_users_info
from book import get_books, print_books_data, write_books, Book
from random import randint


# Function to attempt login
def login(username: str, password: str) -> User | None:
    users = get_users()  # Get all users data
    user = None

    for u in users.values():
        if u.username == username:
            user = u
    if user is None:
        print("User not found")
        return
    if user.password != password:
        print("Password didn't match")
        return
    print("Login Successful!")
    return user


# Function to register a new user
def register(username: str, password) -> User:
    users = get_users()

    id = randint(100, 400)  # Generate random id
    while str(id) in users.keys():
        id = randint(100, 400)

    id = str(id)  # Create random id to avoid the conflict
    users[id] = User(
        id=id,
        username=username,
        password=password,
        role="member"
    )

    write_users(users)  # Save the user data
    return users[id]  # Return the newly created of users accounts


# Prompt Username and password
def input_username_password(username_prompt="Input Username>", password_prompt="Input Password>"):
    username = input(username_prompt)
    password = input(password_prompt)
    return username, password


# Main program logic
def main():
    while True:
        user = None

        pt = PrettyTable()
        pt.title = "Welcome to Library"
        pt.field_names = ["Cmd", "Menu"]
        pt.set_style(SINGLE_BORDER)
        pt.add_row(["1", "Login"])
        pt.add_row(["2", "Register"])
        print(pt)  # Print display menu

        cmd = get_user_input()
        if cmd == 1:
            # User choose to Login
            username, password = input_username_password()
            user = login(username, password)
        elif cmd == 2:
            # User chose to register
            username = input("Input Username>")
            password = input("Input Password>")
            user = register(username, password)  # Register a new user
            print("User Created", user)

        if user:
            user_menu(user)


# User Menu
def get_random_id(source):
    id = randint(100, 400)
    while str(id) in source:
        id = randint(100, 400)
    return str(id)

def borrow_book(user, books, borrows):
    book_menu = show_borrow_info()

    cmd = get_user_input()
    available, _ = book_menu[cmd]
    if not available:
        print("This book is not available")
        return

    print("Are you sure you want to lend a book?", books[available[0]].to_str())
    confirm = input("Are you SURE?(Y/N)?")
    if confirm == 'Y' or confirm == 'y':
        id = get_random_id(borrows.keys())
        borrows[id] = Borrow(
            id=id,
            user=user,
            book=books[available[0]],
            borrow_date=datetime.now(),
        )
        write_borrow(borrows)

def show_user_borrow(user,borrows):
    dateformat = "%Y-%m-%d"
    options = []
    table = PrettyTable()
    table.field_names = [
        "id",
        "isbn",
        "title",
        "borrow_date",
        "return_date"
    ]
    for k, borrow in borrows.items():
        if borrow.user != user:
            continue

        b_date = borrow.borrow_date.strftime(dateformat)

        r_date = ""
        if borrow.return_date:
            r_date = borrow.return_date.strftime(dateformat)
        options.append(borrow.id)
        table.add_row(
            [
                borrow.id,
                borrow.book.isbn,
                borrow.book.title,
                b_date,
                r_date,
            ]
        )
    print(table)
    return options


def user_menu(user: User):
    while True:
        books = get_books()
        users = get_users()
        borrows = get_borrows(users, books)

        if user.role == "Member":
            print("-------- Welcome to Member Menu -------")
            user_borrows = show_user_borrow(user, borrows)
            print("1.Borrow Book")
            print("2.Return Book")
            print("3.Back")
            print("0.Logout")
            cmd = get_user_input()
            if cmd == 1:
                borrow_book(user, books, borrows)
            elif cmd == 2:
                print("which book do you want to return?")
                cmd = str(get_user_input())
                if cmd not in user_borrows:
                    print("Invalid input, cannot return this book")
                    continue

                b = borrows[cmd]
                b.return_date = datetime.now()
                borrows[cmd] = b
                print(borrows[cmd])

                write_borrow(borrows)
            elif cmd == 0:
                break
        else:
            print("-------- Welcome to Admin Menu -------")
            print("1.Manage user")
            print("2.Manage book")

            cmd = get_user_input()
            if cmd == 1:
                manage_user()
            elif cmd == 2:
                manage_book()


def prompt_exist_user(users: dict[str, User], prompt: str) -> str:
    user_id = None
    while True:
        print(prompt)
        user_id = str(get_user_input())
        if user_id not in users:
            print("User not exist")
            continue
        break


def manage_user():
    while True:
        users = get_users()
        show_users_info()
        print("1.Add User")
        print("2.Edit User")
        print("3.Delete User")
        print("0. Back to Admin Menu")

        cmd = get_user_input()
        if cmd == 1:
            print("Adding user")
            username = input("Input Username>")
            password = input("Input Password>")
            _ = register(username, password)  # variablenya moal dipake
        elif cmd == 2:
            user_id = prompt_exist_user(users, "please input user id you want to edit")
            target = users[user_id]
            print(f"Editing user: [{target.id} - {target.username}]")

            username, password = input_username_password(
                "New Username",
                "New Password",
            )
            target.username = username
            target.password = password

            write_users(users)
        elif cmd == 3:
            user_id = prompt_exist_user(users, "Please input user id you want to delete")  # select user id
            confirm = input("Are you SURE?(Y/N)")
            if confirm == 'Y' or confirm == 'y':
                del users[user_id]
                write_users(users)
        elif cmd == 0:
            break


def get_user_input() -> int:
    while True:
        try:
            cmd = int(input("Input the command>"))
            return cmd
        except ValueError:
            print("Please Input the correct value again")


def prompt_available_book(books: dict[str, Book], prompt: str) -> str:  # id, isbn, title, description
    book_str = None
    while True:
        print(prompt)
        book_str = str(get_book_input())
        if book_str not in books:
            print("Books is not available")
            continue
        break
    return book_str


def manage_book():
    while True:
        books = get_books()
        show_book_info()
        print("1.Add Book")
        print("2.Delete Book")
        print("0. Back to Admin Menu")

        cmd = get_book_input()
        if cmd == 1:
            print("Adding Book")
            isbn = input("Input ISBN>")
            title = input("Input title>")
            description = input("Input description: ")

            id = randint(100, 400)  # Generate random id
            while str(id) in books.keys():
                id = randint(100, 400)

            id= str(id)  # Create random id to avoid the conflict
            books[id] = Book(
                id=id,
                isbn=isbn,
                title=title,
                description=description
            )

            write_books(books)

            print("Book added successfully.")
        elif cmd == 2:
            book_id = prompt_available_book(books, "Please input book id you want to delete")  # select user id
            confirm = input("Are you SURE?(Y/N)")
            if confirm == 'Y' or confirm == 'y':
                del books[book_id]
                write_books(books)
            pass
        elif cmd == 0:
            break
    pass


# Display Book
def show_book_info():
    books = get_books()

    table = PrettyTable()
    table.field_names = ["id", "isbn", "title", "description"]
    for book in books.values():
        table.add_row(book.as_list())

    print(table)


def get_stock(books: dict[str, Book], borrows: dict[str, Borrow]):
    isbns = set([x.isbn for x in books.values()])
    isbns = sorted(isbns)

    borrowed = {}
    for isbn in isbns:
        borrowed[isbn] = {
            x.book.id
            for x in borrows.values()
            if x.book.isbn == isbn and x.return_date == None
        }

    total_stock = {}
    for isbn in isbns:
        total_stock[isbn] = [x.id for x in books.values() if x.isbn == isbn]

    stock = {}
    for isbn, value in total_stock.items():
        stock[isbn] = (
            list(set(value) - set(borrowed[isbn])),  # available
            borrowed[isbn],
        )
    return stock


def show_borrow_info():
    users = get_users()
    books = get_books()
    borrows = get_borrows(users, books)

    table = PrettyTable()
    table.field_names = [
        "cmd",
        "isbn",
        "title",
        "description",
        "avail / total",
    ]

    stock = get_stock(books, borrows)
    cmd_isbn = {i + 1: stock[isbn] for i, isbn in enumerate(stock.keys())}
    for i, the_stocks in cmd_isbn.items():
        available, borrow = the_stocks
        try:
            book_id = available[0]
        except:
            book_id = borrow[0]

        book_data = books[book_id]
        total = len(available) + len(borrow)
        table.add_row(
            [
                i,
                book_data.isbn,
                book_data.title,
                book_data.description,
                f"{len(available)}/{total}",
            ]
        )
    # table.sortby = "isbn"
    print(table)
    return cmd_isbn


def get_book_input() -> int:
    while True:
        try:
            cmd = int(input(">"))
            return cmd
        except ValueError:
            print("Please Input the correct value again")


# Run the main function if this script is executed
if __name__ == "__main__":
    main()

    # users = get_users()
    # print_users_data(users)
    #
    # books = get_books()
    # print_books_data(books)
