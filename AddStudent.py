import os
from tkinter import *
import tkinter as tkk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from Sql import Queries
from Design import Design


class AddStudent(tkk.Frame):
    def __init__(self, parent):
        tkk.Frame.__init__(self, parent)

        self.txt_color = '#1E212D'
        self.frame_bg = '#EEEEEE'
        self.fg_frame_bg = '#DDDDDD'

        self.grid(row=1, column=1, sticky=NSEW)
        self.configure(bg=self.frame_bg)

        #  Create SQL Queries Class Instance
        self.sql = Queries()

        # Student Information Frame
        self.frm_add_student = Frame(self, bg=self.fg_frame_bg)
        self.frm_add_student.pack(side=TOP, pady=50)

        #  Student Name
        self.lbl_Student_Name = Label(self.frm_add_student, text='Student Name', bg=self.fg_frame_bg, fg=self.txt_color)
        self.lbl_Student_Name.grid(row=0, column=0, sticky=W, padx=(20, 5), pady=(20, 5))

        self.name_text = StringVar()
        self.student_name = Entry(self.frm_add_student, textvariable=self.name_text, bg=self.frame_bg, fg=self.txt_color, relief=FLAT)
        self.student_name.grid(row=0, column=1, columnspan=3, sticky=EW, padx=(5, 20), pady=(20, 5))

        #  Student Roll No.
        self.lbl_Student_roll_no = Label(self.frm_add_student, text='Student Roll No.', bg=self.fg_frame_bg, fg=self.txt_color)
        self.lbl_Student_roll_no.grid(row=1, column=0, sticky=W, padx=(20, 5), pady=5)

        self.roll_no_text = StringVar()
        self.student_roll_no = Entry(self.frm_add_student, textvariable=self.roll_no_text, bg=self.frame_bg, fg=self.txt_color, relief=FLAT)
        self.student_roll_no.grid(row=1, column=1, sticky=W, padx=(5, 20), pady=5)

        #  Upload Student Image
        self.lbl_upload_img = Label(self.frm_add_student, text='Upload Image', bg=self.fg_frame_bg, fg=self.txt_color)
        self.lbl_upload_img.grid(row=2, column=0, sticky=W, padx=(20, 5), pady=5)

        self.btn_upload_img = Button(self.frm_add_student, text='Upload Image', command=lambda: self.upload_img())
        self.btn_upload_img.configure(bg='#1E212D', fg='#FFFFFF', activebackground='#EE4141',
                                      activeforeground='#FFFFFF', bd=0)
        self.btn_upload_img.grid(row=2, column=1, columnspan=2, sticky=EW, padx=(5, 20), pady=5)
        self.btn_upload_img.bind('<Enter>', Design.button_hover)
        self.btn_upload_img.bind('<Leave>', Design.button_leave)

        #  Show Image
        self.lbl_show_img = Label(self.frm_add_student, text='Image Preview', height=20, fg=self.txt_color)
        self.lbl_show_img.grid(row=3, column=0, columnspan=3, sticky=EW, padx=20, pady=5)

        #  Save Button
        self.btn_save = Button(self.frm_add_student, text='Save', command=lambda: self.add())
        self.btn_save.grid(row=4, column=2, sticky=E, padx=(5, 20), pady=20)
        Design.custom_button(self.btn_save)
        self.btn_save.bind('<Enter>', Design.button_hover)
        self.btn_save.bind('<Leave>', Design.button_leave)

        #  Reset Button
        self.btn_reset = Button(self.frm_add_student, text='Reset', command=lambda: self.reset())
        self.btn_reset.grid(row=4, column=1, sticky=E, padx=5, pady=20)
        Design.custom_button(self.btn_reset)
        self.btn_reset.bind('<Enter>', Design.button_hover)
        self.btn_reset.bind('<Leave>', Design.button_leave)

    #  Upload Image Code
    def upload_img(self):
        #  Reset Image before Select
        self.lbl_show_img.destroy()
        self.lbl_show_img = Label(self.frm_add_student, text='Image Preview', height=20, fg=self.txt_color)
        self.lbl_show_img.grid(row=3, column=0, columnspan=3, sticky=EW, padx=20, pady=5)

        try:
            self.filename = filedialog.askopenfilename(initialdir="/", title="Select an Image", filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
            self.img = Image.open(self.filename)
            self.img.thumbnail((300, 300))
            self.image = ImageTk.PhotoImage(self.img)
            self.lbl_show_img.configure(image=self.image, height=300)

        except AttributeError as e:
            messagebox.showinfo('Information', 'You are not select an image.')
            print(e)

    #  Create Table
    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS Students (
                                StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Name TEXT NOT NULL,
                                Roll_No INTEGER NOT NULL UNIQUE);"""
        #  Execute Command
        self.sql.create_table(query)

    def insert(self):
        #  Create Instance to Store Input Data
        student_name = self.name_text.get().title()
        student_roll = self.roll_no_text.get()

        #  Check Roll No. Exists
        query = f"SELECT Roll_No FROM Students WHERE Roll_No = {student_roll}"
        row = self.sql.select_one(query)
        if row is not None:
            messagebox.showinfo("Message", "This Roll No. already exist.")

        elif os.path.isfile('./imgAttendance/'+student_name+'.jpg'):
            messagebox.showinfo("Message", "An image already exist.")

        elif self.filename == '':
            messagebox.showinfo('Information', 'Select an image.')

        else:
            #  Insert Value into Table
            query = f"""INSERT INTO Students(Name, Roll_No) VALUES('{student_name}', {student_roll})"""
            self.sql.insert(query)

            #  Save Image to Local Directory
            image = Image.open(self.filename)
            image.save('./imgAttendance/'+student_name+'.jpg')

    #  Add Student Information
    def add(self):
        try:
            if self.name_text.get() == '' and self.roll_no_text.get() == '':
                messagebox.showwarning("Something went wrong", "Empty filed not allowed!")
            else:
                self.create_table()
                self.insert()
                self.reset()
        except AttributeError:
            messagebox.showwarning("Something went wrong", "Empty filed not allowed!")

    def reset(self):
        self.student_name.delete(0, END)
        self.student_name.focus()
        self.student_roll_no.delete(0, END)
        self.lbl_show_img.destroy()
        self.lbl_show_img = Label(self.frm_add_student, text='Image Preview', height=20, fg=self.txt_color)
        self.lbl_show_img.grid(row=3, column=0, columnspan=3, sticky=EW, padx=20, pady=5)
