# Name       : Dhiya Abdurrahman
# Student Id : 202352200028

import csv
from _datetime import datetime
from typing import Optional

from dataclasses import dataclass
from book import Book
from user import User


@dataclass
class Borrow:
    id: str
    book: Book
    user: User
    borrow_date: datetime
    return_date: Optional[datetime] = None


    def to_str(self):
        dateformat = "%Y-%m-%d"
        return_date_str=""
        if self.return_date:
            return_date_str = self.return_date.strftime(dateformat)

        return ",".join([
            self.id,
            self.book.id,
            self.user.id,
            self.borrow_date.strftime(dateformat),
            return_date_str,
        ])


def get_borrows(users: dict[str, User], books: dict[str, Book]) -> dict[str, Borrow]:
    borrows = {}
    with open("data/borrow.txt", 'r') as f:
        reader = csv.reader(f)
        _ = next(reader)  # Remove first row
        for id, book_id, user_id, borrow_date, return_date in reader:
            b_year, b_month, b_day = map(int, borrow_date.split("-"))

            return_datetime = None
            if len(return_date.strip()) != 0:
                r_year, r_month, r_day = map(int, return_date.split("-"))
                return_datetime = datetime(year=r_year, month=r_month, day=r_day)

            borrow = Borrow(
                id=id,
                book=books[book_id],
                user=users[user_id],
                borrow_date=datetime(year=b_year, month=b_month, day=b_day),
                return_date=return_datetime
            )
            borrows[id] = borrow
    return borrows


def write_borrow(borrow: dict[str, Borrow]):
    borrows_str = [
        "id,book_id,user_id,borrow_date,return_date"
    ]
    for borrow in borrow.values():
        borrows_str.append(borrow.to_str())  # Convert each User object to a string

    with open("data/borrow.txt","w+") as f:
        f.write("\n".join(borrows_str))  # Write the user data to the file