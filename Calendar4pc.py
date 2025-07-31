from tkinter import *
from tkinter.ttk import Menubutton, Spinbox, Button, Entry, Style
from tkinter.messagebox import showinfo, showerror
import datetime, calendar
import threading
import time    

def set_function(num):
    for i in [button_previous, button_next, button_go_to, calendarFrame, text, calendar2, clock, timerFrame, stopwatchFrame]:
        i.grid_forget()
    if num == 0:
        menubutton.configure(text="Calendar")
        button_previous.grid(row=0, column=1, sticky="nse")
        button_next.grid(row=0, column=2, sticky="nse")
        button_go_to.grid(row=0, column=3, sticky="nse")
        calendarFrame.grid(row=1, column=0, sticky="nsew")
        text.grid(row=0, column=1, sticky="nsew")
    elif num == 1:
        menubutton.configure(text="Dual Calendar")
        button_previous.grid(row=0, column=1, sticky="nse")
        button_next.grid(row=0, column=2, sticky="nse")
        button_go_to.grid(row=0, column=3, sticky="nse")
        calendarFrame.grid(row=1, column=0, sticky="nsew")
        calendar2.grid(row=0, column=1, sticky="nsew")
    elif num == 2:
        menubutton.configure(text="Alarm Clock")
    elif num == 3:
        menubutton.configure(text="Clock")
        clock.grid(row=1, column=0, sticky="nsew")
    elif num == 4:
        menubutton.configure(text="Timer")
        timerFrame.grid(row=1, column=0, sticky="nsew")
    elif num == 5:
        menubutton.configure(text="Stopwatch")
        stopwatchFrame.grid(row=1, column=0, sticky="nsew")

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
    timer_entry_h.delete(0, END)
    timer_entry_h.insert(0, hours)
    timer_entry_m.delete(0, END)
    timer_entry_m.insert(0, minutes)
    timer_entry_s.delete(0, END)
    timer_entry_s.insert(0, seconds)

def start_timer():
    if int(timer_entry_m.get()) > 59 or int(timer_entry_s.get()) > 59:
        showerror("Timer", "Invalid input.")
        if int(timer_entry_m.get()) > 59:
            timer_entry_m.focus_set()
            timer_entry_m.select_range(0, END)
        else:
            timer_entry_s.focus_set()
            timer_entry_s.select_range(0, END)
    else:
        timer_button_3.configure(text="Stop", command=stop_timer)
        timerFrame.bind("<Return>", lambda i: stop_timer())
        while 3600 * int(timer_entry_h.get()) + 60 * int(timer_entry_m.get()) + int(timer_entry_s.get()) > 0:
            if int(timer_entry_s.get()) > 0:
                time.sleep(1)
                seconds = int(timer_entry_s.get())
                timer_entry_s.delete(0, END)
                timer_entry_s.insert(0, seconds - 1)
            else:
                if int(timer_entry_m.get()) > 0:
                    minutes = int(timer_entry_m.get())
                    timer_entry_m.delete(0, END)
                    timer_entry_m.insert(0, minutes - 1)
                    timer_entry_s.delete(0, END)
                    timer_entry_s.insert(0, 59)
                else:
                    if int(timer_entry_h.get()) > 0:
                        hours = int(timer_entry_h.get())
                        timer_entry_h.delete(0, END)
                        timer_entry_h.insert(0, hours - 1)
                        timer_entry_m.delete(0, END)
                        timer_entry_m.insert(0, 59)
                        timer_entry_s.delete(0, END)
                        timer_entry_s.insert(0, 59)
        set_timer(0, 0, 0)
        showinfo("Timer", "The timer is ready!")

def stop_timer():
    set_timer(0, 0, 0)
    timer_button_3.configure(text="Start", command=lambda: threading.Thread(target=start_timer).start())
    timerFrame.bind("<Return>", lambda i: threading.Thread(target=start_timer).start())

