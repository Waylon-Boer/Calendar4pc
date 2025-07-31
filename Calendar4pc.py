from tkinter import *
from tkinter.ttk import Menubutton, Spinbox, Button, Style
from tkinter.messagebox import showinfo, showerror
import datetime, calendar
import threading
import time    

def set_function(num):
    for i in [calendarFrame, timerFrame]:
        i.grid_forget()
    if num == 1:
        calendarFrame.grid(row=1, column=0, sticky="nsew")
    else:
        timerFrame.grid(row=1, column=0, sticky="nsew")

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
    
def set_timer(hours, minutes, seconds):
    entry_h.delete(0, END)
    entry_h.insert(0, hours)
    entry_m.delete(0, END)
    entry_m.insert(0, minutes)
    entry_s.delete(0, END)
    entry_s.insert(0, seconds)

def start_timer():
    if int(entry_m.get()) > 59 or int(entry_s.get()) > 59:
        showerror("Timer", "Invalid input.")
        if int(entry_m.get()) > 59:
            entry_m.focus_set()
            entry_m.select_range(0, END)
        else:
            entry_s.focus_set()
            entry_s.select_range(0, END)
    else:
        button_c1.configure(text="Stop", command=stop_timer)
        timerFrame.bind("<Return>", lambda i: stop_timer())
        while 3600 * int(entry_h.get()) + 60 * int(entry_m.get()) + int(entry_s.get()) > 0:
            if int(entry_s.get()) > 0:
                time.sleep(1)
                seconds = int(entry_s.get())
                entry_s.delete(0, END)
                entry_s.insert(0, seconds - 1)
            else:
                if int(entry_m.get()) > 0:
                    minutes = int(entry_m.get())
                    entry_m.delete(0, END)
                    entry_m.insert(0, minutes - 1)
                    entry_s.delete(0, END)
                    entry_s.insert(0, 59)
                else:
                    if int(entry_h.get()) > 0:
                        hours = int(entry_h.get())
                        entry_h.delete(0, END)
                        entry_h.insert(0, hours - 1)
                        entry_m.delete(0, END)
                        entry_m.insert(0, 59)
                        entry_s.delete(0, END)
                        entry_s.insert(0, 59)
        set_timer(0, 0, 0)
        showinfo("Timer", "The timer is ready!")

def stop_timer():
    set_timer(0, 0, 0)
    button_c1.configure(text="Start", command=lambda: threading.Thread(target=start_timer).start())
    timerFrame.bind("<Return>", lambda i: threading.Thread(target=start_timer).start())

root = Tk()
root.title("Calendar4pc")
root.geometry("575x285")
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.attributes("-toolwindow", True)
root.resizable(width=False, height=False)
calendarFrame = Frame(root)
calendarFrame.grid(row=1, column=0, sticky="nsew")
calendarFrame.rowconfigure(0, weight=1)
calendarFrame.columnconfigure(0, weight=1)
calendarFrame.columnconfigure(1, weight=1)
y = datetime.datetime.now().year
m = datetime.datetime.now().month
calendar1 = Text(calendarFrame, bd=32, relief=FLAT, font=("Consolas", 15), bg="#fff", insertbackground="#fff")
calendar1.grid(row=0, column=0, sticky="nsew")
calendar1.tag_configure(SEL, background="#fff", foreground="#000")
calendar2 = Text(calendarFrame, bd=32, relief=FLAT, font=("Consolas", 15), bg="#e1e1e1", insertbackground="#e1e1e1")
calendar2.grid(row=0, column=1, sticky="nsew")
calendar2.tag_configure(SEL, background="#e1e1e1", foreground="#000")
toolbar = Frame(root, border=4)
toolbar.grid(row=0, column=0, sticky="nsew")
menubutton = Menubutton(toolbar, text="Widgets")
menubutton.grid(row=0, column=0, sticky="nsew")
function = IntVar(value=1)
menu = Menu(menubutton, tearoff=False, activeborderwidth=2.5)
menu.add_radiobutton(label="Calendar", variable=function, value=0, command=lambda: set_function(0))
menu.add_radiobutton(label="Dual Calendar", variable=function, value=1, command=lambda: set_function(1))
menu.add_separator()
menu.add_radiobutton(label="Alarm Clock", variable=function, value=2, command=lambda: set_function(2))
menu.add_radiobutton(label="Clock", variable=function, value=3, command=lambda: set_function(3))
menu.add_radiobutton(label="Timer", variable=function, value=4, command=lambda: set_function(4))
menu.add_radiobutton(label="Stopwatch", variable=function, value=5, command=lambda: set_function(5))
menubutton.configure(menu=menu)
now()

Style().configure("Light.TSpinbox", background="#e1e1e1")
Style().configure("Light.TButton", background="#e1e1e1")

timerFrame = Frame(root, background="#e1e1e1")
timerFrame.rowconfigure(2, weight=1)
timerFrame.rowconfigure(3, weight=1)
for i in range(0, 3):
    timerFrame.columnconfigure(i, weight=1)
timerFrame.configure(bd=16)
label_h = Label(timerFrame, text="Hours", background="#e1e1e1")
label_h.grid(row=0, column=0, sticky="w")
label_m = Label(timerFrame, text="Minutes", background="#e1e1e1")
label_m.grid(row=0, column=1, sticky="w")
label_s = Label(timerFrame, text="Seconds", background="#e1e1e1")
label_s.grid(row=0, column=2, sticky="w")
entry_h = Spinbox(timerFrame, values=list(range(0, 100)), style="Light.TSpinbox")
entry_h.grid(row=1, column=0, sticky="nsew", padx=(0, 1), pady=(0, 16))
entry_h.insert(0, 0)
entry_m = Spinbox(timerFrame, values=list(range(0, 60)), style="Light.TSpinbox")
entry_m.grid(row=1, column=1, sticky="nsew", padx=1, pady=(0, 16))
entry_m.insert(0, 0)
entry_s = Spinbox(timerFrame, values=list(range(0, 60)), style="Light.TSpinbox")
entry_s.grid(row=1, column=2, sticky="nsew", padx=(1, 0), pady=(0, 16))
entry_s.insert(0, 0)
button_a1 = Button(timerFrame, text="5 min", command=lambda: set_timer(0, 5, 0), style="Light.TButton")
button_a1.grid(row=2, column=0, sticky="nsew")
button_b1 = Button(timerFrame, text="Pomodoro Timer", command=lambda: set_timer(0, 25, 0), style="Light.TButton")
button_b1.grid(row=2, column=1, sticky="nsew")
button_c1 = Button(timerFrame, text="Start", command=lambda: threading.Thread(target=start_timer).start(), style="Light.TButton")
button_c1.grid(row=2, column=2, sticky="nsew")
timerFrame.bind("<Return>", lambda i: threading.Thread(target=start_timer).start())

root.mainloop()
