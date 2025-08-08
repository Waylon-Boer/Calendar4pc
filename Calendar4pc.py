from tkinter import *
from tkinter.ttk import Menubutton, Spinbox, Button, Entry, Style, Notebook
from tkinter.messagebox import showinfo, showerror
from tkinter import font
import datetime, calendar
import threading
import time    

def set_function(num):
    for i in [button_previous, button_next, go_to_menubutton, calendarFrame, text, calendar2, timerFrame]:
        i.grid_forget()
    if num == 0:
        main_menubutton.configure(text="Calendar")
        button_previous.grid(row=0, column=1, sticky="nse")
        button_next.grid(row=0, column=2, sticky="nse")
        go_to_menubutton.grid(row=0, column=3, sticky="nse")
        calendarFrame.grid(row=1, column=0, sticky="nsew")
        text.grid(row=0, column=1, sticky="nsew")
    elif num == 1:
        main_menubutton.configure(text="Dual Calendar")
        button_previous.grid(row=0, column=1, sticky="nse")
        button_next.grid(row=0, column=2, sticky="nse")
        go_to_menubutton.grid(row=0, column=3, sticky="nse")
        calendarFrame.grid(row=1, column=0, sticky="nsew")
        calendar2.grid(row=0, column=1, sticky="nsew")
    elif num == 2:
        main_menubutton.configure(text="Timer")
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
    timer_spinbox_h.delete(0, END)
    timer_spinbox_h.insert(0, hours)
    timer_spinbox_m.delete(0, END)
    timer_spinbox_m.insert(0, minutes)
    timer_spinbox_s.delete(0, END)
    timer_spinbox_s.insert(0, seconds)

def start_timer():
    if int(timer_spinbox_m.get()) > 59 or int(timer_spinbox_s.get()) > 59:
        showerror("Timer", "Invalid input.")
        if int(timer_spinbox_m.get()) > 59:
            timer_spinbox_m.focus_set()
            timer_spinbox_m.select_range(0, END)
        else:
            timer_spinbox_s.focus_set()
            timer_spinbox_s.select_range(0, END)
    else:
        timer_button_3.configure(text="Stop", command=stop_timer)
        timerFrame.bind("<Return>", lambda event: stop_timer())
        while 3600 * int(timer_spinbox_h.get()) + 60 * int(timer_spinbox_m.get()) + int(timer_spinbox_s.get()) > 0:
            if int(timer_spinbox_s.get()) > 0:
                time.sleep(1)
                seconds = int(timer_spinbox_s.get())
                timer_spinbox_s.delete(0, END)
                timer_spinbox_s.insert(0, seconds - 1)
            else:
                if int(timer_spinbox_m.get()) > 0:
                    minutes = int(timer_spinbox_m.get())
                    timer_spinbox_m.delete(0, END)
                    timer_spinbox_m.insert(0, minutes - 1)
                    timer_spinbox_s.delete(0, END)
                    timer_spinbox_s.insert(0, 59)
                else:
                    if int(timer_spinbox_h.get()) > 0:
                        hours = int(timer_spinbox_h.get())
                        timer_spinbox_h.delete(0, END)
                        timer_spinbox_h.insert(0, hours - 1)
                        timer_spinbox_m.delete(0, END)
                        timer_spinbox_m.insert(0, 59)
                        timer_spinbox_s.delete(0, END)
                        timer_spinbox_s.insert(0, 59)
        set_timer(0, 0, 0)
        showinfo("Timer", "The timer is ready!")

def stop_timer():
    set_timer(0, 0, 0)
    timer_button_3.configure(text="Start", command=lambda: threading.Thread(target=start_timer).start())
    timerFrame.bind("<Return>", lambda event: threading.Thread(target=start_timer).start())

def refresh():
    text.delete(1.0, END)
    text.insert(INSERT, f"\n{datetime.datetime.now().strftime('%H:%M:%S')}\n")
    text.insert(INSERT, f"{datetime.datetime.now().day} {months[datetime.datetime.now().month]} {datetime.datetime.now().year}\n\n")
    text.insert(INSERT, f"Week {int(datetime.datetime.now().isocalendar().week)} - {weekdays[datetime.datetime.now().weekday()]}")
    text.tag_add("large", 2.0, 3.0)
    clock.delete(1.0, END)
    clock.insert(INSERT, f"\n{datetime.datetime.now().strftime('%H:%M:%S')}\n")
    clock.tag_add("centered", 1.0, END)
    root.after(1, refresh)

