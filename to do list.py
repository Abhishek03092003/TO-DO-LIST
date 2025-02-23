import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
# This function initializes the database and creates a table if it doesn't exist.
def setup_db():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
    conn.commit()
    conn.close()

# Function to add a new task to the database and refresh the listbox.
def add_task():
    task = task_entry.get()
    if task:
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        task_entry.delete(0, tk.END)  # Clear the input field
        load_tasks()  # Refresh the displayed tasks
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Function to load and display tasks from the database.
def load_tasks():
    task_list.delete(0, tk.END)  # Clear the listbox
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        task_list.insert(tk.END, task[1])  # Insert each task into the listbox
    conn.close()

# Function to delete a selected task from the database and refresh the listbox.
def delete_task():
    try:
        selected_task = task_list.get(task_list.curselection())  # Get selected task
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task = ?", (selected_task,))
        conn.commit()
        conn.close()
        load_tasks()  # Refresh the displayed tasks
    except:
        messagebox.showwarning("Warning", "Please select a task to delete!")

# GUI setup
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x500")

# Entry field for new tasks
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

# Button to add a new task
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

# Listbox to display tasks
task_list = tk.Listbox(root, width=50, height=15)
task_list.pack(pady=10)

# Button to delete the selected task
delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

# Initialize the database and load tasks
setup_db()
load_tasks()

# Run the Tkinter event loop
root.mainloop()
