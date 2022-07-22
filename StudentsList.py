from tkinter import messagebox
from tkinter.ttk import *
import tkinter as tkk
from tkinter import *
from PIL import ImageTk, Image

from Design import Design
from Sql import Queries


class StudentsList(tkk.Frame):
    def __init__(self, parent):
        tkk.Frame.__init__(self, parent)

        self.txt_color = '#1E212D'
        self.frame_bg = '#EEEEEE'
        self.fg_frame_bg = '#DDDDDD'

        self.grid(row=1, column=1, sticky=NSEW)
        self.configure(bg=self.frame_bg)

        #  Create SQL Queries Class Instance
        self.sql = Queries()

        #  Frame for Tree view and Image, Button
        self.frm_tree = Frame(self, bg=self.fg_frame_bg)
        self.frm_tree.pack(side=TOP, fill=Y, expand=True, padx=50, pady=50)

        #  Grid Configuration
        self.frm_tree.columnconfigure(1, weight=1)
        self.frm_tree.rowconfigure(0, weight=1)

        self.frm_table = Frame(self.frm_tree, bg=self.fg_frame_bg)
        self.frm_table.grid(row=0, column=0, sticky=NS, padx=(20, 10), pady=20)

        self.scroll_bar_x = Scrollbar(self.frm_table, orient=HORIZONTAL)
        self.scroll_bar_y = Scrollbar(self.frm_table, orient=VERTICAL)

        self.table_tree = Treeview(self.frm_table, columns=('Roll_No', 'Student Name'),
                                   selectmode='extended', yscrollcommand=self.scroll_bar_y.set,
                                   xscrollcommand=self.scroll_bar_x.set)
        self.scroll_bar_y.config(command=self.table_tree.yview)
        self.scroll_bar_y.pack(side=RIGHT, fill=Y)

        self.scroll_bar_x.config(command=self.table_tree.xview)
        self.scroll_bar_x.pack(side=BOTTOM, fill=X)

        self.table_tree.heading('Roll_No', text='Roll_No', anchor=CENTER)
        self.table_tree.heading('Student Name', text='Student Name', anchor=CENTER)

        self.table_tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.table_tree.column('#1', stretch=NO, minwidth=0, width=50, anchor=CENTER)
        self.table_tree.column('#2', stretch=NO, minwidth=0, width=250)
        self.table_tree.pack(side=TOP, fill=Y, expand=True)
        self.table_tree.bind('<Button-1>', self.item_selected)

        #  Image View
        self.lbl_img = Label(self.frm_tree, text='Image Preview', fg=self.txt_color, width=50)
        self.lbl_img.grid(row=0, column=1, sticky=NSEW, padx=(10, 20), pady=20)

        #  Delete Button
        self.btn_delete = Button(self.frm_tree, text='Delete', command=lambda: self.delete())
        self.btn_delete.grid(row=1, column=1, sticky=E, padx=20, pady=(0, 20))
        Design.custom_button(self.btn_delete)
        self.btn_delete.bind('<Enter>', Design.button_hover)
        self.btn_delete.bind('<Leave>', Design.button_leave)

        self.show_list()

    #  Fetch All Records From Table
    def show_list(self):
        query = f"SELECT Roll_No, Name FROM Students ORDER BY Roll_No ASC"
        records = self.sql.select_all(query)
        self.table_tree.delete(*self.table_tree.get_children())
        for line in records:
            row = line
            self.table_tree.insert("", END, values=row)

    #  TreeView Item Selection Event Fire with item_selection Method
    def item_selected(self, event):
        try:
            for selected_item in self.table_tree.selection():
                item = self.table_tree.item(selected_item)
                name = item['values'][1]

                self.img = Image.open('./imgAttendance/' + name + '.jpg')
                self.img.thumbnail((400, 400))
                self.image = ImageTk.PhotoImage(self.img)
                self.lbl_img.configure(image=self.image, width=400)

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
                    roll_no = item['values'][0]

                    #  Delete Record
                    query = f"""DELETE FROM Students WHERE Roll_No = {roll_no}"""
                    self.sql.delete(query)

                    #  Remove Row From Tree
                    for item in self.table_tree.selection():
                        self.table_tree.delete(item)

                    self.lbl_img.destroy()
                    self.lbl_img = Label(self.frm_tree, text='Image Preview', fg=self.txt_color, width=50)
                    self.lbl_img.grid(row=0, column=1, sticky=NSEW, padx=(10, 20), pady=20)