import tkinter as tk
from tkinter import ttk, filedialog, font
import datetime, calendar
import ctypes as ct

class Calendar4pc:
    def __init__(self):
        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        self.root = tk.Tk()
        self.root.title("Calendar4pc")
        self.root.geometry("580x285")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.resizable(width=False, height=False)
        self.root.minsize(width=290, height=285)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        self.style = ttk.Style(self.root)
        self.style.layout("Treeview", [("Event.Treeview.treearea", {"sticky": "nsew"})])

        self.ics_events = []
        self.ics_index = 0

        self.toolbar = tk.Frame(self.root, background="#F1F1F1")
        self.toolbar.grid(row=0, column=0, sticky="nsew")
        self.toolbar.columnconfigure(2, weight=1)

        self.button_previous_y = tk.Button(self.toolbar, width=5, text="Y-", command=self.previous_year)
        self.button_previous_m = tk.Button(self.toolbar, width=5, text="M-", command=self.previous_month)

        self.main_menubutton = ttk.Menubutton(self.toolbar, text="Widgets")
        self.main_menubutton.grid(row=0, column=2, sticky="ns", padx=5, pady=5)
        self.function = tk.IntVar(value=0)
        self.main_menu = tk.Menu(self.main_menubutton, tearoff=False, activeborderwidth=2.5)
        self.main_menu.add_radiobutton(label="Calendar", variable=self.function, value=0, command=lambda: self.set_function(0))
        self.main_menu.add_radiobutton(label="Dual Calendar", variable=self.function, value=1, command=lambda: self.set_function(1))
        self.main_menu.add_radiobutton(label="Annual Calendar", variable=self.function, value=2, command=lambda: self.set_function(2))
        self.main_menu.add_separator()
        self.main_menu.add_radiobutton(label="Events", variable=self.function, value=3, command=lambda: self.set_function(3))
        self.main_menu.add_radiobutton(label="Clock", variable=self.function, value=4, command=lambda: self.set_function(4))
        self.main_menubutton.configure(menu=self.main_menu)

        self.button_next_m = tk.Button(self.toolbar, width=5, text="M+", command=self.next_month)
        self.button_next_y = tk.Button(self.toolbar, width=5, text="Y+", command=self.next_year)

        for button in [self.button_previous_y, self.button_previous_m, self.button_next_m, self.button_next_y]:
            button.configure(bd=0)

        self.calendarFrame = tk.Frame(self.root)
        self.calendarFrame.grid(row=1, column=0, sticky="nsew")
        self.calendarFrame.rowconfigure(0, weight=1)
        self.calendarFrame.columnconfigure(0, weight=1)
        self.calendarFrame.columnconfigure(1, weight=1)

        self.y = datetime.datetime.now().year
        self.m = datetime.datetime.now().month

        self.calendar1 = tk.Text(self.calendarFrame, width=1, bd=32, relief=tk.FLAT, font=("Consolas", 15), bg="#ffffff", insertbackground="#ffffff")
        self.calendar1.grid(row=0, column=0, sticky="nsew")
        self.calendar1.tag_configure(tk.SEL, background="#ffffff", foreground="#000000")

        self.calendar2 = tk.Text(self.calendarFrame, width=1, bd=32, relief=tk.FLAT, font=("Consolas", 15), bg="#e1e1e1", insertbackground="#e1e1e1")
        self.calendar2.tag_configure(tk.SEL, background="#e1e1e1", foreground="#000000")

        self.annual_calendar = tk.Text(self.root, width=1, bd=32, relief=tk.FLAT, font=("Consolas", 12), bg="#ffffff", insertbackground="#ffffff")
        self.annual_calendar.tag_configure(tk.SEL, background="#ffffff", foreground="#000000")

        self.now()

        self.label_today = tk.Label(self.toolbar, text=datetime.datetime.now().date(), width=20, anchor="w")
        self.clock = tk.Label(self.root, relief=tk.FLAT, font=("Segoe UI", 60), bg="#e1e1e1")
        self.label_week = tk.Label(self.toolbar, text="Week " + str(int(datetime.datetime.now().isocalendar().week)), width=20, anchor="e")

        self.button_ics_1 = tk.Button(self.toolbar, bd=0, width=8, text="Open", command=self.open_ics)
        self.button_ics_2 = tk.Button(self.toolbar, bd=0, width=8, text="Close", command=self.close_ics)
        self.button_ics_3 = tk.Button(self.toolbar, bd=0, width=8, text="<<", command=self.previous_ics_event)
        self.button_ics_4 = tk.Button(self.toolbar, bd=0, width=8, text=">>", command=self.next_ics_event)

        self.icsFrame = tk.Frame(self.root)
        self.icsFrame.rowconfigure(1, weight=1)
        self.icsFrame.columnconfigure(0, weight=1)

        self.ics_label = tk.Label(self.icsFrame, bd=0, font=("Segoe UI", 12))
        self.ics_label.grid(row=0, column=0, sticky="nsew", pady=(0, 5))

        self.ics_treeview = ttk.Treeview(self.icsFrame, columns=("key", "value"), show="")
        self.ics_treeview.grid(row=1, column=0, sticky="nsew")

        self.menu_B3 = tk.Menu(self.root, tearoff=False, activeborderwidth=2.5)
        self.menu_B3.add_checkbutton(label="Pin Window", command=lambda: (self.root.attributes("-topmost", not self.root.attributes("-topmost")), self.root.overrideredirect(not self.root.overrideredirect()), self.restore_dark_mode()))
        self.menu_B3.add_command(label="Switch Theme", command=self.switch_theme)
        self.menu_B3.add_separator()
        self.menu_B3.add_command(label="Today", command=lambda: (self.now(), self.go_to_calendar()))
        self.menu_B3.add_command(label="Help", command=self.help_window)

        self.switch_theme()

        self.root.bind("<Button-3>", lambda event: self.menu_B3.tk_popup(event.x_root, event.y_root))
        self.root.bind("<Control-t>", lambda event: self.switch_theme())
        self.root.bind("<Control-T>", lambda event: self.switch_theme())
        self.root.bind("<F1>", lambda event: self.help_window())

        self.set_function(0)
        self.refresh()
        self.root.mainloop()

    def set_function(self, num):
        for widget in [self.button_previous_y, self.button_previous_m, self.button_next_m, self.button_next_y, self.calendarFrame, self.calendar2, self.annual_calendar, self.button_ics_1, self.button_ics_2, self.button_ics_3, self.button_ics_4, self.icsFrame, self.label_today, self.label_week, self.clock]:
            widget.grid_forget()
        self.root.unbind("<Control-Left>")
        self.root.unbind("<Control-Right>")
        self.root.unbind("<Alt-Left>")
        self.root.unbind("<Alt-Right>")
        if num == 0 or num == 1:
            self.button_previous_y.configure(width=5)
            self.button_previous_y.grid(row=0, column=0, sticky="nsw")
            self.button_previous_m.grid(row=0, column=1, sticky="nsw")
            self.button_next_m.grid(row=0, column=3, sticky="nse")
            self.button_next_y.configure(width=5)
            self.button_next_y.grid(row=0, column=4, sticky="nse")
            self.root.bind("<Control-Left>", lambda event: self.previous_year())
            self.root.bind("<Control-Right>", lambda event: self.next_year())
            self.root.bind("<Alt-Left>", lambda event: self.previous_month())
            self.root.bind("<Alt-Right>", lambda event: self.next_month())
        if num == 0:
            self.root.geometry("290x285")
            self.main_menubutton.configure(text="Calendar")
            self.calendarFrame.grid(row=1, column=0, sticky="nsew")
            self.calendarFrame.columnconfigure(1, weight=0)
        elif num == 1:
            self.root.geometry("580x285")
            self.main_menubutton.configure(text="Dual Calendar")
            self.calendarFrame.grid(row=1, column=0, sticky="nsew")
            self.calendar2.grid(row=0, column=1, sticky="nsew")
            self.calendarFrame.columnconfigure(1, weight=1)
        elif num == 2:
            self.root.geometry("716x800")
            self.button_previous_y.configure(width=8)
            self.button_previous_y.grid(row=0, column=0, sticky="nsw")
            self.button_next_y.configure(width=8)
            self.button_next_y.grid(row=0, column=4, sticky="nse")
            self.root.bind("<Control-Left>", lambda event: self.previous_year())
            self.root.bind("<Control-Right>", lambda event: self.next_year())
            self.main_menubutton.configure(text="Annual Calendar")
            self.annual_calendar.grid(row=1, column=0, sticky="nsew")
        elif num == 3:
            self.root.geometry("580x400")
            self.root.resizable(width=False, height=True)
            self.main_menubutton.configure(text="Events")
            self.button_ics_1.grid(row=0, column=0, sticky="nsw")
            self.button_ics_2.grid(row=0, column=1, sticky="nsw")
            self.button_ics_3.grid(row=0, column=3, sticky="nse")
            self.button_ics_4.grid(row=0, column=4, sticky="nse")
            self.icsFrame.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)
        elif num == 4:
            self.root.geometry("435x285")
            self.label_today.grid(row=0, column=0, sticky="nsw", padx=(10, 0))
            self.label_week.grid(row=0, column=4, sticky="nse", padx=(0, 10))
            self.main_menubutton.configure(text="Clock")
            self.clock.grid(row=1, column=0, sticky="nsew")
        if num != 3:
            self.root.resizable(width=False, height=False)
        self.restore_dark_mode()

    def get_calendars(self):
        self.calendar1.configure(state=tk.NORMAL)
        self.calendar1.delete(1.0, tk.END)
        self.calendar1.insert(1.0, calendar.month(self.y, self.m))
        self.calendar1.configure(state=tk.DISABLED)
        self.calendar2.configure(state=tk.NORMAL)
        self.calendar2.delete(1.0, tk.END)
        if self.m == 12:
            self.calendar2.insert(1.0, calendar.month(self.y + 1, 1))
        else:
            self.calendar2.insert(1.0, calendar.month(self.y, self.m + 1))
        self.calendar2.configure(state=tk.DISABLED)
        self.annual_calendar.configure(state=tk.NORMAL)
        self.annual_calendar.delete(1.0, tk.END)
        self.annual_calendar.insert(1.0, calendar.calendar(self.y))
        self.annual_calendar.configure(state=tk.DISABLED)

    def previous_month(self):
        if self.m == 1:
            self.y -= 1
            self.m = 12
        else:
            self.m -= 1
        self.get_calendars()

    def next_month(self):
        if self.m == 12:
            self.y += 1
            self.m = 1
        else:
            self.m += 1
        self.get_calendars()

    def now(self):
        self.y = datetime.datetime.now().year
        self.m = datetime.datetime.now().month
        self.get_calendars()

    def go_to_calendar(self):
        if self.function.get() not in (0, 1, 2):
            self.set_function(0)
            self.function.set(0)

    def previous_year(self):
        self.y -= 1
        self.get_calendars()

    def next_year(self):
        self.y += 1
        self.get_calendars()

    def refresh(self):
        self.clock.configure(text=f"{datetime.datetime.now().strftime('%H:%M:%S')}")
        self.root.after(250, self.refresh)

    def restore_dark_mode(self):
        try:
            if self.toolbar.cget("bg") == "#1C1C1C":
                ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(self.root.winfo_id()), 20, ct.byref(ct.c_int(2)), ct.sizeof(ct.c_int(2)))
        except:
            return

    def switch_theme(self):
        if self.toolbar.cget("background") == "#F0F0F0":
            bg, bg2, bg3, bg4, fg = "#202020", "#1C1C1C", "#2B2B2B", "#5C5C5C", "#FFFFFF"
            var = 2
        else:
            bg, bg2, bg3, bg4, fg = "#FFFFFF", "#F0F0F0", "#E1E1E1", "#D2D2D2", "#000000"
            var = 0
        try:
            ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(self.root.winfo_id()), 20, ct.byref(ct.c_int(var)), ct.sizeof(ct.c_int(var)))
        except:
            return
        self.root["background"] = bg
        self.toolbar.configure(background=bg2)
        for widget in [self.label_today, self.label_week]:
            widget.configure(background=bg2, foreground=fg)
        self.style.configure("TMenubutton", background=bg2, foreground=fg)
        self.style.configure("Treeview", background=bg, foreground=fg)
        self.main_menu.configure(background=bg2, foreground=fg, selectcolor=fg, activebackground=bg3, activeforeground=fg)
        self.menu_B3.configure(background=bg2, foreground=fg, selectcolor=fg, activebackground=bg3, activeforeground=fg)
        for widget in [self.icsFrame, self.clock]:
            widget.configure(background=bg)
        for widget in [self.ics_label, self.calendar1, self.annual_calendar, self.clock]:
            widget.configure(background=bg, foreground=fg)
        self.calendar2.configure(background=bg3, foreground=fg)
        self.calendar1.tag_configure(tk.SEL, background=bg, foreground=fg)
        self.calendar2.tag_configure(tk.SEL, background=bg3, foreground=fg)
        for widget in [self.button_previous_y, self.button_previous_m, self.button_next_m, self.button_next_y, self.button_ics_1, self.button_ics_2, self.button_ics_3, self.button_ics_4]:
            widget.configure(background=bg2, foreground=fg, activebackground=bg4, activeforeground=fg)
            widget.unbind("<Enter>")
            widget.unbind("<Leave>")
            widget.bind("<Enter>", lambda event, button=widget: button.configure(bg=bg3, fg=fg))
            widget.bind("<Leave>", lambda event, button=widget: button.configure(bg=bg2, fg=fg))

    def parse_ics(self, file_path):
        events = []
        event = {}
        inside_event = False

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "BEGIN:VEVENT":
                    inside_event = True
                    event = {}
                elif line == "END:VEVENT":
                    inside_event = False
                    events.append(event)
                elif inside_event:
                    if ":" not in line:
                        continue
                    key, value = line.split(":", 1)
                    key = key.split(";")[0]
                    if key in ("DTSTART", "DTEND"):
                        try:
                            if value.endswith("Z"):
                                value = datetime.datetime.strptime(value, "%Y%m%dT%H%M%SZ")
                            else:
                                value = datetime.datetime.strptime(value, "%Y%m%dT%H%M%S")
                        except:
                            pass
                    event[key] = value
        return events

    def fill_ics_treeview(self, event):
        self.ics_treeview.delete(*self.ics_treeview.get_children())
        for k, v in event.items():
            self.ics_treeview.insert("", "end", values=(k, v))

    def open_ics(self):
        path = filedialog.askopenfilename(filetypes=[("All Supported File Types", "*.ics *.ical *.icalendar *.ifb *.vcs"), ("iCalendar Files", "*.ics *.ical *.icalendar *.ifb"), ("vCalendar Files", "*.vcs")])
        if not path:
            return
        self.ics_events = self.parse_ics(path)
        self.ics_index = 0
        if not self.ics_events:
            return
        self.fill_ics_treeview(self.ics_events[self.ics_index])
        self.ics_label.configure(text=f"Event {self.ics_index + 1}/{len(self.ics_events)}")

    def close_ics(self):
        self.ics_treeview.delete(*self.ics_treeview.get_children())
        self.ics_label.configure(text="")

    def previous_ics_event(self):
        if not self.ics_events:
            return
        self.ics_index = max(0, self.ics_index - 1)
        self.ics_label.configure(text=f"Event {self.ics_index + 1}/{len(self.ics_events)}")
        self.fill_ics_treeview(self.ics_events[self.ics_index])

    def next_ics_event(self):
        if not self.ics_events:
            return
        self.ics_index = min(len(self.ics_events) - 1, self.ics_index + 1)
        self.ics_label.configure(text=f"Event {self.ics_index + 1}/{len(self.ics_events)}")
        self.fill_ics_treeview(self.ics_events[self.ics_index])

    def help_window(self):
        window = tk.Toplevel()
        try:
            window.iconbitmap("icon.ico")
        except:
            pass
        window.title("Help - Calendar4pc")
        window.geometry("700x510")
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        help_tabs = ttk.Notebook(window)
        help_tabs.grid(row=0, column=0, sticky="nsew")
        about = tk.Text(help_tabs, relief=tk.FLAT, border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap=tk.WORD, background="#CCCCCC")
        about.insert(tk.INSERT, f"Calendar4pc\nCopyright (c) 2025-{str(datetime.datetime.now().year)}: Waylon Boer\n\nCalendar4pc is a calendar app with multiple lay-outs.")
        about.configure(state=tk.DISABLED)
        help_tabs.add(about, text="About")
        mit_license = tk.Text(help_tabs, relief=tk.FLAT, border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap=tk.WORD, background="#CCCCCC")
        mit_license.insert(tk.INSERT, """MIT License

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
        mit_license.configure(state=tk.DISABLED)
        help_tabs.add(mit_license, text="License")

Calendar4pc()
