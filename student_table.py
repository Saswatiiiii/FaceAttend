import tkinter as tk
from tkinter import ttk
from tkinter import Frame, BOTH, RIDGE, END, Y, X, RIGHT, BOTTOM
import mysql.connector

class StudentTableWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Registered Students")
        self.root.geometry("1000x500")
        self.root.configure(bg="white")

        # Frame for the table
        table_frame = Frame(self.root, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=10, y=10, width=980, height=470)

        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_y = ttk.Scrollbar(table_frame, orient='vertical')

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("dep", "year", "session", "sem", "id", "name", "roll", "email", "phone", "photo"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Headings
        headings = {
            "dep": "Department", "year": "Year", "session": "Session", "sem": "Semester",
            "id": "Student ID", "name": "Name", "roll": "Roll", "email": "Email ID",
            "phone": "Phone No", "photo": "PhotoSampleStatus"
        }

        for col, text in headings.items():
            self.student_table.heading(col, text=text)
            self.student_table.column(col, width=100)

        self.student_table.column("photo", width=150)
        self.student_table["show"] = "headings"

        self.student_table.pack(fill=BOTH, expand=1)

        self.fetch_data()

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="saswati2006",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student")
            data = cursor.fetchall()

            if data:
                self.student_table.delete(*self.student_table.get_children())
                for row in data:
                    self.student_table.insert("", END, values=row)

            conn.commit()
            conn.close()
        except Exception as e:
            print("Error fetching data:", e)
