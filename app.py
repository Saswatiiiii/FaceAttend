import tkinter as tk
import sys
import os
from PIL import Image, ImageTk
from student import Student_Management_System
from admin_login import open_admin_login
from face_recognization import FaceRecognition
from attendance import Attendance

# Exit function
def go_exit():
    root.destroy()

# Student system


# Attendance window
def attendance_window():
    attend_window = tk.Toplevel(root)
    attend_window.attributes('-fullscreen', True)
    attend_window.title("Attendance")

    screen_w = attend_window.winfo_screenwidth()
    screen_h = attend_window.winfo_screenheight()

    canvas = tk.Canvas(attend_window, width=screen_w, height=screen_h, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_rectangle(0, 0, screen_w, screen_h, fill="#f0f4f8", outline="")

    frame = tk.Frame(attend_window, bg="#ffffff", bd=3, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Attendance Panel", font=("Helvetica", 38, "bold"),
             bg="#ffffff", fg="#2c3e50").pack(pady=40)

    btn_font = ("Helvetica", 22, "bold")

    tk.Button(frame, text="📸  Take Attendance", font=btn_font, width=25, height=2,
              bg="#0066cc", fg="white", activebackground="#3385ff", activeforeground="white",
              relief="flat", cursor="hand2",
              command=lambda: FaceRecognition(tk.Toplevel(attend_window))).pack(pady=30)

    tk.Button(frame, text="📑  Show Attendance", font=btn_font, width=25, height=2,
              bg="#0066cc", fg="white", activebackground="#3385ff", activeforeground="white",
              relief="flat", cursor="hand2",
              command=lambda: open_attendance_table()).pack(pady=30)

    tk.Button(attend_window, text="⬅️ Back", font=("Helvetica", 18, "bold"), width=14, height=1,
              bg="#555555", fg="white", activebackground="#333333", activeforeground="white",
              relief="flat", cursor="hand2",
              command=attend_window.destroy).place(relx=0.5, rely=0.9, anchor="center")
    

def student_registration():
    reg_window = tk.Toplevel(root)
    reg_window.attributes('-fullscreen', True)
    reg_window.title("Student Registration")

    screen_w = reg_window.winfo_screenwidth()
    screen_h = reg_window.winfo_screenheight()

    # Background Canvas
    canvas = tk.Canvas(reg_window, width=screen_w, height=screen_h, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Background gradient-like design
    canvas.create_rectangle(0, 0, screen_w, screen_h, fill="#f0f4f8", outline="")
    canvas.create_rectangle(0, 0, screen_w, 180, fill="#003366", outline="")

    # Header Text
    canvas.create_text(screen_w // 2, 70, text="Student Portal",
                       font=("Helvetica", 42, "bold"), fill="white")

    # Frame to hold content (card style)
    content_frame = tk.Frame(reg_window, bg="white", bd=2, relief="ridge")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Welcome Label
    tk.Label(content_frame, text="Welcome Students!", font=("Helvetica", 32, "bold"),
             bg="white", fg="#003366").pack(pady=40)

    btn_font = ("Helvetica", 20, "bold")

    # Helper function for modern buttons
    def create_button(parent, text, command, color):
        return tk.Button(parent, text=text, font=btn_font,
                         width=25, height=2, bg=color, fg="white",
                         activebackground="#005b99", activeforeground="white",
                         bd=0, relief="flat", cursor="hand2",
                         highlightthickness=0, command=command)

    # Buttons
    create_button(content_frame, "First Time Registration", open_student_system, "#007acc").pack(pady=25)
    create_button(content_frame, "Attendance", attendance_window, "#007acc").pack(pady=25)

    # Back button
    tk.Button(reg_window, text="Back", font=("Helvetica", 16, "bold"),
              width=12, height=1, bg="#d32f2f", fg="white",
              activebackground="#9a0007", bd=0, relief="flat",
              cursor="hand2", command=reg_window.destroy).place(relx=0.5, rely=0.9, anchor="center")


# Show attendance table
def open_attendance_table():
    attendance_window = tk.Toplevel(root)
    Attendance(attendance_window)

def open_student_system():
    student_window = tk.Toplevel(root)
    Student_Management_System(student_window)    

# -------- Main Window Starts Here --------
root = tk.Tk()
root.title("Student Management System")
root.attributes('-fullscreen', True)

# Set app icon if available
icon_path = os.path.join(os.path.dirname(sys.argv[0]), "app_icon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
half_height = screen_height // 2

# Background image
top_img_path = r"c:\Users\Saswati\Downloads\InShot_20250103_200118897.jpg"
top_img = Image.open(top_img_path).resize((screen_width, half_height), Image.Resampling.LANCZOS)
top_bg = ImageTk.PhotoImage(top_img)

canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=top_bg, anchor="nw")
canvas.create_rectangle(0, half_height, screen_width, screen_height, fill="lightblue", outline="lightblue")

# Main button frame
button_frame = tk.Frame(root, bg='lightblue')
button_frame.place(relx=0.5, rely=0.7, anchor="center")
button_font = ("Helvetica", 18, "bold")

tk.Button(button_frame, text="Students", command=student_registration,
          font=button_font, width=20, height=2).grid(row=0, column=0, padx=30)

tk.Button(button_frame, text="Admin", command=lambda: open_admin_login(root),
          font=button_font, width=20, height=2).grid(row=0, column=1, padx=30)

tk.Button(root, text="Exit", command=go_exit,
          font=("Helvetica", 14), width=10).place(relx=0.5, rely=0.95, anchor="center")

root.mainloop()
