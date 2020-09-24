from tkinter import *
# import tkMessageBox
import tkinter

top = Tk()

Lb1 = Listbox(top, selectmode=MULTIPLE)
Lb1.insert(1, "Python")
Lb1.insert(2, "Perl")
Lb1.insert(3, "C")
Lb1.insert(4, "PHP")
Lb1.insert(5, "JSP")
Lb1.insert(6, "Ruby")
Lb1.insert(7, "Python")
Lb1.insert(8, "Perl")
Lb1.insert(9, "C")
Lb1.insert(10, "PHP")
Lb1.insert(11, "JSP")
Lb1.insert(12, "Ruby")
Lb1.insert(13, "Python")
Lb1.insert(14, "Perl")
Lb1.insert(15, "C")
Lb1.insert(16, "PHP")
Lb1.insert(17, "JSP")
Lb1.insert(18, "Ruby")
Lb1.yview_scroll(1, UNITS)
Lb1.pack()
top.mainloop()