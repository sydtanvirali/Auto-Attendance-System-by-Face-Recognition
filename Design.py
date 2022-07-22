from tkinter import *
from tkinter import font


class Design:
    #  Menu Buttons Configuration
    @staticmethod
    def menu_custom_button(widget):
        btn_font = font.Font(family='Bahnschrift Condensed', size=16, weight='bold')
        widget.configure(width=220, anchor='w', bd=0, bg='#1E212D', fg='#FFFFFF', activebackground='#EE4141',
                         activeforeground='#FFFFFF', compound=LEFT, font=btn_font)

    #  All Buttons Configuration
    @staticmethod
    def custom_button(widget):
        btn_font = font.Font(family='Bahnschrift Condensed', size=14, weight='bold')
        widget.configure(width=10, bd=0, bg='#1E212D', fg='#FFFFFF', activebackground='#EE4141',
                         activeforeground='#FFFFFF', font=btn_font)

    # Menu Buttons Hover Effect
    @staticmethod
    def button_hover(event):
        event.widget['bg'] = '#F05454'
        event.widget['fg'] = '#FFFFFF'

    @staticmethod
    def button_leave(event):
        event.widget['bg'] = '#1E212D'
        event.widget['fg'] = '#FFFFFF'
