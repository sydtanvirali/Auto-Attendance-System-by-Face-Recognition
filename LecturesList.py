import tkinter as tkk
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import *

from Design import Design
from Sql import Queries


class LecturesList(tkk.Frame):
    def __init__(self, parent):
        tkk.Frame.__init__(self, parent)

        self.frame_bg = '#EEEEEE'
        self.fg_frame_bg = '#DDDDDD'

        self.grid(row=1, column=1, sticky=NSEW)
        self.configure(bg=self.frame_bg)

        #  Create SQL Queries Class Instance
        self.sql = Queries()

        #  Frame for TreeView
        self.frm_tree = Frame(self, bg=self.fg_frame_bg)
        self.frm_tree.pack(side=TOP, fill=Y, expand=True, padx=50, pady=50)

        #  Grid Configuration
        self.frm_tree.columnconfigure(0, weight=1)
        self.frm_tree.rowconfigure(0, weight=1)

        self.frm_table = Frame(self.frm_tree)
        self.frm_table.grid(row=0, column=0, sticky=NS, padx=20, pady=20)

        self.scroll_bar_x = Scrollbar(self.frm_table, orient=HORIZONTAL)
        self.scroll_bar_y = Scrollbar(self.frm_table, orient=VERTICAL)

        self.table_tree = Treeview(self.frm_table, columns=('Subject', 'Teacher Name'),
                                   selectmode='extended', yscrollcommand=self.scroll_bar_y.set,
                                   xscrollcommand=self.scroll_bar_x.set)
        self.scroll_bar_y.config(command=self.table_tree.yview)
        self.scroll_bar_y.pack(side=RIGHT, fill=Y)

        self.scroll_bar_x.config(command=self.table_tree.xview)
        self.scroll_bar_x.pack(side=BOTTOM, fill=X)

        self.table_tree.heading('Subject', text='Subject', anchor=CENTER)
        self.table_tree.heading('Teacher Name', text='Teacher Name', anchor=CENTER)

        self.table_tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.table_tree.column('#1', stretch=NO, minwidth=0, width=250)
        self.table_tree.column('#2', stretch=NO, minwidth=0, width=250)
        self.table_tree.pack(side=TOP, fill=Y, expand=True)

        #  Delete Button
        self.btn_delete = Button(self.frm_tree, text='Delete', command=lambda: self.delete())
        self.btn_delete.grid(row=1, column=0, sticky=E, padx=20, pady=(0, 20))
        Design.custom_button(self.btn_delete)
        self.btn_delete.bind('<Enter>', Design.button_hover)
        self.btn_delete.bind('<Leave>', Design.button_leave)

        self.show_list()

    #  Fetch All Records From Table
    def show_list(self):
        query = f"SELECT Lecture, Teacher FROM Lectures ORDER BY Lecture ASC"
        records = self.sql.select_all(query)
        self.table_tree.delete(*self.table_tree.get_children())
        for line in records:
            row = line
            self.table_tree.insert("", END, values=row)

    #  Delete Item
    def delete(self):
        item = len(self.table_tree.selection())
        if item == 0:
            messagebox.showinfo("Message", "Select a record.")
        else:
            response = messagebox.askquestion("Delete Record", "Are you sure? You wand to delete Record?")
            if response == 'yes':
                for selected_item in self.table_tree.selection():
                    item = self.table_tree.item(selected_item)
                    subject = item['values'][0]

                    #  Delete Record
                    query = f"""DELETE FROM Lectures WHERE Lecture = '{subject}'"""
                    self.sql.delete(query)

                    #  Remove Row From Tree
                    for item in self.table_tree.selection():
                        self.table_tree.delete(item)