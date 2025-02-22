from tkinter import *
import datetime, calendar

def get_calendars():
    calendar1.delete(1.0, END)
    calendar1.insert(1.0, calendar.month(y, m))
    calendar2.delete(1.0, END)
    if m == 12:
        calendar2.insert(1.0, calendar.month(y + 1, 1))
    else:
        calendar2.insert(1.0, calendar.month(y, m + 1))

def previous_month():
    global y, m
    if m == 1:
        y = y - 1
        m = 12
    else:
        m = m - 1
    get_calendars()

def next_month():
    global y, m
    if m == 12:
        y = y + 1
        m = 1
    else:
        m = m + 1
    get_calendars()

def now():
    global y, m
    y = datetime.datetime.now().year
    m = datetime.datetime.now().month
    get_calendars()

def previous_year():
    global y
    y = y - 1
    get_calendars()

def next_year():
    global y
    y = y + 1
    get_calendars()
    
def change_window():
    if root.overrideredirect() == None:
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.geometry(f"575x285+{root.winfo_screenwidth()-575-20}+{20}")
        button6.configure(text="")
    else:
        root.overrideredirect(False)
        root.attributes("-topmost", False)
        root.geometry("575x285")
        button6.configure(text="")

root = Tk()
root.title("Calendar4pc")
root.geometry("575x285")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.attributes("-toolwindow", True)
root.resizable(width=False, height=False)
f = Frame(root)
f.grid(row=0, column=0, sticky="nsew")
f.rowconfigure(0, weight=1)
f.columnconfigure(0, weight=1)
f.columnconfigure(1, weight=1)
y = datetime.datetime.now().year
m = datetime.datetime.now().month
calendar1 = Text(f, bd=32, relief=FLAT, font=("Consolas", 15))
calendar1.grid(row=0, column=0, sticky="nsew")
calendar2 = Text(f, bd=32, relief=FLAT, bg="#ccc", font=("Consolas", 15))
calendar2.grid(row=0, column=1, sticky="nsew")
toolbar = Frame(root)
toolbar.grid(row=1, column=0, sticky="nsew")
for i in range(0, 6):
    toolbar.columnconfigure(i, weight=1)
button1 = Button(toolbar, relief=FLAT, font=("Segoe Fluent Icons", 13), text="", command=previous_month)
button1.grid(row=0, column=0, sticky="nsew", ipady=4)
button2 = Button(toolbar, relief=FLAT, font=("Segoe Fluent Icons", 13), text="", command=next_month)
button2.grid(row=0, column=1, sticky="nsew", ipady=4)
button3 = Button(toolbar, relief=FLAT, font=("Segoe Fluent Icons", 13), text="", command=now)
button3.grid(row=0, column=2, sticky="nsew", ipady=4)
button4 = Button(toolbar, relief=FLAT, font=("Segoe Fluent Icons", 13), text="", command=previous_year)
button4.grid(row=0, column=3, sticky="nsew", ipady=4)
button5 = Button(toolbar, relief=FLAT, font=("Segoe Fluent Icons", 13), text="", command=next_year)
button5.grid(row=0, column=4, sticky="nsew", ipady=4)
button6 = Button(toolbar, relief=FLAT, font=("Segoe Fluent Icons", 13), text="", command=change_window)
button6.grid(row=0, column=5, sticky="nsew", ipady=4)
now()
root.mainloop()
