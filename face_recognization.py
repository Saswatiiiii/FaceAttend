from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector
import cv2
import os
import numpy as np


class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")

        # Fullscreen setup
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Title Label
        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"),
                          bg="#162936", fg="white")
        title_lbl.place(x=0, y=0, width=screen_width, height=45)

        # Center Image
        img_center = Image.open(r"c:\Users\Saswati\Downloads\face_recog.jpg")
        img_center = img_center.resize((screen_width, screen_height - 45), Image.Resampling.LANCZOS)
        self.photoimg_center = ImageTk.PhotoImage(img_center)

        img_label = Label(self.root, image=self.photoimg_center)
        img_label.place(x=0, y=45, width=screen_width, height=screen_height - 45)

        # Face Recognition Button
        b1 = Button(self.root, background="#000117", foreground="white", font=("times new roman", 16, "bold"),
                    text="Face Recognition", cursor="hand2", command=self.face_recog)
        b1.place(x=screen_width // 2 - 100, y=screen_height - 100, width=200, height=40)

        # Exit Button
        exit_btn = Button(self.root, text="Exit", font=("times new roman", 16, "bold"),
                          bg="red", fg="white", cursor="hand2", command=self.root.destroy)
        exit_btn.place(x=screen_width - 150, y=screen_height - 100, width=120, height=40)

    # ====================== Attendance ======================
    def mark_attendance(self, std_id, roll, name, dept):
        now = datetime.now()
        today_date = now.strftime("%d/%m/%Y")

        attendance_exists = False

        # Check if attendance for today already exists
        with open("attendance.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()

            for line in myDataList:
                entry = line.strip().split(",")
                if len(entry) >= 7:
                    recorded_id, _, _, _, _, recorded_date, _ = entry
                    if recorded_id == std_id and recorded_date == today_date:
                        attendance_exists = True
                        break

        if attendance_exists:
            messagebox.showinfo(
                "Attendance Info",
                f"Attendance for {name} (ID: {std_id}) is already marked for today ({today_date})."
            )
            cv2.destroyAllWindows()
            self.root.destroy()
            return False

        # If no attendance exists, mark it
        dtString = now.strftime("%H:%M:%S")
        with open("attendance.csv", "a", newline="\n") as f:
            f.writelines(f"{std_id},{roll},{name},{dept},{dtString},{today_date},Present\n")

        messagebox.showinfo(
            "Attendance Marked",
            f"Attendance for {name} (ID: {std_id}) marked successfully on {today_date}."
        )
        return True

    # ====================== Face Recognition Function ======================
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbours, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor=scaleFactor, minNeighbors=minNeighbours)

            conn = mysql.connector.connect(host="localhost", username="root", password="saswati2006", database="face_recognizer")
            my_cursor = conn.cursor()

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                my_cursor.execute("SELECT Student_id, Name, Roll, Department FROM student WHERE Student_id=%s", (id,))
                result = my_cursor.fetchone()

                if result:
                    std_id, name, roll, dept = result
                else:
                    std_id, name, roll, dept = "Unknown", "Unknown", "Unknown", "Unknown"

                if confidence > 77:
                    # Display info
                    cv2.putText(img, f"ID: {std_id}", (x, y - 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(img, f"Roll: {roll}", (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(img, f"Name: {name}", (x, y - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(img, f"Dept: {dept}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(img, f"Confidence: {confidence}%", (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 215, 255), 2)

                    if self.mark_attendance(std_id, roll, name, dept) is False:
                        conn.close()
                        return False
                    else:
                        conn.close()
                        return False  # Stop immediately after one attendance
                else:
                    cv2.putText(img, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            conn.close()
            return True

        def recognize(img, clf, faceCascade):
            return draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)
        cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Face Recognition", 900, 650)

        while True:
            ret, img = video_cap.read()
            if not ret:
                break

            # Recognize faces
            if recognize(img, clf, faceCascade) is False:
                break  # Immediately break after successful attendance

            cv2.putText(img, "Scanning...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 255, 255), 2)

            cv2.imshow("Face Recognition", img)

            if cv2.waitKey(1) & 0xFF == 13:  # ENTER (optional)
                break

        video_cap.release()
        cv2.destroyAllWindows()
        


if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognition(root)
    root.mainloop()