def change_theme():
    if toolbar.cget("background") == "#f0f0f0":
        calendar1.configure(bg="#1e1e1e", fg="#ffffff", insertbackground="#1e1e1e")
        calendar1.tag_configure(SEL, background="#1e1e1e", foreground="#ffffff")
        calendar2.configure(bg="#000000", fg="#ffffff", insertbackground="#000000")
        calendar2.tag_configure(SEL, background="#000000", foreground="#ffffff")
        text.configure(bg="#000000", fg="#ffffff", insertbackground="#000000")
        text.tag_configure(SEL, background="#000000", foreground="#ffffff")
        toolbar.configure(bg="#0f0f0f")
        for i in [MainMenu, GoToMenu]:
            i.configure(background="#0f0f0f", foreground="#ffffff", activebackground="#1e1e1e", activeforeground="#ffffff", selectcolor="#fff")
        main_menubutton.configure(style="Dark.Toolbar.TMenubutton")
        for i in [button_previous, button_next, go_to_menubutton]:
            i.configure(style="Dark.Toolbar.TButton")
        timerFrame.configure(background="#1e1e1e")
        for i in [timer_label_h, timer_label_m, timer_label_s]:
            i.configure(background="#1e1e1e", foreground="#ffffff")
        for i in [timer_spinbox_h, timer_spinbox_m, timer_spinbox_s]:
            i.configure(style="Dark.TSpinbox")
        for i in [timer_button_1, timer_button_2, timer_button_3]:
            i.configure(style="Dark.TButton")
    else:
        calendar1.configure(bg="#ffffff", fg="#000000", insertbackground="#ffffff")
        calendar1.tag_configure(SEL, background="#ffffff", foreground="#000000")
        calendar2.configure(bg="#e1e1e1", fg="#000000", insertbackground="#e1e1e1")
        calendar2.tag_configure(SEL, background="#e1e1e1", foreground="#000000")
        text.configure(bg="#e1e1e1", fg="#000000", insertbackground="#e1e1e1")
        text.tag_configure(SEL, background="#e1e1e1", foreground="#000000")
        toolbar.configure(bg="#f0f0f0")
        for i in [MainMenu, GoToMenu]:
            i.configure(background="#f0f0f0", foreground="#000000", activebackground="#e1e1e1", activeforeground="#000000", selectcolor="#000")
        main_menubutton.configure(style="TMenubutton")
        for i in [button_previous, button_next, go_to_menubutton]:
            i.configure(style="TButton")
        timerFrame.configure(background="#e1e1e1")
        for i in [timer_label_h, timer_label_m, timer_label_s]:
            i.configure(background="#e1e1e1", foreground="#000000")
        for i in [timer_spinbox_h, timer_spinbox_m, timer_spinbox_s]:
            i.configure(style="Light.TSpinbox")
        for i in [timer_button_1, timer_button_2, timer_button_3]:
            i.configure(style="Light.TButton")

def help_window():
    window = Toplevel()
    try:
        window.iconbitmap("icon.ico")
    except:
        window.iconbitmap("")
    window.title("Help - Calendar4pc")
    window.geometry("700x510")
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    help_tabs = Notebook(window)
    help_tabs.grid(row=0, column=0, sticky="nsew")
    about = Text(help_tabs, relief=FLAT, border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap=WORD, background="#dcb")
    about.insert(INSERT, f"Calendar4pc\nCopyright (c) 2025-{str(datetime.datetime.now().year)}: Waylon Boer\n\nCalendar4pc is a calendar app with multiple lay-outs.")
    about.configure(state=DISABLED)
    help_tabs.add(about, text="About")
    mit_license = Text(help_tabs, relief=FLAT, border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap=WORD, background="#dcb")
    mit_license.insert(INSERT, """MIT License

Copyright (c) 2025 Waylon Boer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""")
    mit_license.configure(state=DISABLED)
    help_tabs.add(mit_license, text="License")
    window.mainloop()
    
def pin():
    root.attributes("-topmost", not root.attributes("-topmost"))
    root.overrideredirect(not root.overrideredirect())


weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

root = Tk()
root.title("Calendar4pc")
root.geometry("575x285")
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.resizable(width=False, height=False)
try:
    root.iconbitmap("icon.ico")
except:
    root.iconbitmap("")

Style().configure("Dark.Toolbar.TMenubutton", background="#0f0f0f", foreground="#ffffff")
Style().configure("Dark.Toolbar.TButton", background="#0f0f0f")
Style().configure("Light.TSpinbox", background="#e1e1e1")
Style().configure("Light.TButton", background="#e1e1e1")
Style().configure("Dark.TSpinbox", background="#1e1e1e")
Style().configure("Dark.TButton", background="#1e1e1e")

