from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Student_Management_System:

    def __init__(self, root):
        self.root = root
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window to fullscreen
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.attributes("-fullscreen", True)

        # Prevent window resizing
        self.root.resizable(False, False)
        
        self.root.title("Student Management System")
        
        # Fullscreen exit using Escape key
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # ==========variables========
        self.var_dep = StringVar()
        self.var_year = StringVar()
        self.var_session = StringVar()
        self.var_sem = StringVar()
        self.var_id = StringVar()
        self.var_name = StringVar()
        self.var_roll = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_radio1 = StringVar()

        # Background image
        img = Image.open(r"c:\Users\Saswati\Downloads\InShot_20250103_200118897.jpg")
        img = img.resize((screen_width, screen_height-130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        bg_img = Label(self.root, image=self.photoimg)
        bg_img.place(x=0, y=130, width=screen_width, height=screen_height-130)

        # Header image
        img = Image.open(r"c:\Users\Saswati\Downloads\InShot_20250219_222820469 (1).jpg")
        img = img.resize((screen_width, 175), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=screen_width, height=175)

        main_frame = Frame(bg_img, bd=2)
        main_frame.place(x=0, y=50, width=screen_width-50, height=600)

        exit_btn = Button(self.root, text="Exit", font=("times new roman", 16, "bold"),
                          bg="red", fg="white", cursor="hand2", command=self.root.destroy)
        exit_btn.place(x=screen_width - 150, y=screen_height - 100, width=120, height=40)

        # Title Label for 'Student Registration' — in the gap
        registration_title = Label(root, text="Student Registration", font=("Arial", 30, "bold"), bg = "blue", fg = "black")
        registration_title.pack(pady=10)
        registration_title.place(relx=0.5, rely=0.25, anchor="center", width=1530, height=50)

        # Left label frame
        Registration_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                text="Student Details", font=("times new roman", 12, "bold"))
        Registration_frame.place(relx=0.52, rely=0.6, anchor="center", width=870, height=555)

        img_Registration = Image.open(r"c:\Users\Saswati\OneDrive\Pictures\happy-students-diplomas-near-campus-260nw-1765367483.jpg")
        img_Registration = img_Registration.resize((screen_width-500, 160), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_Registration)

        f_lbl= Label(Registration_frame, image = self.photoimg_left)
        f_lbl.place(x=5,y=0,width=860,height=160)

        # Current Course Info Frame
        current_course_frame = LabelFrame(Registration_frame, bd=2, bg="white", relief=RIDGE,
                                          text="Current Course Information", font=("times new roman", 12, "bold"))
        current_course_frame.place(x=0, y=160, width=863, height=130)

        # Department
        dep_label = Label(current_course_frame, text="Department", font=("times new roman", 14, "bold"), bg="white")
        dep_label.grid(row=0, column=0, padx=10, sticky=W)

        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep,
                                 font=("times new roman", 14, "bold"), state="readonly", width=20)
        dep_combo["values"] = ("Select Department", "Computer Science and Technology",
                               "Electronics and Tele Communication", "Civil")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Year
        year_label = Label(current_course_frame, text="Year", font=("times new roman", 14, "bold"), bg="white")
        year_label.grid(row=0, column=3, padx=10, sticky=W)

        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year,
                                  font=("times new roman", 14, "bold"), state="readonly", width=20)
        year_combo["values"] = ("Select Year", "First Year", "Second Year", "Third Year")
        year_combo.current(0)
        year_combo.grid(row=0, column=4, padx=2, pady=10, sticky=W)

        # Session
        session_label = Label(current_course_frame, text="Session", font=("times new roman", 14, "bold"), bg="white")
        session_label.grid(row=1, column=0, padx=10, sticky=W)

        session_combo = ttk.Combobox(current_course_frame, textvariable=self.var_session,
                                     font=("times new roman", 14, "bold"), state="readonly", width=20)
        session_combo["values"] = ("Select Session", "2024-25", "2025-26", "2026-27")
        session_combo.current(0)
        session_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # Semester
        semester_label = Label(current_course_frame, text="Semester", font=("times new roman", 14, "bold"), bg="white")
        semester_label.grid(row=1, column=3, padx=10, sticky=W)

        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_sem,
                                      font=("times new roman", 14, "bold"), state="readonly", width=20)
        semester_combo["values"] = ("Select Semester", "Semester-1", "Semester-2", "Semester-3",
                                    "Semester-4", "Semester-5", "Semester-6")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=4, padx=2, pady=10, sticky=W)

        ## Class Student Info
        class_Student_frame = LabelFrame(Registration_frame, bd=2, bg="white", relief=RIDGE,
                                         text="Student Information", font=("times new roman", 13, "bold"))
        class_Student_frame.place(x=0, y=300, width=863, height=268)

        # Student ID
        Label(class_Student_frame, text="*Student ID:", font=("times new roman", 14, "bold"), bg="white", fg = "red").grid(
            row=0, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_Student_frame, width=20, textvariable=self.var_id, font=("times new roman", 14, "bold")).grid(
            row=0, column=1, padx=10, pady=5, sticky=W)

        # Student Name
        Label(class_Student_frame, text="Student Name:", font=("times new roman", 14, "bold"), bg="white").grid(
            row=0, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_Student_frame, width=20, textvariable=self.var_name,
                  font=("times new roman", 14, "bold")).grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Roll No
        Label(class_Student_frame, text="Roll No:", font=("times new roman", 14, "bold"), bg="white").grid(
            row=1, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_Student_frame, width=20, textvariable=self.var_roll,
                  font=("times new roman", 14, "bold")).grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Email ID
        Label(class_Student_frame, text="Email ID:", font=("times new roman", 14, "bold"), bg="white").grid(
            row=1, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_Student_frame, width=20, textvariable=self.var_email,
                  font=("times new roman", 14, "bold")).grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Phone Number
        Label(class_Student_frame, text="Phone Number:", font=("times new roman", 14, "bold"), bg="white").grid(
            row=2, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_Student_frame, width=20, textvariable=self.var_phone,
                  font=("times new roman", 14, "bold")).grid(row=2, column=1, padx=10, pady=5, sticky=W)


        # Radio Buttons
        ttk.Radiobutton(class_Student_frame, variable=self.var_radio1, text="Take Photo Sample",
                        value="Yes", command=self.toggle_take_photo_button).grid(row=3, column=0)
        ttk.Radiobutton(class_Student_frame, variable=self.var_radio1, text="No Photo Sample",
                        value="No", command=self.toggle_take_photo_button).grid(row=3, column=1)

        # Buttons Frame
        btn_frame = Frame(class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=140, width=860, height=36)

        Button(btn_frame, text="Save", command=self.add_data, width=40, font=("times new roman", 13, "bold"),
               bg="black", fg="white").grid(row=0, column=0)

        self.take_photo_btn = Button(btn_frame, command=self.generate_dataset, text="Take Photo Sample", width=46,
                                     font=("times new roman", 13, "bold"), bg="black", fg="white")
        self.take_photo_btn.grid(row=0, column=1)
       # self.take_photo_btn.config(state=DISABLED)



    def toggle_take_photo_button(self):
        if self.var_radio1.get() == "Yes":
            self.take_photo_btn.config(state=NORMAL)
        else:
            self.take_photo_btn.config(state=DISABLED)

    def add_data(self):
         
        if self.var_dep.get()=="Select Department" or self.var_name.get()=="" or self.var_id.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root) 
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="saswati2006",database="face_recognizer")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(

                                                                                                self.var_dep.get(),
                                                                                                self.var_year.get(),
                                                                                                self.var_session.get(),
                                                                                                self.var_sem.get(),
                                                                                                self.var_id.get(),
                                                                                                self.var_name.get(),
                                                                                                self.var_roll.get(),
                                                                                                self.var_email.get(),
                                                                                                self.var_phone.get(),
                                                                                                self.var_radio1.get()

                                                                                      ))
                conn.commit()
                
                conn.close()
                messagebox.showinfo("Success","Student details has been added Successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="saswati2006",database="face_recognizer")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from student")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()  

    

    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="saswati2006", database="face_recognizer")
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student")
                myresult = my_cursor.fetchall()
                id = 0
                for x in myresult:
                    id+=1

                # Use the correct student ID from the input fields
                id = self.var_id.get()

                # Update student data
                my_cursor.execute(
                    "UPDATE student SET Department=%s, Year=%s, Session=%s, Semester=%s, Name=%s, Roll=%s, Email=%s, Phone_no=%s, PhotoSample=%s WHERE Student_id=%s",
                    (
                        self.var_dep.get(),
                        self.var_year.get(),
                        self.var_session.get(),
                        self.var_sem.get(),
                        self.var_name.get(),
                        self.var_roll.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_radio1.get(),
                        self.var_id.get()
                    )
                )

                conn.commit()
                
                conn.close()

                #================== Load predefined face classifier ========================
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                def face_cropped(img):
                    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(grey, 1.3, 5)

                    for (x, y, w, h) in faces:
                        face_cropped = img[y:y+h, x:x+w]
                        return face_cropped
                    return None

                cap = cv2.VideoCapture(0)
                img_id = 0
                while True:
                    ret, my_frame = cap.read()
                    cropped_face = face_cropped(my_frame)

                    if cropped_face is not None:
                        img_id += 1
                        face = cv2.resize(cropped_face, (450, 450))
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                        file_name_path = f"data/user.{id}.{img_id}.jpg"
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                        cv2.imshow("Cropped Face", face)

                    if cv2.waitKey(1) == 13 or img_id == 100:
                        break

                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result", "Generating data sets completed!!!!")

                # ================== Auto Train the Model ==================
                self.train_classifier()

            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    #======================= Train Classifier (Auto-training after capture) =======================
    def train_classifier(self):
        data_dir = "data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L')  # Convert to grayscale
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)

        ids = np.array(ids)

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")

        messagebox.showinfo("Result", "Training completed successfully!", parent=self.root)



if __name__ == "__main__":
    root = Tk()
    obj = Student_Management_System(root)
    root.mainloop()
