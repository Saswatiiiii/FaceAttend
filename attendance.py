from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime
import os
import csv

mydata = []  # Global list to store attendance data

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance System")

        # Fullscreen setup
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Background Image
        img = Image.open(r"c:\\Users\\Saswati\\Downloads\\InShot_20250103_200118897.jpg")
        img = img.resize((screen_width, screen_height - 300), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        bg_img = Label(self.root, image=self.photoimg)
        bg_img.place(x=0, y=300, width=screen_width, height=screen_height - 300)

        # Header Image
        img = Image.open(r"c:\\Users\\Saswati\\Downloads\\InShot_20250219_222820469.jpg")
        img = img.resize((1530, 300), Image.Resampling.LANCZOS)
        self.photoimg_header = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg_header)
        f_lbl.place(x=0, y=0, width=1530, height=300)

        main_frame = Frame(bg_img, bd=2)
        main_frame.place(x=0, y=0, width=1480, height=490)

        # Right Frame - Attendance Table
        Right_frame = LabelFrame(
            main_frame, bd=2, bg="white", relief=RIDGE, text="Attendance Details",
            font=("times new roman", 12, "bold"), fg="darkblue"
        )
        Right_frame.place(x=0, y=0, width=screen_width, height=500)

        # Search Frame
        search_frame = LabelFrame(Right_frame, text="Search", font=("times new roman", 12, "bold"), bg="white", fg="darkblue")
        search_frame.place(x=0, y=0, width=screen_width, height=60)

        # Search by Roll Label
        Label(search_frame, text="Search by Roll:", font=("times new roman", 12), bg="white").place(x=10, y=5)
        
        self.search_var = StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20, font=("times new roman", 12))
        self.search_entry.place(x=140, y=5)

        Button(search_frame, text="Search", command=self.search_data, width=12, font=("times new roman", 12, "bold"), bg="blue", fg="white").place(x=320, y=5)
        
        # Search by Name Label
        Label(search_frame, text="Search by Name:", font=("times new roman", 12), bg="white").place(x=470, y=5)

        self.name_search_var = StringVar()
        self.name_search_entry = ttk.Entry(search_frame, textvariable=self.name_search_var, width=25, font=("times new roman", 12))
        self.name_search_entry.place(x=600, y=5)

        Button(search_frame, text="Search Name", command=self.search_by_name, width=15, font=("times new roman", 12, "bold"), bg="purple", fg="white").place(x=820, y=5)

        # Search by Date
        Label(search_frame, text="Search by Date:", font=("times new roman", 12), bg="white").place(x=1000, y=5)

        self.date_search = DateEntry(search_frame, width=15, font=("times new roman", 12), background="darkblue", foreground="white", borderwidth=2, date_pattern='dd-mm-yyyy')
        self.date_search.place(x=1110, y=5)

        Button(search_frame, text="Search Date", command=self.search_by_date, width=15, font=("times new roman", 12, "bold"), bg="green", fg="white").place(x=1270, y=5)

        # Table Frame
        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=0, y=90, width=screen_width, height=380)

        self.AttendanceReportTable = ttk.Treeview(
            table_frame, columns=("Attendance ID", "Roll", "Name", "Department", "Time", "Date", "Attendance"), show="headings"
        )

        for col in self.AttendanceReportTable["columns"]:
            self.AttendanceReportTable.heading(col, text=col)
            self.AttendanceReportTable.column(col, width=100)

        self.AttendanceReportTable.pack(fill=BOTH, expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)

        self.loadAttendanceData()

        # Back Button
        self.back_button = Button(self.root, text="Back", command=self.go_back, font=("times new roman", 12, "bold"), width=12, bg="red", fg="white")
        self.back_button.place(x=screen_width - 150, y=screen_height - 100, width=120, height=40)

    def loadAttendanceData(self):
        global mydata
        mydata.clear()

        if os.path.exists("attendance.csv"):
            with open("attendance.csv", "r", newline="") as file:
                csvreader = csv.reader(file)
                next(csvreader, None)
                for row in csvreader:
                    mydata.append(row)

        self.fetchData(mydata)

    def fetchData(self, rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for row in rows:
            self.AttendanceReportTable.insert("", END, values=row)

    def get_cursor(self, event=""):
        cursor_row = self.AttendanceReportTable.focus()
        content = self.AttendanceReportTable.item(cursor_row)
        row = content['values']
        if row:
            pass  # Not needed now, because you don't set variables like self.name etc.

    def search_data(self):
        query = self.search_var.get().lower()
        filtered = [row for row in mydata if query == row[1].lower()]  # Exact match for Roll
        self.fetchData(filtered)

    def search_by_name(self):
        query = self.name_search_var.get().lower()
        filtered = [row for row in mydata if query in row[2].lower()]  # Search in Name column
        self.fetchData(filtered)

    def search_by_date(self):
        selected_date = self.date_search.get_date().strftime('%d/%m/%Y')
        filtered = [row for row in mydata if row[5] == selected_date]
        self.fetchData(filtered)

    def go_back(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