def start_stopwatch():
    
    while True:
        if int(stopwatch_entry_s.get()) < 59:
            time.sleep(1)
            seconds = int(stopwatch_entry_s.get())
            stopwatch_entry_s.delete(0, END)
            stopwatch_entry_s.insert(0, seconds + 1)
        else:
            if int(stopwatch_entry_m.get()) < 59:
                minutes = int(stopwatch_entry_m.get())
                stopwatch_entry_m.delete(0, END)
                stopwatch_entry_m.insert(0, minutes + 1)
                stopwatch_entry_s.delete(0, END)
                stopwatch_entry_s.insert(0, 0)
            else:
                hours = int(stopwatch_entry_h.get())
                stopwatch_entry_h.delete(0, END)
                stopwatch_entry_h.insert(0, hours + 1)
                stopwatch_entry_m.delete(0, END)
                stopwatch_entry_m.insert(0, 0)
                stopwatch_entry_s.delete(0, END)
                stopwatch_entry_s.insert(0, 0)

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

toolbar = Frame(root, border=4)
toolbar.grid(row=0, column=0, sticky="nsew")
toolbar.columnconfigure(1, weight=1)
menubutton = Menubutton(toolbar, text="Widgets")
menubutton.grid(row=0, column=0, sticky="nsw")
function = IntVar(value=0)
menu = Menu(menubutton, tearoff=False, activeborderwidth=2.5, activebackground="#e1e1e1", activeforeground="#000")
menu.add_radiobutton(label="Calendar", variable=function, value=0, command=lambda: set_function(0))
menu.add_radiobutton(label="Dual Calendar", variable=function, value=1, command=lambda: set_function(1))
menu.add_separator()
menu.add_radiobutton(label="Alarm Clock", variable=function, value=2, command=lambda: set_function(2))
menu.add_radiobutton(label="Clock", variable=function, value=3, command=lambda: set_function(3))
menu.add_radiobutton(label="Timer", variable=function, value=4, command=lambda: set_function(4))
menu.add_radiobutton(label="Stopwatch", variable=function, value=5, command=lambda: set_function(5))
menubutton.configure(menu=menu)
button_previous = Button(toolbar, width=5, text="<", command=previous_month)
button_previous.grid(row=0, column=1, sticky="nse")
button_next = Button(toolbar, width=5, text=">", command=next_month)
button_next.grid(row=0, column=2, sticky="nse")
menuGoTo = Menu(root, tearoff=False, activeborderwidth=2.5, activebackground="#e1e1e1", activeforeground="#000")
menuGoTo.add_command(label="Today", command=now)
menuGoTo.add_command(label="Previous Year", command=previous_year)
menuGoTo.add_command(label="Next Year", command=next_year)
button_go_to = Button(toolbar, text="Go To")
button_go_to.grid(row=0, column=3, sticky="nse", padx=(0, 2))
button_go_to.bind("<Button-1>", lambda i: menuGoTo.tk_popup(button_go_to.winfo_rootx()-58, button_go_to.winfo_rooty()+25))


calendarFrame = Frame(root)
calendarFrame.grid(row=1, column=0, sticky="nsew")
calendarFrame.rowconfigure(0, weight=1)
calendarFrame.columnconfigure(0, weight=1)
calendarFrame.columnconfigure(1, weight=1)
y = datetime.datetime.now().year
m = datetime.datetime.now().month
calendar1 = Text(calendarFrame, width=1, bd=32, relief=FLAT, font=("Consolas", 15), bg="#fff", insertbackground="#fff")
calendar1.grid(row=0, column=0, sticky="nsew")
calendar1.tag_configure(SEL, background="#fff", foreground="#000")
calendar2 = Text(calendarFrame, width=1, bd=32, relief=FLAT, font=("Consolas", 15), bg="#e1e1e1", insertbackground="#e1e1e1")
calendar2.tag_configure(SEL, background="#e1e1e1", foreground="#000")
text = Text(calendarFrame, width=1, bd=32, relief=FLAT, font=("tkDefaultFont", 16), bg="#e1e1e1", insertbackground="#e1e1e1")
text.grid(row=0, column=1, sticky="nsew")
text.tag_configure(SEL, background="#e1e1e1", foreground="#000")
text.tag_configure("large", font=("tkDefaultFont", 32))
now()

