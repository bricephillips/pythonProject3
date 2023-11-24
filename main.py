import tkinter as tk
from tkinter import simpledialog
import sqlite3

def add_user():
    fname = entry_fname.get()
    lname = entry_lname.get()

    if fname and lname:
        user_data = (fname, lname)
        listbox.insert(tk.END, user_data)
        entry_fname.delete(0, tk.END)
        entry_lname.delete(0, tk.END)
        # Add the user to the SQLite database
        insert_user_into_database(user_data)

def remove_user():
    selected_index = listbox.curselection()
    if selected_index:
        user_data = listbox.get(selected_index[0])
        listbox.delete(selected_index)
        # Remove the user from the SQLite database
        delete_user_from_database(user_data)

def update_user():
    selected_index = listbox.curselection()
    if selected_index:
        old_user_data = listbox.get(selected_index[0])
        # Show a pop-up for updating user information
        new_user_data = show_update_popup(old_user_data)
        if new_user_data:
            listbox.delete(selected_index)
            listbox.insert(tk.END, new_user_data)
            # Update the user in the SQLite database
            update_user_in_database(old_user_data, new_user_data)

def show_update_popup(old_user_data):
    # Show a pop-up for updating user information
    new_user_data = simpledialog.askstring("Update User", "Enter new information (fname lname):", initialvalue=" ".join(old_user_data))
    if new_user_data:
        new_user_data = tuple(new_user_data.split())
        return new_user_data
    return None

def insert_user_into_database(user_data):
    # Connect to the SQLite database
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    # Execute an SQL query to insert the user into the database
    cursor.execute("INSERT INTO users (fname, lname) VALUES (?, ?)", user_data)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

def delete_user_from_database(user_data):
    # Connect to the SQLite database
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    # Execute an SQL query to delete the user from the database
    cursor.execute("DELETE FROM users WHERE fname=? AND lname=?", user_data)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

def update_user_in_database(old_user_data, new_user_data):
    # Connect to the SQLite database
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    # Execute an SQL query to update the user in the database
    cursor.execute("UPDATE users SET fname=?, lname=? WHERE fname=? AND lname=?", (*new_user_data, *old_user_data))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Create the main window
window = tk.Tk()
window.title("GUI with SQLite")

# Create and pack entries for user input
entry_fname = tk.Entry(window)
entry_fname.pack(pady=5)
entry_lname = tk.Entry(window)
entry_lname.pack(pady=5)

# Create and pack the "Add" button
add_button = tk.Button(window, text="Add User", command=add_user)
add_button.pack(pady=5)

# Create and pack the "Remove" button
remove_button = tk.Button(window, text="Remove User", command=remove_user)
remove_button.pack(pady=5)

# Create and pack the "Update" button
update_button = tk.Button(window, text="Update User", command=update_user)
update_button.pack(pady=5)

# Create and pack a list box at the bottom
listbox = tk.Listbox(window)
listbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Connect to the SQLite database and create a "users" table if it doesn't exist
connection = sqlite3.connect('test.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT, lname TEXT)")
connection.commit()
connection.close()

# Load existing users from the database and populate the list box
connection = sqlite3.connect('test.db')
cursor = connection.cursor()
cursor.execute("SELECT fname, lname FROM users")
users = cursor.fetchall()
for user_data in users:
    listbox.insert(tk.END, user_data)
connection.close()

# Run the Tkinter event loop
window.mainloop()
