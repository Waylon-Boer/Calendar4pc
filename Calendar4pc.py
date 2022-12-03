from tkinter import *
from tkinter.messagebox import showinfo as TkMsgBox
import datetime, calendar
class __init__():
    def go(self):
        global y, m, xy, xm
        cal.configure(state=NORMAL)
        nxtcal.configure(state=NORMAL)
        cal.delete(1.0, "end")
        nxtcal.delete(1.0, "end")
        if self == "now":
            y, m = datetime.datetime.now().year, datetime.datetime.now().month
        elif self == "m<":
            if m == 1:
                y, m = y - 1, 12
            else:
                m = m - 1
        elif self == "m>":
            if m == 12:
                y, m = y + 1, 1
            else:
                m = m + 1
        elif self == "y<":
            y = y - 1
        elif self == "y>":
            y = y + 1
        cal.insert(INSERT, calendar.month(y, m))
        if m == 12:
            xy, xm = y + 1, 1
        else:
            xy, xm = y, m + 1
        nxtcal.insert(INSERT, calendar.month(xy, xm))
        cal.configure(state=DISABLED)
        nxtcal.configure(state=DISABLED)
    def theme():
        global darkmode
        if darkmode == 0:
            cal.configure(bg="#345", fg="#fff")
            nxtcal.configure(bg="#543", fg="#fff")
            bB.configure(bg="#222", fg="#fff")
            bN.configure(bg="#222", fg="#fff")
            bF.configure(bg="#222", fg="#fff")
            darkmode = 1
        elif darkmode == 1:
            cal.configure(bg="#000", fg="#fff")
            nxtcal.configure(bg="#000", fg="#fff")
            bB.configure(bg="#222", fg="#fff")
            bN.configure(bg="#222", fg="#fff")
            bF.configure(bg="#222", fg="#fff")
            darkmode = 2
        else:
            cal.configure(bg="#acd", fg="#000")
            nxtcal.configure(bg="#dca", fg="#000")
            bB.configure(bg="#ddd", fg="#000")
            bN.configure(bg="#ddd", fg="#000")
            bF.configure(bg="#ddd", fg="#000")
            darkmode = 0
root, darkmode = Tk(), 0
root.title("Calendar4pc")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.attributes("-toolwindow", 1)
root.geometry("500x235")
root.minsize(width=250, height=235)
root.maxsize(width=500, height=235)
f = Frame()
f.grid(row=0, column=0, sticky="nsew")
f.rowconfigure(0, weight=1)
f.columnconfigure(1, weight=1)
cal = Text(f, bg="#acd", font=("Courier New", 14, "bold"), bd=14, relief=FLAT, width=20)
cal.grid(row=0, column=0, sticky="nsew")
nxtcal = Text(f, bg="#dca", font=("Courier New", 14, "bold"), bd=14, relief=FLAT)
nxtcal.grid(row=0, column=1, sticky="nsew")
nav = Frame()
nav.grid(row=1, column=0, sticky="nsew")
for i in range(0, 3):
    nav.columnconfigure(i, weight=1)
bB = Button(nav, text="◄", bg="#ddd", font=("", 11), relief=FLAT, width=1, command=lambda: __init__.go("m<"))
bB.grid(row=0, column=0, sticky="nsew")
bN = Button(nav, text=datetime.datetime.now().date(), bg="#ddd", font=("", 11), relief=FLAT, width=1, command=lambda: __init__.go("now"))
bN.grid(row=0, column=1, sticky="nsew")
bF = Button(nav, text="►", bg="#ddd", font=("", 11), relief=FLAT, width=1, command=lambda: __init__.go("m>"))
bF.grid(row=0, column=2, sticky="nsew")
__init__.go("now")
root.bind("<Left>", lambda a: __init__.go("m<"))
root.bind("<Right>", lambda a: __init__.go("m>"))
root.bind("<Down>", lambda a: __init__.go("y<"))
root.bind("<Up>", lambda a: __init__.go("y>"))
root.bind("<Return>", lambda a: __init__.go("now"))
root.bind("<Escape>", lambda a: __init__.theme())
root.bind("<F1>", lambda a: TkMsgBox("About calendar4pc", "Calendar4pc: A calendar app\nCopyright (C) 2022-" + str(datetime.datetime.now().year) +": Waylon Boer\n\nCalendar4pc is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. Calendar4pc is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with Calendar4pc. If not, see <https://www.gnu.org/licenses/>."))
root.mainloop()
