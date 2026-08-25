# CRUD operation : Create/Read/Update/Delete
import sqlite3

# Create tables
def create_tables():
    connection = sqlite3.connect('advpy.db')
    cursor = connection.cursor()
    # Query to create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        city TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

def insert_user(name,age,city):
    connection = sqlite3.connect('advpy.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name,age,city) VALUES (?,?,?)",(name,age,city))
    user_id = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return user_id

# Inserting multiple rows of data
def insert_many_users(users_list):
    connection = sqlite3.connect('advpy.db')
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO users (name,age,city) VALUES (?,?,?)",users_list)
    connection.commit()
    cursor.close()
    connection.close()

# Read users list/data
def get_all_users():
    connection = sqlite3.connect('advpy.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

# Read by user id
def get_user_by_id(user_id):
    connection = sqlite3.connect('advpy.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?",(user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

# Update
def update_user_by_age(new_age,user_id):
    connection = sqlite3.connect('advpy.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET age = ? WHERE id = ?",(new_age,user_id))
    rows_affected = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()
    return rows_affected

# Delete
def delete_user(user_id):
    connection = sqlite3.connect('advpy.db')
    cursor = connection.cursor()
    cursor.execute("Delete from users WHERE id = ?",(user_id,))
    rows_deleted = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()
    return rows_deleted

def crud_demo():
    create_tables()
    print("Table created.")
    # Insert
    insert_user('Rakesh',36,'Mysore')
    insert_user('Keerthi',30,'Mysore')
    print("User inserted.")

    insert_many_users([
        ('Sumith',20,'Bengaluru'),
        ('Pasu',39,'Indore')
    ])
    print("Multiple Users inserted.")

    print("\nAll Users List.")
    users = get_all_users()
    for user in users:
        print(f" {user}")

    print("\nAll Users List.")
    user = get_user_by_id(2)
    print(f" {user}")

    print("Updating user")
    rows_updated = update_user_by_age(33,2)
    print(f" Updated {rows_updated} row(s)")

    print("\nAll Users List.")
    users = get_all_users()
    for user in users:
        print(f" {user}")

    print("Deleting user")
    rows_updated = delete_user(4)
    print(f" Deleted {rows_updated} row(s)")

    print("\nAll Users List.")
    users = get_all_users()
    for user in users:
        print(f" {user}")

crud_demo()