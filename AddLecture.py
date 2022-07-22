from tkinter import *
import tkinter as tkk
from tkinter import messagebox
from Sql import Queries
from Design import Design


class AddLecture(tkk.Frame):
    def __init__(self, parent):
        tkk.Frame.__init__(self, parent)

        self.txt_color = '#1E212D'
        self.frame_bg = '#EEEEEE'
        self.fg_frame_bg = '#DDDDDD'

        self.grid(row=1, column=1, sticky=NSEW)
        self.configure(bg=self.frame_bg)

        #  Create SQL Queries Class Instance
        self.sql = Queries()

        # Lecture Information Frame
        self.frm_add_lecture = Frame(self, bg=self.fg_frame_bg)
        self.frm_add_lecture.pack(side=TOP, pady=50)

        #  Subject Name
        self.lbl_subject = Label(self.frm_add_lecture, text='Subject Name', bg=self.fg_frame_bg, fg=self.txt_color)
        self.lbl_subject.grid(row=0, column=0, sticky=W, padx=(20, 5), pady=(20, 5))

        self.subject_text = StringVar()
        self.subject_name = Entry(self.frm_add_lecture, textvariable=self.subject_text, bg=self.frame_bg, fg=self.txt_color, relief=FLAT)
        self.subject_name.grid(row=0, column=1, columnspan=3, sticky=EW, padx=(5, 20), pady=(20, 5))

        #  Teacher Name
        self.lbl_teacher_Name = Label(self.frm_add_lecture, text='Teacher Name', bg=self.fg_frame_bg, fg=self.txt_color)
        self.lbl_teacher_Name.grid(row=1, column=0, sticky=W, padx=(20, 5), pady=5)

        self.name_text = StringVar()
        self.teacher_name = Entry(self.frm_add_lecture, textvariable=self.name_text, bg=self.frame_bg, fg=self.txt_color, relief=FLAT)
        self.teacher_name.grid(row=1, column=1, columnspan=3, sticky=EW, padx=(5, 20), pady=5)

        #  Save Button
        self.btn_save = Button(self.frm_add_lecture, text='Save', command=lambda: self.add())
        self.btn_save.grid(row=4, column=2, sticky=E, padx=(5, 20), pady=20)
        Design.custom_button(self.btn_save)
        self.btn_save.bind('<Enter>', Design.button_hover)
        self.btn_save.bind('<Leave>', Design.button_leave)

        #  Reset Button
        self.btn_reset = Button(self.frm_add_lecture, text='Reset', command=lambda: self.reset())
        self.btn_reset.grid(row=4, column=1, sticky=E, padx=5, pady=20)
        Design.custom_button(self.btn_reset)
        self.btn_reset.bind('<Enter>', Design.button_hover)
        self.btn_reset.bind('<Leave>', Design.button_leave)

    #  Create Table
    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS Lectures (
                                        LectureID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        Lecture TEXT NOT NULL UNIQUE,
                                        Teacher TEXT NOT NULL);"""
        #  Execute Command
        self.sql.create_table(query)

    def insert(self):
        #  Create Instance to Store Input Data
        subject_name = self.subject_text.get().title()
        teacher_name = self.name_text.get().title()

        #  Check Subject Name Exists
        query = f"SELECT Lecture FROM Lectures WHERE Lecture = '{subject_name}'"
        row = self.sql.select_one(query)

        if row is not None:
            messagebox.showinfo("Message", "This subject name already exist.")
        else:
            #  Insert Value into Table
            query = f"""INSERT INTO Lectures(Lecture, Teacher) 
                                VALUES('{subject_name}', '{teacher_name}')"""
            #  Execute Command
            self.sql.insert(query)

    #  Add Lecturer Information
    def add(self):
        if self.name_text.get() == '' and self.subject_text.get() == '':
            messagebox.showwarning("Something went wrong", "Empty filed not allowed!")
        else:
            self.create_table()
            self.insert()
            self.reset()

    def reset(self):
        self.subject_name.delete(0, END)
        self.subject_name.focus()
        self.teacher_name.delete(0, END)
