import tkinter as tk
from tkinter import messagebox
from student_table import StudentTableWindow  # Import the student table window
import os

def open_admin_login(root):
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")

    # Make the Admin Login window fullscreen
    login_window.attributes('-fullscreen', True)
    login_window.configure(bg="#f0f0f0")
    login_window.grab_set()

    # College Header
    header = tk.Label(login_window, text="Login Portal",
                      font=("Helvetica", 36, "bold"), bg="#003366", fg="white", pady=20)
    header.pack(fill="x")

    # Login Frame (centered box)
    login_frame = tk.Frame(login_window, bg="white", bd=2, relief="groove")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Login Title
    tk.Label(login_frame, text="Admin Login Portal", font=("Helvetica", 28, "bold"), bg="white", fg="#003366").pack(pady=20)

    # Username field
    tk.Label(login_frame, text="Username:", font=("Helvetica", 20), bg="white").pack(pady=5)
    username_entry = tk.Entry(login_frame, font=("Helvetica", 20), width=20)
    username_entry.pack(pady=5)

    # Password field
    tk.Label(login_frame, text="Password:", font=("Helvetica", 20), bg="white").pack(pady=5)
    password_entry = tk.Entry(login_frame, show="*", font=("Helvetica", 20), width=20)
    password_entry.pack(pady=5)

    # Toggle show/hide password
    def toggle_password():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
            toggle_btn.config(text="Hide Password")
        else:
            password_entry.config(show='*')
            toggle_btn.config(text="Show Password")

    toggle_btn = tk.Button(login_frame, text="Show Password", command=toggle_password,
                           font=("Helvetica", 14), bg="#0052cc", fg="white", width=15)
    toggle_btn.pack(pady=10)

    # Admin Dashboard
    def open_dashboard():
        dashboard = tk.Toplevel(root)
        dashboard.title("Admin Dashboard")

        # Make the dashboard fullscreen
        dashboard.attributes('-fullscreen', True)
        dashboard.configure(bg="#f0f0f0")
        dashboard.grab_set()

        # Header
        header = tk.Label(dashboard, text="Admin Dashboard",
                          font=("Helvetica", 36, "bold"), bg="#003366", fg="white", pady=20)
        header.pack(fill="x")

        # Section Frame (card-like box)
        section_frame = tk.Frame(dashboard, bg="white", bd=2, relief="groove")
        section_frame.place(relx=0.5, rely=0.5, anchor="center")

        section_label = tk.Label(section_frame, text="Dashboard Controls", font=("Helvetica", 28, "bold"),
                                 bg="white", fg="#003366")
        section_label.pack(pady=30)

        button_frame = tk.Frame(section_frame, bg="white")
        button_frame.pack(pady=20)

        def open_student_photos():
            os.startfile("data")

        def open_registered_students():
            StudentTableWindow(dashboard)

        def go_back_to_main():
            dashboard.destroy()

        # Styled Buttons
        btn_style = {
            "font": ("Helvetica", 20),
            "width": 20,
            "height": 2,
            "bg": "#0052cc",
            "fg": "white",
            "activebackground": "#003366",
            "activeforeground": "white",
            "bd": 0
        }

        btn_photos = tk.Button(button_frame, text="📸 Student Photos", command=open_student_photos, **btn_style)
        btn_photos.grid(row=0, column=0, padx=30, pady=20)

        btn_registered = tk.Button(button_frame, text="📝 Registered Students", command=open_registered_students, **btn_style)
        btn_registered.grid(row=0, column=1, padx=30, pady=20)

        btn_back = tk.Button(section_frame, text="⏪ Back", command=go_back_to_main,
                             font=("Helvetica", 18), width=15, bg="gray", fg="white",
                             activebackground="#333", activeforeground="white", bd=0)
        btn_back.pack(pady=40)

        

        # ESC key to exit fullscreen
        dashboard.bind("<Escape>", lambda event: dashboard.destroy())

    # Login validation
    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            login_window.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Try again.")
            

    # Login button
    tk.Button(login_frame, text="Login", command=verify_login,
              font=("Helvetica", 20), bg="#28a745", fg="white", width=20).pack(pady=20)

    # ESC key to exit fullscreen
    login_window.bind("<Escape>", lambda event: login_window.destroy())

# Main window setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")

    # Set main window size (normal window)
    root.geometry("800x600")

    tk.Button(root, text="Admin", command=lambda: open_admin_login(root),
              font=("Helvetica", 24), width=20, height=2, bg="#003366", fg="white").pack(pady=100)

    tk.Button(root, text="Exit", command=root.quit, font=("Helvetica", 18), width=10, bg="gray", fg="white").pack(pady=20)

    root.mainloop()

