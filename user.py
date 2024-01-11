# Name       : Dhiya Abdurrahman
# Student Id : 202352200028

import csv
from dataclasses import dataclass

from prettytable import PrettyTable


# Define the data structure for a user using dataclasses
@dataclass
class User:
    # User data structure
    id: str
    username: str
    password: str
    role: str

    def as_list(self) -> list[str]:
        return [
            self.id,
            self.username,
            self.password,
            self.role,
        ]

    # Method to convert User object to a string

    def to_str(self) -> str:
        return ",".join(self.as_list())


# Function to get users from a file and store them in a dictionary
def get_users() -> dict[str, User]:
    users = {}
    with open("data/user.txt", 'r') as f:
        reader = csv.reader(f)
        _ = next(reader)  # Remove first row
        for id, username, password, role in reader:
            # Create a User object for each line in the file
            user = User(
                id=id,
                username=username,
                password=password,
                role=role,
            )
            users[id] = user
    return users


# Function to write users to a file
def write_users(users: dict[str, User]):  # write user data/users.txt file
    user_str = [
        "id,username,password,role"
    ]
    for user in users.values():
        user_str.append(user.to_str())  # Convert each User object to a string

    with open("data/user.txt", "w+") as f:
        f.write("\n".join(user_str))  # Write the user data to the file


# Function to print user data
def print_users_data(users: dict[str, User]):
    print("ID - Username - Password - Role")
    for u in users.values():  # Iterate through the users
        print(u.id, u.username, u.password, u.role)  # Print user information


def show_users_info():
    users = get_users()
    table = PrettyTable()
    table.field_names = ["id", "username", "password", "role"]
    for user in users.values():
        table.add_row(user.as_list())

    print(table)
