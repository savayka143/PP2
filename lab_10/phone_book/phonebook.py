import psycopg2
import csv

DB_NAME = "phonebook"
DB_USER = "postgres"
DB_PASSWORD = "qwerty"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER,
        password=DB_PASSWORD, host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("Connected to database!")
except Exception as e:
    print("Connection error:", e)
    exit(1)

def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(30) NOT NULL
        );
    """)
    conn.commit()

def insert_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row['name'], row['phone'])
            )
        conn.commit()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cursor.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()

def update_contact():
    contact_id = input("Enter contact ID to update: ")
    new_name = input("Enter new name (or leave blank): ")
    new_phone = input("Enter new phone (or leave blank): ")
    if new_name and new_phone:
        cursor.execute("UPDATE contacts SET name=%s, phone=%s WHERE id=%s", (new_name, new_phone, contact_id))
    elif new_name:
        cursor.execute("UPDATE contacts SET name=%s WHERE id=%s", (new_name, contact_id))
    elif new_phone:
        cursor.execute("UPDATE contacts SET phone=%s WHERE id=%s", (new_phone, contact_id))
    else:
        print("No update performed")
        return
    conn.commit()

def query_by_filter():
    option = input("Search by 1) name or 2) phone? (Enter 1 or 2): ")
    if option == '1':
        search = input("Enter name to search: ")
        cursor.execute("SELECT * FROM contacts WHERE name ILIKE %s", ('%' + search + '%',))
    elif option == '2':
        search = input("Enter phone to search: ")
        cursor.execute("SELECT * FROM contacts WHERE phone ILIKE %s", ('%' + search + '%',))
    else:
        print("Invalid option")
        return
    for row in cursor.fetchall():
        print("ID:", row[0], "Name:", row[1], "Phone:", row[2])

def delete_contact():
    name = input("Enter name to delete: ")
    cursor.execute("DELETE FROM contacts WHERE name = %s", (name,))
    conn.commit()

def main_menu():
    create_table()
    while True:
        print("\n1: Insert from CSV")
        print("2: Insert from console")
        print("3: Update contact")
        print("4: Query contacts")
        print("5: Delete contact")
        print("6: Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            file_path = input("Enter CSV file path: ")
            insert_from_csv(file_path)
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_by_filter()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    try:
        main_menu()
    finally:
        cursor.close()
        conn.close()
