from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
from datetime import datetime
import face_recognition
from Sql import Queries
import numpy as np
import tkinter as tkk
import cv2
import os
from Design import Design


class Attendance(tkk.Frame):
    def __init__(self, parent):
        tkk.Frame.__init__(self, parent)

        self.frame_bg = '#EEEEEE'
        self.txt_color = '#1E212D'

        self.grid(row=1, column=1, sticky=NSEW)
        self.configure(bg=self.frame_bg)

        #  Create SQL Queries Class Instance
        self.sql = Queries()

        #  Fetch Subjects Details from Lecture Table
        query = f"SELECT Lecture FROM Lectures"
        my_list = self.sql.select_all(query)
        subject_list = []
        for line in my_list:
            subject_list.append(line[0])

        #  Select Lecture
        self.cmb_lecture_var = StringVar()
        self.cmb_lecture = Combobox(self, value=subject_list, state='readonly', textvariable=self.cmb_lecture_var, width=30)
        self.cmb_lecture.pack(side=TOP, padx=10, pady=(10, 0))
        self.cmb_lecture.set('Select Lecture...')

        #  Video Play on Label
        self.lbl_video = Label(self, text='Select lecture before click on Start button to launch Attendance.',
                               bg=self.frame_bg, fg=self.txt_color)
        self.lbl_video.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=(10, 0))

        #  Frame for Buttons
        self.frm_btn = Frame(self, bg=self.frame_bg)
        self.frm_btn.pack(side=TOP, padx=20, pady=20)

        #  Buttons
        self.btn_start = Button(self.frm_btn, text='START', command=self.launch_camera)
        self.btn_start.grid(row=0, column=0, padx=10)
        Design.custom_button(self.btn_start)
        self.btn_start.bind('<Enter>', Design.button_hover)
        self.btn_start.bind('<Leave>', Design.button_leave)

        self.btn_stop = Button(self.frm_btn, text='STOP', command=self.stop_camera)
        self.btn_stop.grid(row=0, column=1, padx=10)
        Design.custom_button(self.btn_stop)
        self.btn_stop.bind('<Enter>', Design.button_hover)
        self.btn_stop.bind('<Leave>', Design.button_leave)

    def launch_camera(self):
        if self.cmb_lecture_var.get() == 'Select Lecture...':
            messagebox.showinfo('Message', 'Before starting an Attendance. Select a Lecture.')
            self.cmb_lecture.focus()
        else:
            self.cmb_lecture.configure(state='disabled')
            self.btn_start.configure(state='disabled')
            #  Importing Images
            path = 'imgAttendance'
            images = []  # LIST CONTAINING ALL THE IMAGES
            images_name = []  # LIST CONTAINING ALL THE CORRESPONDING CLASS Names
            my_list = os.listdir(path)
            print("Total Students Detected:", len(my_list))
            for x, cl in enumerate(my_list):
                cur_img = cv2.imread(f'{path}/{cl}')
                images.append(cur_img)
                images_name.append(os.path.splitext(cl)[0])

            encode_list_known = self.find_encodings(images)
            print('Encodings Complete')

            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            #  url = "https://192.168.158.123:8080/video"
            #  self.cap.open(url)

            #  Webcam Image
            while True:
                success, img = self.cap.read()
                img = cv2.flip(img, 1)
                img_s = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                #  Webcam Encodings
                faces_cur_frame = face_recognition.face_locations(img_s)
                encodes_cur_frame = face_recognition.face_encodings(img_s, faces_cur_frame)

                #  Find Matches
                for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
                    matches = face_recognition.compare_faces(encode_list_known, encodeFace)
                    face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
                    match_index = np.argmin(face_dis)

                    if matches[match_index]:
                        name = images_name[match_index]
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                        self.mark_attendance(name)
                    else:
                        name = 'Unknown Person'
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(img))
                self.lbl_video.configure(image=img, text='')
                self.update()

    def stop_camera(self):
        try:
            if self.cap.isOpened():
                response = messagebox.askquestion("Stop Attendance", "Are you sure? You want to stop Attendance?")
                if response == 'yes':
                    self.cap.release()
                    self.lbl_video.configure(text='Select lecture before click on Start button to launch Attendance.',
                                         compound=CENTER)
                    self.cmb_lecture.configure(state='readonly')
                    self.cmb_lecture.set('Select Lecture...')
                    self.btn_start.configure(state='normal')

        except (AttributeError, cv2.error) as e:
            print(e)

    #  Compute Encodings
    @staticmethod
    def find_encodings(images):
        encode_list = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
        return encode_list

    #  Making Attendance
    def mark_attendance(self, name):
        now = datetime.now()
        dtd_string = now.strftime("%d-%b-%Y")
        dtt_string = now.strftime("%I:%M:%S %p")

        #  Create Table
        query = f"""CREATE TABLE IF NOT EXISTS Attendance (
                        AttendanceID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Roll_No INTEGER NOT NULL,
                        Name INTEGER NOT NULL,
                        Lecture INTEGER NOT NULL,
                        Time TEXT NOT NULL,
                        Date TEXT NOT NULL,
                        FOREIGN KEY (Name) REFERENCES Students (StudentID) ON DELETE CASCADE,
                        FOREIGN KEY (Lecture) REFERENCES Lectures (LectureID) ON DELETE CASCADE);"""
        self.sql.create_table(query)

        #  Fetch All Names from Table to Avoid Duplication
        query = f"""SELECT S.Name, L.Lecture, A.Date FROM Attendance A 
                                                JOIN Students S ON A.Name = S.StudentID 
                                                JOIN Lectures L ON A.Lecture = L.LectureID"""
        my_data_list = self.sql.select_all(query)

        #  Fetch Roll Number to Save
        query = f"""SELECT Roll_No FROM Students WHERE Name = '{name}' """
        roll_no = self.sql.select_one(query)[0]

        #  Get StudentID by Name
        query = f"SELECT StudentID FROM Students WHERE Name = '{name}'"
        student_id = self.sql.select_one(query)[0]

        #  Get LectureID by Name
        lecture = self.cmb_lecture_var.get()
        query = f"SELECT LectureID FROM Lectures WHERE Lecture = '{lecture}'"
        lecture_id = self.sql.select_one(query)[0]

        #  Insert Record After Matching Face
        row = (name, lecture, dtd_string)
        if row not in my_data_list:
            query = f"""INSERT INTO Attendance (Roll_No, Name, Lecture, Time, Date) 
                                VALUES({roll_no}, {student_id}, {lecture_id}, '{dtt_string}', '{dtd_string}')"""
            self.sql.insert_wsm(query)