toolbar = Frame(root, border=4, background="#f0f0f0")
toolbar.grid(row=0, column=0, sticky="nsew")
toolbar.columnconfigure(1, weight=1)
main_menubutton = Menubutton(toolbar, text="Widgets")
main_menubutton.grid(row=0, column=0, sticky="nsw")
function = IntVar(value=0)
MainMenu = Menu(main_menubutton, tearoff=False, activeborderwidth=2.5, activebackground="#e1e1e1", activeforeground="#000000")
MainMenu.add_radiobutton(label="Calendar", variable=function, value=0, command=lambda: set_function(0))
MainMenu.add_radiobutton(label="Dual Calendar", variable=function, value=1, command=lambda: set_function(1))
MainMenu.add_separator()
MainMenu.add_radiobutton(label="Timer", variable=function, value=4, command=lambda: set_function(2))
main_menubutton.configure(menu=MainMenu)
button_previous = Button(toolbar, width=5, text="<", command=previous_month)
button_previous.grid(row=0, column=1, sticky="nse")
button_next = Button(toolbar, width=5, text=">", command=next_month)
button_next.grid(row=0, column=2, sticky="nse")
go_to_menubutton = Menubutton(toolbar, text="Go To", style="TButton", direction="left")
go_to_menubutton.grid(row=0, column=3, sticky="nse", padx=(0, 2))
GoToMenu = Menu(go_to_menubutton, tearoff=False, activeborderwidth=2.5, activebackground="#e1e1e1", activeforeground="#000000")
GoToMenu.add_command(label="Today", command=now)
GoToMenu.add_command(label="Previous Year", command=previous_year)
GoToMenu.add_command(label="Next Year", command=next_year)
GoToMenu.add_separator()
GoToMenu.add_command(label="Help", command=help_window)
go_to_menubutton.configure(menu=GoToMenu)

calendarFrame = Frame(root)
calendarFrame.grid(row=1, column=0, sticky="nsew")
calendarFrame.rowconfigure(0, weight=1)
calendarFrame.columnconfigure(0, weight=1)
calendarFrame.columnconfigure(1, weight=1)
y = datetime.datetime.now().year
m = datetime.datetime.now().month
calendar1 = Text(calendarFrame, width=1, bd=32, relief=FLAT, font=("Consolas", 15), bg="#ffffff", insertbackground="#ffffff")
calendar1.grid(row=0, column=0, sticky="nsew")
calendar1.tag_configure(SEL, background="#ffffff", foreground="#000000")
calendar2 = Text(calendarFrame, width=1, bd=32, relief=FLAT, font=("Consolas", 15), bg="#e1e1e1", insertbackground="#e1e1e1")
calendar2.tag_configure(SEL, background="#e1e1e1", foreground="#000000")
text = Text(calendarFrame, width=1, bd=32, relief=FLAT, font=("tkDefaultFont", 16), bg="#e1e1e1", insertbackground="#e1e1e1")
text.grid(row=0, column=1, sticky="nsew")
text.tag_configure(SEL, background="#e1e1e1", foreground="#000000")
text.tag_configure("large", font=("tkDefaultFont", 32))
now()

clock = Text(root, relief=FLAT, font=("tkDefaultFont", 52), bg="#e1e1e1", insertbackground="#e1e1e1")
clock.tag_configure(SEL, background="#e1e1e1", foreground="#000000")
clock.tag_configure("centered", justify='center')

timerFrame = Frame(root, background="#e1e1e1")
timerFrame.rowconfigure(2, weight=1)
timerFrame.rowconfigure(3, weight=1)
for i in range(0, 3):
    timerFrame.columnconfigure(i, weight=1)
timerFrame.configure(bd=16)
timer_label_h = Label(timerFrame, text="Hours", background="#e1e1e1")
timer_label_h.grid(row=0, column=0, sticky="w")
timer_label_m = Label(timerFrame, text="Minutes", background="#e1e1e1")
timer_label_m.grid(row=0, column=1, sticky="w")
timer_label_s = Label(timerFrame, text="Seconds", background="#e1e1e1")
timer_label_s.grid(row=0, column=2, sticky="w")
timer_spinbox_h = Spinbox(timerFrame, values=list(range(0, 100)), style="Light.TSpinbox")
timer_spinbox_h.grid(row=1, column=0, sticky="nsew", padx=(0, 1), pady=(0, 16))
timer_spinbox_h.insert(0, 0)
timer_spinbox_m = Spinbox(timerFrame, values=list(range(0, 60)), style="Light.TSpinbox")
timer_spinbox_m.grid(row=1, column=1, sticky="nsew", padx=1, pady=(0, 16))
timer_spinbox_m.insert(0, 0)
timer_spinbox_s = Spinbox(timerFrame, values=list(range(0, 60)), style="Light.TSpinbox")
timer_spinbox_s.grid(row=1, column=2, sticky="nsew", padx=(1, 0), pady=(0, 16))
timer_spinbox_s.insert(0, 0)
timer_button_1 = Button(timerFrame, text="5 min", command=lambda: set_timer(0, 5, 0), style="Light.TButton")
timer_button_1.grid(row=2, column=0, sticky="nsew")
timer_button_2 = Button(timerFrame, text="25 min", command=lambda: set_timer(0, 25, 0), style="Light.TButton")
timer_button_2.grid(row=2, column=1, sticky="nsew")
timer_button_3 = Button(timerFrame, text="Start", command=lambda: threading.Thread(target=start_timer).start(), style="Light.TButton")
timer_button_3.grid(row=2, column=2, sticky="nsew")
timerFrame.bind("<Return>", lambda event: threading.Thread(target=start_timer).start())

set_function(0)
refresh()
root.bind("<F1>", lambda event: help_window())
root.bind("<Double-Button-1>", lambda event: pin())
root.bind("<Button-3>", lambda event: change_theme())
root.mainloop()