clock = Text(root, relief=FLAT, font=("tkDefaultFont", 52), bg="#e1e1e1", insertbackground="#e1e1e1")
clock.tag_configure(SEL, background="#e1e1e1", foreground="#000")
clock.tag_configure("centered", justify='center')

Style().configure("Light.TSpinbox", background="#e1e1e1")
Style().configure("Light.TButton", background="#e1e1e1")

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
timer_entry_h = Spinbox(timerFrame, values=list(range(0, 100)), style="Light.TSpinbox")
timer_entry_h.grid(row=1, column=0, sticky="nsew", padx=(0, 1), pady=(0, 16))
timer_entry_h.insert(0, 0)
timer_entry_m = Spinbox(timerFrame, values=list(range(0, 60)), style="Light.TSpinbox")
timer_entry_m.grid(row=1, column=1, sticky="nsew", padx=1, pady=(0, 16))
timer_entry_m.insert(0, 0)
timer_entry_s = Spinbox(timerFrame, values=list(range(0, 60)), style="Light.TSpinbox")
timer_entry_s.grid(row=1, column=2, sticky="nsew", padx=(1, 0), pady=(0, 16))
timer_entry_s.insert(0, 0)
timer_button_1 = Button(timerFrame, text="5 min", command=lambda: set_timer(0, 5, 0), style="Light.TButton")
timer_button_1.grid(row=2, column=0, sticky="nsew")
timer_button_2 = Button(timerFrame, text="25 min", command=lambda: set_timer(0, 25, 0), style="Light.TButton")
timer_button_2.grid(row=2, column=1, sticky="nsew")
timer_button_3 = Button(timerFrame, text="Start", command=lambda: threading.Thread(target=start_timer).start(), style="Light.TButton")
timer_button_3.grid(row=2, column=2, sticky="nsew")
timerFrame.bind("<Return>", lambda i: threading.Thread(target=start_timer).start())

stopwatchFrame = Frame(root, background="#e1e1e1")
stopwatchFrame.rowconfigure(2, weight=1)
stopwatchFrame.rowconfigure(3, weight=1)
for i in range(0, 3):
    stopwatchFrame.columnconfigure(i, weight=1)
stopwatchFrame.configure(bd=16)
stopwatch_label_h = Label(stopwatchFrame, text="Hours", background="#e1e1e1")
stopwatch_label_h.grid(row=0, column=0, sticky="w")
stopwatch_label_m = Label(stopwatchFrame, text="Minutes", background="#e1e1e1")
stopwatch_label_m.grid(row=0, column=1, sticky="w")
stopwatch_label_s = Label(stopwatchFrame, text="Seconds", background="#e1e1e1")
stopwatch_label_s.grid(row=0, column=2, sticky="w")
stopwatch_entry_h = Entry(stopwatchFrame, style="Light.TSpinbox")
stopwatch_entry_h.grid(row=1, column=0, sticky="nsew", padx=(0, 1), pady=(0, 16))
stopwatch_entry_h.insert(0, 0)
stopwatch_entry_m = Entry(stopwatchFrame, style="Light.TSpinbox")
stopwatch_entry_m.grid(row=1, column=1, sticky="nsew", padx=1, pady=(0, 16))
stopwatch_entry_m.insert(0, 0)
stopwatch_entry_s = Entry(stopwatchFrame, style="Light.TSpinbox")
stopwatch_entry_s.grid(row=1, column=2, sticky="nsew", padx=(1, 0), pady=(0, 16))
stopwatch_entry_s.insert(0, 0)
stopwatch_button_1 = Button(stopwatchFrame, text="Start", command=lambda: threading.Thread(target=start_stopwatch).start(), style="Light.TButton")
stopwatch_button_1.grid(row=2, column=1, sticky="nsew")
stopwatchFrame.bind("<Return>", lambda i: threading.Thread(target=start_stopwatch).start())

set_function(0)
refresh()

root.mainloop()
