# Standard python libraries.
import sqlite3
import getpass
import secrets
import string

# Need to install ( pip install cryptography ).
# A library for encoding and decoding
from cryptography.fernet import Fernet

# To randomly generate the encryption key.
encryption_key = Fernet.generate_key()

cipher_suite = Fernet(encryption_key)

# Create and connect to the database file.
conn = sqlite3.connect("password_manager.db")

cursor = conn.cursor()

# To create a database table for passwords in the cache.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    )
''')
# To create in the database
conn.commit()


# To create a database table for users in the cache.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    )
''')
# To create in the database
conn.commit()


def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    # saving Password as bytes
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()

    cursor.execute("INSERT INTO users (username, password, encrypted_password) VALUES (?, ?)",
                   (username, encrypted_password))
    conn.commit()
    print("User registration successful!")


while True:
    print("\nPassword Manager:")
    print("\t1.Register:")
    print("\t2.Add Password:")
    print("\t3.View Password:")
    print("\t4.Change Password:")
    print("\t5.Delete Password:")
    print("\t6.EXIT:")

    choice = input("Select an option: ")

    if choice == "1":
        register_user()

conn.close()
