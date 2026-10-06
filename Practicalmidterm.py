import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


conn = sqlite3.connect("song.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Song(
    song INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    genre TEXT NOT NULL
)
""")

conn.commit()


# =========================
# CREATE
# =========================

def add_song():
    name = name_entry.get()
    age = age_entry.get()
    genre = genre_entry.get()

    if name == "" or age == "" or genre == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute(
        "INSERT INTO Song (name, age, genre) VALUES (?, ?, ?)",
        (name, age, genre)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Song added successfully."
    )

    clear_fields()
    display_songs()


# =========================
# READ
# =========================

def display_songs():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM Song")

    songs = cursor.fetchall()

    for song in songs:
        tree.insert(
            "",
            tk.END,
            values=(song[1], song[2], song[3])
        )


# =========================
# UPDATE
# =========================

def update_song():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a song to update."
        )
        return

    selected_values = tree.item(selected[0])["values"]

    old_name = selected_values[0]
    old_age = selected_values[1]
    old_genre = selected_values[2]

    cursor.execute("""
        SELECT song
        FROM Song
        WHERE name = ? AND age = ? AND genre = ?
    """, (old_name, old_age, old_genre))

    result = cursor.fetchone()

    if result is None:
        messagebox.showerror(
            "Error",
            "Song record not found."
        )
        return

    song_id = result[0]

    name = name_entry.get()
    age = age_entry.get()
    genre = genre_entry.get()

    if name == "" or age == "" or genre == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute("""
        UPDATE Song
        SET name = ?, age = ?, genre = ?
        WHERE song = ?
    """, (name, age, genre, song_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Song updated successfully."
    )

    clear_fields()
    display_songs()


# =========================
# DELETE
# =========================

def delete_song():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a song to delete."
        )
        return

    selected_values = tree.item(selected[0])["values"]

    name = selected_values[0]
    age = selected_values[1]
    genre = selected_values[2]

    cursor.execute("""
        SELECT song
        FROM Song
        WHERE name = ? AND age = ? AND genre = ?
    """, (name, age, genre))

    result = cursor.fetchone()

    if result is None:
        messagebox.showerror(
            "Error",
            "Song record not found."
        )
        return

    song_id = result[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this song?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM Song WHERE song = ?",
            (song_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Song deleted successfully."
        )

        clear_fields()
        display_songs()


# =========================
# CLEAR
# =========================

def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)


# =========================
# EXIT
# =========================

def exit_program():
    conn.close()
    root.destroy()


# =========================
# SELECT SONG
# =========================

def select_song(event):
    selected = tree.selection()

    if selected:
        song = tree.item(selected[0])["values"]

        clear_fields()

        name_entry.insert(0, song[0])
        age_entry.insert(0, song[1])
        genre_entry.insert(0, song[2])


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Song Artist Information")
root.geometry("700x500")


# =========================
# LIGHT PINK COLORS
# =========================

BG_COLOR = "#FFE6F0"
FRAME_COLOR = "#FFF5F8"
TITLE_COLOR = "#D81B60"
LABEL_COLOR = "#C2185B"
ENTRY_BG = "#FFFFFF"

ADD_COLOR = "#F48FB1"
UPDATE_COLOR = "#F06292"
DELETE_COLOR = "#EC407A"
CLEAR_COLOR = "#E91E63"
EXIT_COLOR = "#D81B60"

TABLE_HEADER = "#F48FB1"
TABLE_SELECTED = "#F06292"

BUTTON_TEXT = "white"

root.configure(bg=BG_COLOR)


# =========================
# TITLE
# =========================

title_label = tk.Label(
    root,
    text="Song Artist Information",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

title_label.pack(pady=15)


# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(
    root,
    bg=FRAME_COLOR,
    bd=2,
    relief="groove"
)

input_frame.pack(
    pady=5,
    padx=20
)


# =========================
# NAME
# =========================

tk.Label(
    input_frame,
    text="Name:",
    font=("Arial", 10, "bold"),
    bg=FRAME_COLOR,
    fg=LABEL_COLOR
).grid(
    row=0,
    column=0,
    padx=10,
    pady=7
)

name_entry = tk.Entry(
    input_frame,
    width=30,
    bg=ENTRY_BG,
    fg="#333333",
    relief="solid",
    bd=1
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=7
)


# =========================
# AGE
# =========================

tk.Label(
    input_frame,
    text="Age:",
    font=("Arial", 10, "bold"),
    bg=FRAME_COLOR,
    fg=LABEL_COLOR
).grid(
    row=1,
    column=0,
    padx=10,
    pady=7
)

age_entry = tk.Entry(
    input_frame,
    width=30,
    bg=ENTRY_BG,
    fg="#333333",
    relief="solid",
    bd=1
)

age_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


# =========================
# GENRE
# =========================

tk.Label(
    input_frame,
    text="Genre:",
    font=("Arial", 10, "bold"),
    bg=FRAME_COLOR,
    fg=LABEL_COLOR
).grid(
    row=2,
    column=0,
    padx=10,
    pady=7
)

genre_entry = tk.Entry(
    input_frame,
    width=30,
    bg=ENTRY_BG,
    fg="#333333",
    relief="solid",
    bd=1
)

genre_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=7
)


# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

button_frame.pack(pady=12)


# =========================
# ADD BUTTON
# =========================

tk.Button(
    button_frame,
    text="Add",
    width=10,
    bg=ADD_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#F06292",
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=add_song
).grid(
    row=0,
    column=0,
    padx=4
)


# =========================
# UPDATE BUTTON
# =========================

tk.Button(
    button_frame,
    text="Update",
    width=10,
    bg=UPDATE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#EC407A",
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=update_song
).grid(
    row=0,
    column=1,
    padx=4
)


# =========================
# DELETE BUTTON
# =========================

tk.Button(
    button_frame,
    text="Delete",
    width=10,
    bg=DELETE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#D81B60",
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=delete_song
).grid(
    row=0,
    column=2,
    padx=4
)


# =========================
# CLEAR BUTTON
# =========================

tk.Button(
    button_frame,
    text="Clear",
    width=10,
    bg=CLEAR_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#C2185B",
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=4
)


# =========================
# EXIT BUTTON
# =========================

tk.Button(
    button_frame,
    text="Exit",
    width=10,
    bg=EXIT_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#AD1457",
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=exit_program
).grid(
    row=0,
    column=4,
    padx=4
)


# =========================
# TABLE STYLE
# =========================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview.Heading",
    background=TABLE_HEADER,
    foreground="white",
    font=("Arial", 10, "bold"),
    relief="flat"
)

style.configure(
    "Treeview",
    background="white",
    foreground="#333333",
    fieldbackground="white",
    rowheight=30,
    font=("Arial", 10)
)

style.map(
    "Treeview",
    background=[
        ("selected", TABLE_SELECTED)
    ],
    foreground=[
        ("selected", "white")
    ]
)


# =========================
# TABLE
# =========================

tree = ttk.Treeview(
    root,
    columns=("Name", "Age", "Genre"),
    show="headings"
)

tree.heading(
    "Name",
    text="Name"
)

tree.heading(
    "Age",
    text="Age"
)

tree.heading(
    "Genre",
    text="Genre"
)

tree.column(
    "Name",
    width=220,
    anchor="center"
)

tree.column(
    "Age",
    width=100,
    anchor="center"
)

tree.column(
    "Genre",
    width=220,
    anchor="center"
)

tree.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


# =========================
# SELECT EVENT
# =========================

tree.bind(
    "<<TreeviewSelect>>",
    select_song
)


# =========================
# DISPLAY RECORDS
# =========================

display_songs()


# =========================
# START APPLICATION
# =========================

root.mainloop()
