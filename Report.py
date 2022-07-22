from tkinter.ttk import *
from tkinter import *
import tkinter as tkk
from tkinter import messagebox
from PIL import ImageTk, Image
from Sql import Queries
from Design import Design


class Report(tkk.Frame):
    def __init__(self, parent):
        tkk.Frame.__init__(self, parent)

        self.frame_bg = '#EEEEEE'
        self.fg_frame_bg = '#DDDDDD'

        self.grid(row=1, column=1, sticky=NSEW)
        self.configure(bg=self.frame_bg)

        #  Create SQL Queries Class Instance
        self.sql = Queries()

        #  Frame for Combobox and Button
        self.frm_cmb = Frame(self, bg=self.fg_frame_bg)
        self.frm_cmb.pack(side=TOP, fill=X, padx=50, pady=(50, 0))

        #  Get Date List
        query = f"SELECT DISTINCT Date FROM Attendance ORDER BY Date DESC"
        my_list = self.sql.select_all(query)
        self.date_list = []
        for line in my_list:
            self.date_list.append(line[0])

        #  Date List ComboBox
        self.cmb_list_var = StringVar()
        self.cmb_list = Combobox(self.frm_cmb, values=self.date_list, state='readonly',
                                 textvariable=self.cmb_list_var, width=30)
        self.cmb_list.grid(row=0, column=0, padx=(20, 0), pady=(20, 10))
        self.cmb_list.set('Select Date...')
        self.cmb_list.bind('<<ComboboxSelected>>', self.cmb_select)

        #  Lecture List Combobox
        self.cmb_sub_var = StringVar()
        self.cmb_sub = Combobox(self.frm_cmb, state='readonly',
                                textvariable=self.cmb_sub_var, width=30)
        self.cmb_sub.grid(row=0, column=1, padx=(20, 0), pady=(20, 10))
        self.cmb_sub.set('Select Subject...')

        #  View Button
        self.btn_view = Button(self.frm_cmb, text='View')
        self.btn_view.grid(row=0, column=2, padx=(20, 0), pady=(20, 10))
        Design.custom_button(self.btn_view)
        self.btn_view.bind('<Button-1>', self.clicked)
        self.btn_view.bind('<Enter>', Design.button_hover)
        self.btn_view.bind('<Leave>', Design.button_leave)

        #  Delete Button
        self.btn_delete = Button(self.frm_cmb, text='Delete', command=lambda: self.delete())
        self.btn_delete.grid(row=0, column=3, padx=20, pady=(20, 10))
        Design.custom_button(self.btn_delete)
        self.btn_delete.bind('<Enter>', Design.button_hover)
        self.btn_delete.bind('<Leave>', Design.button_leave)

        #  Frame for TreeView
        self.frm_tree = Frame(self, bg=self.fg_frame_bg)
        self.frm_tree.pack(side=LEFT, fill=BOTH, expand=True, padx=50, pady=(0, 50))

        #  Grid Configuration
        self.frm_tree.columnconfigure(1, weight=1)
        self.frm_tree.rowconfigure(0, weight=1)

        self.frm_table = Frame(self.frm_tree)
        self.frm_table.grid(row=0, column=0, sticky=NS, padx=(20, 10), pady=(10, 20))

        self.scroll_bar_x = Scrollbar(self.frm_table, orient=HORIZONTAL)
        self.scroll_bar_y = Scrollbar(self.frm_table, orient=VERTICAL)

        self.table_tree = Treeview(self.frm_table, columns=('Roll_No', 'Name', 'Lecture', 'Time', 'Date'),
                                   selectmode='extended', yscrollcommand=self.scroll_bar_y.set,
                                   xscrollcommand=self.scroll_bar_x.set)
        self.scroll_bar_y.config(command=self.table_tree.yview)
        self.scroll_bar_y.pack(side=RIGHT, fill=Y)

        self.scroll_bar_x.config(command=self.table_tree.xview)
        self.scroll_bar_x.pack(side=BOTTOM, fill=X)

        self.table_tree.heading('Roll_No', text='Roll_No', anchor=CENTER)
        self.table_tree.heading('Name', text='Name', anchor=CENTER)
        self.table_tree.heading('Lecture', text='Lecture', anchor=CENTER)
        self.table_tree.heading('Time', text='Time', anchor=CENTER)
        self.table_tree.heading('Date', text='Date', anchor=CENTER)

        self.table_tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.table_tree.column('#1', stretch=NO, minwidth=0, width=50, anchor=CENTER)
        self.table_tree.column('#2', stretch=NO, minwidth=0, width=220)
        self.table_tree.column('#3', stretch=NO, minwidth=0, width=150)
        self.table_tree.column('#4', stretch=NO, minwidth=0, width=100, anchor=CENTER)
        self.table_tree.column('#5', stretch=NO, minwidth=0, width=100, anchor=CENTER)
        self.table_tree.pack(side=TOP, fill=Y, expand=True)
        self.table_tree.bind('<Button-1>', self.item_selected)

        self.lbl_img = Label(self.frm_tree, text='Click on Name to Show Image', fg='#1E212D')
        self.lbl_img.grid(row=0, column=1, sticky=NSEW, padx=(10, 20), pady=(10, 20))

    #  Get Lecture List
    def cmb_select(self, event):
        self.select_date = self.cmb_list_var.get()
        query = f"""SELECT DISTINCT L.Lecture FROM Attendance A 
                                                    JOIN Lectures L
                                                    ON A.Lecture = L.LectureID
                                                    WHERE Date = '{self.select_date}' 
                                                    ORDER BY L.Lecture DESC """
        my_list = self.sql.select_all(query)
        self.lecture_list = []
        for line in my_list:
            self.lecture_list.append(line[0])

        #  Set Subject List on Combobox
        self.cmb_sub.set('Select Subject...')
        self.cmb_sub['values'] = self.lecture_list

    #  View Button Event Fire with Clicked Method
    def clicked(self, event):
        if self.cmb_sub_var.get() != 'Select Subject...':
            lecture = self.cmb_sub_var.get()
            date = self.cmb_list_var.get()
            query = f"""SELECT A.Roll_No, S.Name, L.Lecture, A.Time, A.Date FROM Attendance A 
                                                                JOIN Lectures L
                                                                ON A.Lecture = L.LectureID
                                                                JOIN Students S
                                                                ON A.Name = S.StudentID
                                                                WHERE L.Lecture = '{lecture}'
                                                                AND A.Date = '{date}'
                                                                ORDER BY A.Roll_No ASC """

            records = self.sql.select_all(query)
            self.table_tree.delete(*self.table_tree.get_children())
            for line in records:
                row = line
                self.table_tree.insert("", END, values=row)

        elif self.cmb_list_var.get() != 'Select Date...' and self.cmb_sub_var.get() == 'Select Subject...':
            date = self.cmb_list_var.get()
            query = f"""SELECT A.Roll_No, S.Name, L.Lecture, A.Time, A.Date FROM Attendance A 
                                                                JOIN Lectures L
                                                                ON A.Lecture = L.LectureID
                                                                JOIN Students S
                                                                ON A.Name = S.StudentID
                                                                WHERE A.Date = '{date}' 
                                                                ORDER BY A.Roll_No ASC """

            records = self.sql.select_all(query)
            self.table_tree.delete(*self.table_tree.get_children())
            for line in records:
                row = line
                self.table_tree.insert("", END, values=row)

        else:
            messagebox.showinfo('Message', 'Select Date or Subject.')

    #  TreeView Item Selection Event Fire with item_selection Method
    def item_selected(self, event):
        try:
            for selected_item in self.table_tree.selection():
                item = self.table_tree.item(selected_item)
                name = item['values'][1]

                #  Set Image after Clicking Name
                self.img = Image.open('./imgAttendance/' + name + '.jpg')
                self.img.thumbnail((400, 400))
                self.image = ImageTk.PhotoImage(self.img)
                self.lbl_img.configure(image=self.image)

        except (FileNotFoundError, AttributeError):
            self.lbl_img.configure(text='Image Not Found', compound=TOP)
            messagebox.showerror("Error", "Image not found.")

    def delete(self):
        item = len(self.table_tree.selection())
        if item == 0:
            messagebox.showinfo("Message", "Select a record.")
        else:
            response = messagebox.askquestion("Delete Record", "Are you sure? You wand to delete Record?")
            if response == 'yes':
                for selected_item in self.table_tree.selection():
                    item = self.table_tree.item(selected_item)
                    name = item['values'][1]
                    lecture = item['values'][2]
                    date = item['values'][4]

                    query = f"""SELECT StudentID FROM Students WHERE Name = '{name}'"""
                    studentID = self.sql.select_one(query)[0]
                    query = f"""SELECT LectureID FROM Lectures WHERE Lecture = '{lecture}'"""
                    lectureID = self.sql.select_one(query)[0]

                    #  Delete Record
                    query = f"""DELETE FROM Attendance WHERE Name = {studentID} AND Lecture = {lectureID}
                                                                            AND Date = '{date}'"""
                    self.sql.delete(query)

                    #  Remove Row From Tree
                    for item in self.table_tree.selection():
                        self.table_tree.delete(item)

                    self.lbl_img.destroy()
                    self.lbl_img = Label(self.frm_tree, text='Click on Name to Show Image', fg='#1E212D')
                    self.lbl_img.grid(row=0, column=1, sticky=NSEW, padx=(10, 20), pady=(10, 20))


