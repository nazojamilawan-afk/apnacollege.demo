
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE NOT NULL,
    department TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    entry_date TEXT,
    entry_time TEXT
)
""")

conn.commit()

# Main window
root = tk.Tk()
root.title("Library Entrance Management System")
root.geometry("850x600")
root.configure(bg="#eaf0f6")

# Heading
heading = tk.Label(
    root,
    text="LIBRARY ENTRANCE MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg="#173b63",
    fg="white",
    pady=20
)
heading.pack(fill="x")

# Student registration
def register_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    department = dept_entry.get().strip()

    if not name or not roll or not department:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        cursor.execute(
            "INSERT INTO students (name, roll_no, department) VALUES (?, ?, ?)",
            (name, roll, department)
        )
        conn.commit()
        messagebox.showinfo("Success", "Student Registered Successfully!")

        name_entry.delete(0, tk.END)
        roll_entry.delete(0, tk.END)
        dept_entry.delete(0, tk.END)

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll Number Already Exists")

# Student entrance
def student_entry():
    roll = entrance_entry.get().strip()

    cursor.execute(
        "SELECT id, name FROM students WHERE roll_no = ?",
        (roll,)
    )

    student = cursor.fetchone()

    if student:
        student_id, name = student

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        cursor.execute(
            "INSERT INTO entries (student_id, entry_date, entry_time) VALUES (?, ?, ?)",
            (student_id, date, time)
        )
        conn.commit()

        messagebox.showinfo(
            "Welcome",
            f"Welcome {name}!\nEntry Recorded Successfully.\nDate: {date}\nTime: {time}"
        )

        entrance_entry.delete(0, tk.END)

        show_records()

    else:
        messagebox.showerror("Error", "Student Not Found!")

# Show records
def show_records():
    for row in table.get_children():
        table.delete(row)

    cursor.execute("""
        SELECT students.name, students.roll_no,
               students.department, entries.entry_date,
               entries.entry_time
        FROM entries
        JOIN students ON entries.student_id = students.id
        ORDER BY entries.id DESC
    """)

    for record in cursor.fetchall():
        table.insert("", tk.END, values=record)

# Student registration section
registration = tk.LabelFrame(
    root,
    text="Student Registration",
    font=("Arial", 12, "bold"),
    bg="white",
    padx=15,
    pady=15
)
registration.pack(fill="x", padx=20, pady=15)

tk.Label(registration, text="Student Name", bg="white").grid(row=0, column=0)
name_entry = tk.Entry(registration, width=22)
name_entry.grid(row=0, column=1, padx=10)

tk.Label(registration, text="Roll Number", bg="white").grid(row=0, column=2)
roll_entry = tk.Entry(registration, width=22)
roll_entry.grid(row=0, column=3, padx=10)

tk.Label(registration, text="Department", bg="white").grid(row=1, column=0, pady=15)
dept_entry = tk.Entry(registration, width=22)
dept_entry.grid(row=1, column=1)

tk.Button(
    registration,
    text="Register Student",
    command=register_student,
    bg="#173b63",
    fg="white",
    padx=15
).grid(row=1, column=3, pady=10)

# Entrance section
entrance = tk.LabelFrame(
    root,
    text="Student Library Entrance",
    font=("Arial", 12, "bold"),
    bg="white",
    padx=15,
    pady=15
)
entrance.pack(fill="x", padx=20, pady=10)

tk.Label(entrance, text="Enter Roll Number:", bg="white").pack(side="left")

entrance_entry = tk.Entry(entrance, width=25)
entrance_entry.pack(side="left", padx=10)

tk.Button(
    entrance,
    text="Record Entry",
    command=student_entry,
    bg="green",
    fg="white",
    padx=15
).pack(side="left")

# Records table
records = tk.LabelFrame(
    root,
    text="Library Entrance Records",
    font=("Arial", 12, "bold"),
    bg="white",
    padx=10,
    pady=10
)
records.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("Name", "Roll No", "Department", "Date", "Time")

table = ttk.Treeview(
    records,
    columns=columns,
    show="headings"
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=140)

table.pack(fill="both", expand=True)

tk.Button(
    root,
    text="Refresh Records",
    command=show_records,
    bg="#173b63",
    fg="white"
).pack(pady=5)

# Load records when application starts
show_records()

root.mainloop()

# Close database when application exits
conn.close()
