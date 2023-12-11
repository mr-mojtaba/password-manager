# Standard python libraries.
import sqlite3
import getpass
import secrets
import string

# Need to install ( pip install cryptography ).
# A library for encoding and decoding
from cryptography.fernet import Fernet

# To randomly generate the encryption key.
# encryption_key = Fernet.generate_key()
encryption_key = b'YV0Mspw-sjFKElkftrFa21d9IRH50_Dz5aEshkzu7zc='

cipher_suite = Fernet(encryption_key)


# ---------- SQL ----------

# Create and connect to the database file.
conn = sqlite3.connect("password_manager.db")

cursor = conn.cursor()

# To create a database table for passwords in the cache.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
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


# ---------- Functions ----------


def register_user():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # To encrypt the password and save the Password as bytes.
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()

    # To add to the users' table in the database.
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, encrypted_password))

    # To create in the database.
    conn.commit()
    print("User registration successful!")


def login():
    global username
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # To select from the users' table in the database.
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))

    # To create a variable for user record found.
    user = cursor.fetchone()

    # To create a variable for the user's password.
    stored_password = user[2]

    if user:
        decrypted_password = cipher_suite.decrypt(stored_password.encode()).decode()
        if password == decrypted_password:
            print("Login Successful!")
            return True
    print("Login failed!\nPlease try again.")
    return False


def generate_strong_password(lenght=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    strong_password = "".join(secrets.choice(characters) for _ in range(lenght))
    return strong_password


def change_user_password():
    if not login():
        return
    new_password = getpass.getpass("Enter your password (or leave blank to generate strong password): ")

    if not new_password:
        new_password = generate_strong_password()
        print(f"Your new password is: {new_password}")

    # To encrypt the password and save the Password as bytes.
    encrypted_password = cipher_suite.encrypt(new_password.encode()).decode()

    # To update to the new password.
    cursor.execute("UPDATE users SET password=? WHERE username=?",
                   (encrypted_password, username))

    # To create in the database.
    conn.commit()
    print("Your new password changed successfully.")


def add_password():
    if not login():
        return
    website = input("Website or Service: ")
    username = input("Username: ")
    print("Do you want to generate a strong password for this service? (Y/N): ")
    generate_option = input()
    if generate_option.lower() == "y":
        password = generate_strong_password()
        print(f"Your password is: {password}")
    else:
        password = getpass.getpass("Enter your password: ")

    # To encrypt the password and save the Password as bytes.
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()

    # To add to the passwords' table in the database.
    cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                   (website, username, encrypted_password))

    # To create in the database.
    conn.commit()
    print("Password added successfully!")


def view_passwords():
    if not login():
        return
    cursor.execute("SELECT * FROM passwords")
    passwords = cursor.fetchall()
    for password in passwords:
        website = password[1]
        username = password[2]
        encrypted_password = password[3]
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        print(f"ID: {password[0]}, Website: {password[1]}, Username: {username}, Password: {decrypted_password}")


def delete_password():
    if not login():
        return
    password_id = input("Enter the password ID to delete: ")
    cursor.execute("DELETE FROM passwords WHERE id=?", (password_id,))
    conn.commit()
    print("Password deleted!")


# ---------- Project loop ----------

while True:
    print("\nPassword Manager:")
    print("\t1.Register")
    print("\t2.Change user Password")
    print("\t3.Add Password")
    print("\t4.View Passwords")
    print("\t5.Delete Password")
    print("\t6.EXIT")

    choice = input("Select an option: ")

    if choice == "1":
        register_user()
    elif choice == "2":
        change_user_password()
    elif choice == "3":
        add_password()
    elif choice == "4":
        view_passwords()
    elif choice == "5":
        delete_password()
    elif choice == "6":
        break
    else:
        print("Invalid choice!\nPlease select again")

conn.close()
