from tkinter.ttk import *
from tkinter import *
import tkinter as tkk
from tkinter import font, ttk
from Design import Design

from Attendance import Attendance
from Report import Report
from AddStudent import AddStudent
from AddLecture import AddLecture
from StudentsList import StudentsList
from LecturesList import LecturesList


class AppGUI(tkk.Tk):
    def __init__(self):
        tkk.Tk.__init__(self)
        #  Assigning Variables
        self.menu_bg = '#1E212D'
        self.title_bg = '#DDDDDD'
        self.frame_bg = '#EEEEEE'

        #  Main Window Configuration
        self.title("Auto Attendance System")
        self.state('zoomed')
        self.geometry("1024x668")
        self.configure(bg='#EEEEEE')

        #  Menu Buttons Icons
        self.logo = PhotoImage(file='./Icons/logo.png')
        self.icon_home = PhotoImage(file='./Icons/home.png')
        self.icon_report = PhotoImage(file='./Icons/report.png')
        self.icon_add_student = PhotoImage(file='./Icons/add_student.png')
        self.icon_add_lecture = PhotoImage(file='./Icons/add_lecture.png')
        self.icon_students_list = PhotoImage(file='./Icons/students_list.png')
        self.icon_lectures_list = PhotoImage(file='./Icons/lectures_list.png')

        #  Configure Grid Layout
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        #  Title Frame
        frm_title = Frame(self, bg=self.title_bg)
        frm_title.grid(row=0, column=1, sticky=EW)

        #  Title Text
        lbl_font = font.Font(family='Bahnschrift', size=20, weight='bold')
        self.lbl_title = Label(frm_title, text='Auto Attendance System', bg=self.title_bg, fg='#1E212D', font=lbl_font)
        self.lbl_title.pack(side=LEFT, ipady=20, ipadx=20)

        # Menu Frame
        frm_menu = Frame(self, bg=self.menu_bg)
        frm_menu.grid(row=0, column=0, rowspan=2, sticky=NS)

        #  Call Buttons
        self.menu_buttons(frm_menu)

        #  Call Home Frame
        Attendance(self)

    def menu_buttons(self, menu):
        lbl_logo = Label(menu, image=self.logo, bg=self.menu_bg)
        lbl_logo.pack(side=TOP, fill=X)

        #  Menu Buttons
        btn_home = Button(menu, image=self.icon_home, text=' Home', command=lambda: self.show_frame(Attendance))
        Design.menu_custom_button(btn_home)
        btn_home.pack(side=TOP, fill=X, ipady=2.5)
        btn_home.bind('<Enter>', Design.button_hover)
        btn_home.bind('<Leave>', Design.button_leave)

        btn_report = Button(menu, image=self.icon_report, text=' Attendance', command=lambda: self.show_frame(Report))
        Design.menu_custom_button(btn_report)
        btn_report.pack(side=TOP, fill=X, ipady=2.5)
        btn_report.bind('<Enter>', Design.button_hover)
        btn_report.bind('<Leave>', Design.button_leave)

        btn_add_student = Button(menu, image=self.icon_add_student, text=' Add Student', command=lambda: self.show_frame(AddStudent))
        Design.menu_custom_button(btn_add_student)
        btn_add_student.pack(side=TOP, fill=X, ipady=2.5)
        btn_add_student.bind('<Enter>', Design.button_hover)
        btn_add_student.bind('<Leave>', Design.button_leave)

        btn_add_lecture = Button(menu, image=self.icon_add_lecture, text=' Add Lecture', command=lambda: self.show_frame(AddLecture))
        Design.menu_custom_button(btn_add_lecture)
        btn_add_lecture.pack(side=TOP, fill=X, ipady=2.5)
        btn_add_lecture.bind('<Enter>', Design.button_hover)
        btn_add_lecture.bind('<Leave>', Design.button_leave)

        btn_students_list = Button(menu, image=self.icon_students_list, text=' Students List', command=lambda: self.show_frame(StudentsList))
        Design.menu_custom_button(btn_students_list)
        btn_students_list.pack(side=TOP, fill=X, ipady=2.5)
        btn_students_list.bind('<Enter>', Design.button_hover)
        btn_students_list.bind('<Leave>', Design.button_leave)

        btn_lectures_list = Button(menu, image=self.icon_lectures_list, text=' Lectures List', command=lambda: self.show_frame(LecturesList))
        Design.menu_custom_button(btn_lectures_list)
        btn_lectures_list.pack(side=TOP, fill=X, ipady=2.5)
        btn_lectures_list.bind('<Enter>', Design.button_hover)
        btn_lectures_list.bind('<Leave>', Design.button_leave)

        #  Separator
        separator = ttk.Separator(menu, orient='horizontal')
        separator.pack(fill=X, padx=5)

    def show_frame(self, frame):
        if frame is Report:
            AddStudent(self).destroy()
            AddLecture(self).destroy()
            StudentsList(self).destroy()
            LecturesList(self).destroy()

            self.lbl_title.configure(text='Attendance Report')
            Report(self)

        elif frame is AddStudent:
            Report(self).destroy()
            AddLecture(self).destroy()
            StudentsList(self).destroy()
            LecturesList(self).destroy()

            self.lbl_title.configure(text='Student Registration')
            AddStudent(self)

        elif frame is AddLecture:
            Report(self).destroy()
            AddStudent(self).destroy()
            StudentsList(self).destroy()
            LecturesList(self).destroy()

            self.lbl_title.configure(text='Add Lecture')
            AddLecture(self)

        elif frame is StudentsList:
            Report(self).destroy()
            AddStudent(self).destroy()
            AddLecture(self).destroy()
            LecturesList(self).destroy()

            self.lbl_title.configure(text='Students Information')
            StudentsList(self)

        elif frame is LecturesList:
            Report(self).destroy()
            AddStudent(self).destroy()
            AddLecture(self).destroy()
            StudentsList(self).destroy()

            self.lbl_title.configure(text='Lectures Information')
            LecturesList(self)

        else:
            Report(self).destroy()
            AddStudent(self).destroy()
            AddLecture(self).destroy()
            StudentsList(self).destroy()
            LecturesList(self).destroy()

            self.lbl_title.configure(text='Auto Attendance System')
            Attendance(self).tkraise()


if __name__ == '__main__':
    app = AppGUI()
    app.mainloop()
