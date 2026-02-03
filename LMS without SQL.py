import tkinter as tk
from tkinter import messagebox
import csv
import os

FILE_NAME = "library.csv"

# Create CSV file if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Book ID", "Title", "Author"])


def add_book():
    bid = entry_id.get()
    title = entry_title.get()
    author = entry_author.get()

    if not bid or not title or not author:
        messagebox.showerror("Error", "All fields are required")
        return

    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([bid, title, author])

    clear_fields()
    view_books()
    messagebox.showinfo("Success", "Book added successfully")


def view_books():
    listbox.delete(0, tk.END)
    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            listbox.insert(tk.END, "|".join(row))


def search_book():
    bid = entry_id.get()
    if not bid:
        messagebox.showerror("Error", "Enter Book ID to search")
        return

    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == bid:
                entry_title.delete(0, tk.END)
                entry_author.delete(0, tk.END)
                entry_title.insert(0, row[1])
                entry_author.insert(0, row[2])
                messagebox.showinfo("Found", "Book found")
                return

    messagebox.showerror("Not Found", "Book ID not found")


def update_book():
    bid = entry_id.get()
    title = entry_title.get()
    author = entry_author.get()

    if not bid or not title or not author:
        messagebox.showerror("Error", "All fields required")
        return

    updated = False
    data = []

    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        data = list(reader)

    for i in range(1, len(data)):
        if data[i][0] == bid:
            data[i] = [bid, title, author]
            updated = True
            break

    if not updated:
        messagebox.showerror("Error", "Book ID not found")
        return

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    view_books()
    messagebox.showinfo("Success", "Book updated successfully")


def delete_book():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a book to delete")
        return

    data = []
    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        data = list(reader)

    data.pop(selected[0] + 1)

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    view_books()
    messagebox.showinfo("Deleted", "Book deleted successfully")


def clear_fields():
    entry_id.delete(0, tk.END)
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)


# GUI
root = tk.Tk()
root.title("Library Management System")
root.geometry("520x420")

tk.Label(root, text="Book ID").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="Title").pack()
entry_title = tk.Entry(root)
entry_title.pack()

tk.Label(root, text="Author").pack()
entry_author = tk.Entry(root)
entry_author.pack()

tk.Button(root, text="Add Book", command=add_book).pack(pady=3)
tk.Button(root, text="Search Book", command=search_book).pack(pady=3)
tk.Button(root, text="Update Book", command=update_book).pack(pady=3)
tk.Button(root, text="Delete Book", command=delete_book).pack(pady=3)

listbox = tk.Listbox(root, width=65)
listbox.pack(pady=10)

view_books()
root.mainloop()
