# ---- group2 -----------

from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from datetime import time
import sqlite3


conn = sqlite3.connect("ListDatabase.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON")
cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS student (ID_Number VARCHAR(8) PRIMARY KEY,"
            "Full_Name VARCHAR(30), Year_Level VARCHAR(10), Course_Code TEXT,"
            "FOREIGN KEY (Course_Code) REFERENCES courses(Course_Code)"
            "   ON UPDATE CASCADE"
            "   ON DELETE CASCADE)")
cur.execute("CREATE TABLE IF NOT EXISTS EVENT(Event_Code TEXT PRIMARY KEY, Location TEXT,"
            "Event_Date DATE, Start_time DATE, End_Time DATE)")
cur.execute("CREATE TABLE IF NOT EXISTS ATTENDANCE(Event_Code TEXT, ID_Number VARCHAR(8),"
            "Time_In TIME NOT NULL, Time_Out TIME,"
            "PRIMARY KEY(Event_Code, ID_Number),"
            "FOREIGN KEY (Event_Code) REFERENCES EVENT(Event_Code)"
            "   ON UPDATE CASCADE"
            "   ON DELETE CASCADE,"
            "FOREIGN KEY (ID_Number) REFERENCES student(ID_Number)"
            "   ON DELETE CASCADE "
            "   ON UPDATE CASCADE)")


def get_cur_date():
    return datetime.now().strftime("%x")


def get_curtime():
    return datetime.now().strftime("%X")


def conv_strtime_to_time(strtime):
    return time.fromisoformat(strtime)


def timemargin(gtime):
    hour = int(gtime.strftime("%H"))
    mins = int(gtime.strftime("%M"))
    if mins - 30 < 0:
        adv = time(hour-1, 60+(mins-30)).strftime("%X")
    else:
        adv = time(hour, mins-30).strftime("%X")
    if mins + 30 >= 60:
        cut = time(hour+1, (mins+30)-60).strftime("%X")
    else:
        cut = time(hour, mins+30).strftime("%X")
    return [adv, cut]


def toexit(app):
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        app.destroy()
    else:
        return


class App:
    def __init__(self, app):
        app.title("E-Attendance System")
        app_width = 1000
        app_height = 650
        app.geometry("{}x{}+{}+{}".format(app_width, app_height, int((app.winfo_screenwidth() - app_width)/2),
                                          int((app.winfo_screenheight()-60 - app_height)/2)))
        app.resizable(False, False)
        app.config(bg="RosyBrown3")

        Label(app, text="E-ATTENDANCE SYSTEM", font=("Bodoni MT", 40, "bold"), bg="RosyBrown3", fg="black")\
            .place(x=0, y=10, width=1000, height=60)

        navframe = Frame(app, bg="Mistyrose2")
        navframe.place(x=0, y=90, width=1000, height=30)
        self.eventsbtn = Button(navframe, relief=RAISED, text="EVENTS", font=("Bodoni MT", 14, "bold"),
                                command=lambda: [self.refresh(), self.event_frame()])
        self.eventsbtn.place(x=0, y=0, width=130, height=30)
        self.recordbtn = Button(navframe, relief=RAISED, text="ATTENDANCE RECORD", font=("Bodoni MT", 14, "bold"),
                                command=lambda: [self.refresh(), self.attend_frame()])
        self.recordbtn.place(x=130, y=0, width=230, height=30)
        self.coursebtn = Button(navframe, relief=RAISED, text="COURSE", font=("Bodoni MT", 14, "bold"),
                                command=lambda: [self.refresh(), self.course_frame()])
        self.coursebtn.place(x=360, y=0, width=130, height=30)
        self.studbtn = Button(navframe, relief=RAISED, text="STUDENTS", font=("Bodoni MT", 14, "bold"),
                              command=lambda: [self.refresh(), self.stud_frame()])
        self.studbtn.place(x=490, y=0, width=130, height=30)

        self.recordframe = Frame(app, bg="Mistyrose2")
        self.eventframe = Frame(app, bg="Mistyrose2")
        self.courseframe = Frame(app, bg="Mistyrose2")
        self.studframe = Frame(app, bg="Mistyrose2")

        self.refresh(), self.event_frame()

        app.protocol("WM_DELETE_WINDOW", lambda x=app: toexit(x))

    def refresh(self):
        self.recordbtn.config(fg="Gray10", bg="Mistyrose2", activebackground="RosyBrown3", activeforeground="Gray10")
        self.eventsbtn.config(fg="Gray10", bg="Mistyrose2", activebackground="RosyBrown3", activeforeground="Gray10")
        self.coursebtn.config(fg="Gray10", bg="Mistyrose2", activebackground="RosyBrown3", activeforeground="Gray10")
        self.studbtn.config(fg="Gray10", bg="Mistyrose2", activebackground="RosyBrown3", activeforeground="Gray10")
        self.recordframe.place_forget()
        self.eventframe.place_forget()
        self.courseframe.place_forget()
        self.studframe.place_forget()

    def attend_frame(self):
        self.recordbtn.config(activeforeground="Gray10", activebackground="Mistyrose2", bg="RosyBrown3", fg="Gray10")
        self.recordframe.place(x=0, y=130, width=1000, height=520)
        AttendanceRecord(self.recordframe)

    def event_frame(self):
        self.eventsbtn.config(activeforeground="Gray10", activebackground="Mistyrose2", bg="RosyBrown3", fg="Gray10")
        self.eventframe.place(x=0, y=130, width=1000, height=520)
        Events(self.eventframe)

    def course_frame(self):
        self.coursebtn.config(activeforeground="Gray10", activebackground="Mistyrose2", bg="RosyBrown3", fg="Gray10")
        self.courseframe.place(x=0, y=130, width=1000, height=520)
        Courses(self.courseframe)

    def stud_frame(self):
        self.studbtn.config(activeforeground="Gray10", activebackground="Mistyrose2", bg="RosyBrown3", fg="Gray10")
        self.studframe.place(x=0, y=130, width=1000, height=520)
        Students(self.studframe)


def eventlist():
    ev = ["All"]
    cur.execute("SELECT Event_Code FROM EVENT")
    res = cur.fetchall()
    if res:
        for e in res:
            ev.append(e[0])
        return ev
    else:
        return []


class AttendanceRecord:
    def __init__(self, frame):
        self.ev_code = StringVar()
        self.ev_code.set("All")

        Label(frame, text="Event   Code: ", fg="Gray10", bg="Mistyrose2", font=("Blinker", 12, "bold"), anchor="e").\
            place(x=30, y=35, height=25, width=90)
        evs = ttk.Combobox(frame, textvariable=self.ev_code, font=("Bodoni MT", 12, "bold"), values=eventlist())
        self.ev_code.trace("w", lambda name, index, mode, sv=self.ev_code: self.displayrecord())
        listframe = Frame(frame, bg="white")
        listframe.place(x=30, y=80, width=940, height=420)
        evs.place(x=120, y=35, height=25, width=200)

        self.recordlist = ttk.Treeview(listframe, columns=("evcode", "evdate", "sid", "sname", "syearcourse",
                                                           "timein", "timeout"))

        ry = Scrollbar(listframe, orient=VERTICAL)
        ry.config(command=self.recordlist.yview)
        ry.pack(side=RIGHT, fill=Y)
        self.recordlist.config(yscrollcommand=ry.set)
        self.recordlist.heading("evcode", text="Event Code")
        self.recordlist.heading("evdate", text="Event Date")
        self.recordlist.heading("sid", text="ID Number")
        self.recordlist.heading("sname", text="Name")
        self.recordlist.heading("syearcourse", text="Course & Year")
        self.recordlist.heading("timein", text="Time In")
        self.recordlist.heading("timeout", text="Time Out")
        self.recordlist['show'] = 'headings'
        self.recordlist.column("evcode", width=145, anchor="center")
        self.recordlist.column("evdate", width=70, anchor="center")
        self.recordlist.column("sid", width=80, anchor="center")
        self.recordlist.column("sname", width=350, anchor="w")
        self.recordlist.column("syearcourse", width=145, anchor="center")
        self.recordlist.column("timein", width=65, anchor="center")
        self.recordlist.column("timeout", width=65, anchor="center")
        self.recordlist.pack(fill=BOTH, expand=1)

        self.displayrecord()

    def displayrecord(self):
        self.recordlist.delete(*self.recordlist.get_children())
        if self.ev_code.get() == "All" or self.ev_code.get() == "":
            cur.execute("SELECT * FROM ATTENDANCE")
        else:
            cur.execute("SELECT * FROM ATTENDANCE WHERE Event_Code=?", (self.ev_code.get(),))
        rec = cur.fetchall()
        if not rec:
            return
        else:
            for r in rec:
                cur.execute("SELECT * FROM student WHERE ID_Number=?", (r[1],))
                s = cur.fetchone()
                cur.execute("SELECT Event_Date FROM EVENT WHERE Event_Code=?", (r[0],))
                d = cur.fetchone()[0]
                tout = r[3]
                if tout is not None:
                    tout = conv_strtime_to_time(tout).strftime('%I:%M %p')
                self.recordlist.insert('', END, values=(r[0], d, r[1], s[1], (s[3] + " (" + s[2] + ")"),
                                                        conv_strtime_to_time(r[2]).strftime('%I:%M %p'), tout))


class Events:
    def __init__(self, frame):
        self.searchevcode = StringVar()
        self.keyev = StringVar()
        self.eventcode = StringVar()
        self.loc = StringVar()
        self.shour = IntVar()
        self.smin = IntVar()
        self.ehour = IntVar()
        self.emin = IntVar()

        Label(frame, text="Event   Code: ", fg="Gray10", bg="Mistyrose2", font=("Blinker", 12, "bold"), anchor="e").\
            place(x=490, y=20, height=30, width=150)
        Entry(frame, textvariable=self.searchevcode, font=("Roboto", 12)).place(x=640, y=20, height=30, width=250)
        Label(frame, text="SEARCH", font=("Blinker", 12, "bold"), fg="Gray10", bg="Rosybrown3", relief=RAISED).\
            place(x=890, y=20, height=30, width=80)
        self.searchevcode.trace("w", lambda name, index, mode, sv=self.searchevcode: self.searchevent())

        evfr = Frame(frame)
        evfr.place(x=30, y=80, width=940, height=420)
        evcanvas = Canvas(evfr, width=940, height=410)
        self.evframe = Frame(evcanvas)
        y = Scrollbar(evfr, orient=VERTICAL, command=evcanvas.yview)
        y.pack(side=RIGHT, fill=Y)
        evcanvas.pack(side=LEFT)
        evcanvas.bind('<Configure>', lambda e: evcanvas.configure(scrollregion=evcanvas.bbox('all')))
        evcanvas.configure(yscrollcommand=y.set)
        evcanvas.create_window((0, 0), window=self.evframe, anchor="nw")

        addeventbtn = Button(frame, text="ADD EVENT", font=("Blinker", 12, "bold"), command=self.addeventframe,
                             activebackground="Mistyrose2", fg="Gray10", bg="Rosybrown3", activeforeground="Gray10")
        addeventbtn.place(x=30, y=20, height=30, width=130)

        self.searchevent()
        self.clear()

    def addeventframe(self):
        self.addevframe = Toplevel()
        self.addevframe.title("Add Event")
        self.addevframe.resizable(False, False)
        width = 435
        height = 320
        self.clear()
        self.addevframe.geometry("{}x{}+{}+{}".format(width, height,
                                                      int((self.addevframe.winfo_screenwidth() - width) / 2),
                                                      int((self.addevframe.winfo_screenheight() - 60 - height) / 2)))
        self.addevframe.config(bg="Rosybrown3")
        self.addevframe.grab_set()

        head = Label(self.addevframe, text="ADD EVENT", fg="Gray10", bg="Rosybrown3", font=("Bodoni MT", 16, "bold"))
        head.place(x=5, y=10, width=440, height=30)

        levcode = Label(self.addevframe, text=" EVENT CODE: ", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                        anchor="w")
        eevcode = Entry(self.addevframe, textvariable=self.eventcode, font=("Roboto", 12, "bold"))
        levloc = Label(self.addevframe, text=" LOCATION: ", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                       anchor="w")
        eevloc = Entry(self.addevframe, textvariable=self.loc, font=("Roboto", 12, "bold"))
        levdate = Label(self.addevframe, text=" DATE: ", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                        anchor="w")
        self.ev_date = DateEntry(self.addevframe, background="gray", foreground="snow", date_pattern='mm/dd/yy')
        lstarttime = Label(self.addevframe, text=" START TIME: ", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                           anchor="w")
        starthour = Spinbox(self.addevframe, from_=0, to_=23,  background="white", foreground="black",
                            textvariable=self.shour, font=("Bodoni MT", 13,))
        Label(self.addevframe, text=":", bg="Rosybrown3", fg="Gray10", font=("Bodoni MT", 20, "bold"), anchor="center")\
            .place(x=170, y=177, height=35, width=10)
        startmin = Spinbox(self.addevframe, from_=0, to_=59,  background="white", foreground="black",
                           textvariable=self.smin, font=("Bodoni MT", 13,))
        Label(self.addevframe, text="(24-Hour Format)", bg="Rosybrown3", fg="Gray10", font=("Bodoni MT", 11),
              anchor="center").place(x=225, y=180, height=35)
        lendtime = Label(self.addevframe, text=" END TIME: ",  fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                         anchor="w")
        Label(self.addevframe, text=":", bg="Rosybrown3", fg="Gray10", font=("Bodoni MT", 20, "bold"), anchor="center")\
            .place(x=170, y=217, height=35, width=10)
        ehour = Spinbox(self.addevframe, from_=0, to_=23, textvariable=self.ehour, font=("Bodoni MT", 13,),
                        background="white", foreground="black")
        emin = Spinbox(self.addevframe, from_=0, to_=59, background="white", foreground="black", textvariable=self.emin,
                       font=("Bodoni MT", 13,))
        Label(self.addevframe, text="(24-Hour Format)", bg="Rosybrown3", fg="Gray10", font=("Bodoni MT", 11),
              anchor="center").place(x=225, y=220, height=35)

        levcode.place(x=10, y=60, width=120, height=35)
        eevcode.place(x=130, y=60, width=295, height=35)
        levloc.place(x=10, y=100, width=120, height=35)
        eevloc.place(x=130, y=100, width=295, height=35)
        levdate.place(x=10, y=140, width=120, height=35)
        self.ev_date.place(x=130, y=140, width=295, height=35)
        lstarttime.place(x=10, y=180, width=120, height=35)
        starthour.place(x=130, y=180, width=40, height=35)
        startmin.place(x=180, y=180, width=40, height=35)
        lendtime.place(x=10, y=220, width=120, height=35)
        ehour.place(x=130, y=220, width=40, height=35)
        emin.place(x=180, y=220, width=40, height=35)

        addevbtn = Button(self.addevframe, text="ADD", font=("Blinker", 12, "bold"), command=self.addevent,
                          activebackground="Mistyrose2", fg="Gray10", bg="Mistyrose2", activeforeground="Gray10")
        clearevbtn = Button(self.addevframe, text="CLEAR", font=("Blinker", 12, "bold"), command=self.clear,
                            activebackground="Mistyrose2", fg="Gray10", bg="Mistyrose2", activeforeground="Gray10")
        addevbtn.place(width=100, height=30, y=275, x=220)
        clearevbtn.place(width=100, height=30, y=275, x=325)

    def addevent(self):
        if self.loc.get() == "" or self.eventcode.get() == "":
            messagebox.showerror("Error", "Please fill out all fields")
            return
        elif get_cur_date() > self.ev_date.get():
            messagebox.showerror("Error", "Invalid event date!")
            return
        else:
            try:
                starttime = time(int(self.shour.get()), int(self.smin.get())).strftime("%X")
                endtime = time(int(self.ehour.get()), int(self.emin.get())).strftime("%X")
                if self.ev_date.get() == get_cur_date() and (starttime > endtime or starttime < get_curtime()
                                                             or endtime < get_curtime()):
                    messagebox.showerror("Error", "Invalid time provided!")
                    return

                if messagebox.askyesno("Add Event", "Confirm adding event?"):
                    try:
                        cur.execute("INSERT INTO EVENT VALUES (?, ?, ?, ?, ?)", (self.eventcode.get(), self.loc.get(),
                                                                                 self.ev_date.get(), starttime,
                                                                                 endtime))
                        conn.commit()
                        messagebox.showinfo("Success", "Event added successfully")
                        self.addevframe.destroy()
                        self.clear()
                        self.searchevent()
                    except sqlite3.IntegrityError:
                        messagebox.showerror("Error", "Event code already in database!")
            except ValueError:
                messagebox.showerror("Error", "Invalid time provided!")
                return

    def updateevframe(self, event):
        self.keyev.set(event[0])
        self.updevframe = Toplevel()
        self.updevframe.title("Add Event")
        self.updevframe.resizable(False, False)
        width = 435
        height = 320
        self.updevframe.geometry("{}x{}+{}+{}".format(width, height,
                                                      int((self.updevframe.winfo_screenwidth() - width) / 2),
                                                      int((self.updevframe.winfo_screenheight() -
                                                           60 - height) / 2)))
        self.updevframe.config(bg="Rosybrown3")
        self.updevframe.grab_set()
        self.clear()
        stime = conv_strtime_to_time(event[3])
        etime = conv_strtime_to_time(event[4])
        self.eventcode.set(event[0])
        self.loc.set(event[1])
        self.shour.set(stime.strftime("%H"))
        self.smin.set(stime.strftime("%M"))
        self.ehour.set(etime.strftime("%H"))
        self.emin.set(etime.strftime("%M"))

        head = Label(self.updevframe, text="UPDATE EVENT DETAILS", fg="Gray10", bg="Rosybrown3",
                     font=("Bodoni MT", 16, "bold"))
        head.place(x=5, y=10, width=440, height=30)

        levcode = Label(self.updevframe, text=" EVENT CODE: ", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                        anchor="w")
        eevcode = Entry(self.updevframe, textvariable=self.eventcode, font=("Roboto", 12, "bold"))
        levloc = Label(self.updevframe, text=" LOCATION: ", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                       anchor="w")
        eevloc = Entry(self.updevframe, textvariable=self.loc, font=("Roboto", 12, "bold"))
        levdate = Label(self.updevframe, text=" DATE: ", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                        anchor="w")
        self.ev_date = DateEntry(self.updevframe, background="gray", foreground="snow", date_pattern='mm/dd/yy')
        lstarttime = Label(self.updevframe, text=" START TIME: ", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                           anchor="w")
        starthour = Spinbox(self.updevframe, from_=0, to_=23, background="white", foreground="black",
                            textvariable=self.shour, font=("Bodoni MT", 13,))
        Label(self.updevframe, text=":", bg="Rosybrown3", fg="Gray10", font=("Bodoni MT", 20, "bold"), anchor="center")\
            .place(x=170, y=177, height=35, width=10)
        startmin = Spinbox(self.updevframe, from_=0, to_=59, background="white", foreground="black",
                           textvariable=self.smin, font=("Bodoni MT", 13,))
        Label(self.updevframe, text="(24-Hour Format)", bg="Rosybrown3", fg="Gray10", font=("Bodoni MT", 11),
              anchor="center").place(x=225, y=180, height=35)
        lendtime = Label(self.updevframe, text=" END TIME: ", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                         anchor="w")
        Label(self.updevframe, text=":", bg="Rosybrown3", fg="Gray10", font=("Bodoni MT", 20, "bold"), anchor="center")\
            .place(x=170, y=217, height=35, width=10)
        ehour = Spinbox(self.updevframe, from_=0, to_=23, textvariable=self.ehour, font=("Bodoni MT", 13,),
                        background="white", foreground="black")
        emin = Spinbox(self.updevframe, from_=0, to_=59, background="white", foreground="black", textvariable=self.emin,
                       font=("Bodoni MT", 13,))
        Label(self.updevframe, text="(24-Hour Format)", bg="Rosybrown3", fg="Gray10", font=("Bodoni MT", 11),
              anchor="center").place(x=225, y=220, height=35)

        self.ev_date.set_date(event[2])

        levcode.place(x=10, y=60, width=120, height=35)
        eevcode.place(x=130, y=60, width=295, height=35)
        levloc.place(x=10, y=100, width=120, height=35)
        eevloc.place(x=130, y=100, width=295, height=35)
        levdate.place(x=10, y=140, width=120, height=35)
        self.ev_date.place(x=130, y=140, width=295, height=35)
        lstarttime.place(x=10, y=180, width=120, height=35)
        starthour.place(x=130, y=180, width=40, height=35)
        startmin.place(x=180, y=180, width=40, height=35)
        lendtime.place(x=10, y=220, width=120, height=35)
        ehour.place(x=130, y=220, width=40, height=35)
        emin.place(x=180, y=220, width=40, height=35)

        updevbtn = Button(self.updevframe, text="UPDATE", font=("Blinker", 12, "bold"), command=self.updateevent,
                          activebackground="Mistyrose2", fg="Gray10", bg="Mistyrose2", activeforeground="Gray10")
        clearevbtn = Button(self.updevframe, text="CLEAR", font=("Blinker", 12, "bold"), command=self.clear,
                            activebackground="Mistyrose2", fg="Gray10", bg="Mistyrose2", activeforeground="Gray10")
        updevbtn.place(width=100, height=30, y=275, x=220)
        clearevbtn.place(width=100, height=30, y=275, x=325)

    def updateevent(self):
        if self.loc.get() == "" or self.eventcode.get() == "":
            messagebox.showerror("Error", "Please fill out all fields")
            return
        elif get_cur_date() > self.ev_date.get():
            messagebox.showerror("Error", "Invalid event date!")
            return
        else:
            try:
                starttime = time(self.shour.get(), self.smin.get()).strftime("%X")
                endtime = time(self.ehour.get(), self.emin.get()).strftime("%X")
                if self.ev_date.get() == get_cur_date() and (starttime > endtime or starttime < get_curtime()
                                                             or endtime < get_curtime()):
                    messagebox.showerror("Error", "Invalid time provided!")
                    return

                if messagebox.askyesno("Update Event Details", "Confirm updating event details?"):
                    try:
                        if self.keyev.get() != self.eventcode.get():
                            cur.execute("UPDATE EVENT SET Event_Code=?, Location=?, Event_Date=?, Start_time=?, "
                                        "End_time=? WHERE Event_Code=?",
                                        (self.eventcode.get(), self.loc.get(), self.ev_date.get(), starttime, endtime,
                                         self.keyev.get()))
                        else:
                            cur.execute("UPDATE EVENT SET Location=?, Event_Date=?, Start_time=?, End_time=? "
                                        "WHERE Event_Code=?",
                                        (self.loc.get(), self.ev_date.get(), starttime, endtime, self.eventcode.get()))
                        conn.commit()
                        self.keyev.set("")
                        messagebox.showinfo("Success", "Event details updated!")
                        self.updevframe.destroy()
                        self.clear()
                        self.searchevent()
                    except sqlite3.IntegrityError:
                        messagebox.showerror("Error", "Event already in database")
                        return
            except ValueError:
                messagebox.showerror("Error", "Invalid time provided!")
                return

    def searchevent(self):
        if self.searchevcode.get() == "":
            cur.execute("SELECT * FROM EVENT")
        else:
            cur.execute("SELECT * FROM EVENT WHERE Event_Code LIKE ?", ('%' + self.searchevcode.get() + '%',))
        events = cur.fetchall()
        for frame in self.evframe.winfo_children():
            frame.destroy()
        row = 0
        if not events:
            noevfr = Frame(self.evframe, bg="white", width=930, height=420)
            noevfr.propagate(0)
            noevfr.grid(row=0, column=0)
            noev = Label(noevfr, text="Add Events", font=('Bodoni MT', 60, 'bold'), fg="Rosybrown3", bg="white")
            noev.place(x=0, y=0, width=940, height=390)
        else:
            for event in events:
                evframe = Frame(self.evframe, highlightbackground="black", highlightthickness=1, height=80, width=910,
                                bg="Rosybrown3")
                evframe.propagate(0)
                evframe.grid(row=row, column=0, padx=5, pady=(5, 0))
                labels = Frame(evframe, bg="Rosybrown3")
                labels.place(x=0, y=0, height=78, width=450)
                Label(labels, text=event[0], font=('Bodoni MT', 27, 'bold'), bg="Rosybrown3").\
                    place(x=10, y=5, height=40)
                Label(labels, text=(event[1] + " | " + event[2]),
                      font=('Bodoni MT', 12, 'bold'), bg="Rosybrown3").place(x=10, y=43, height=30)
                buttons = Frame(evframe, bg="Rosybrown3")
                buttons.place(width=265, x=630, y=0, height=78)
                update = Button(buttons, text="Update Details", font=("Blinker", 12, "bold"), fg="Gray10",
                                bg="Mistyrose2", activebackground="Rosybrown3", activeforeground="Gray10",
                                command=lambda x=event: self.updateevframe(x))
                update.place(x=10, y=5, height=30, width=120)
                delete = Button(buttons, text="Delete Event", font=("Blinker", 12, "bold"), fg="Gray10",
                                bg="Mistyrose2", activebackground="Rosybrown3", activeforeground="Gray10",
                                command=lambda x=event: self.delete_event(x))
                delete.place(x=140, y=5, height=30, width=120)
                attend = Button(buttons, text="Check Attendance", font=("Blinker", 12, "bold"), fg="Gray10",
                                bg="Mistyrose2", activebackground="Rosybrown3", activeforeground="Gray10",
                                command=lambda x=event: Attendance(x))
                attend.place(x=10, y=43, height=30, width=250)
                stime = conv_strtime_to_time(event[3])
                etime = conv_strtime_to_time(event[4])

                if get_cur_date() > event[2] or (get_cur_date() == event[2] and get_curtime() > timemargin(etime)[1]):
                    update.config(state=DISABLED)
                    delete.config(state=DISABLED)
                    attend.config(state=DISABLED)
                    Label(buttons, text="EVENT FINISHED!", font=('Bodoni MT', 20, 'bold'), bg="white", fg="green").\
                        place(x=15, y=19, height=40, width=240)
                elif get_curtime() < timemargin(stime)[0]:
                    attend.config(state=DISABLED)
                elif get_cur_date() < event[2]:
                    attend.config(state=DISABLED)
                elif get_cur_date() == event[2] and get_curtime() > stime.strftime("%X"):
                    update.config(state=DISABLED)
                    delete.config(state=DISABLED)

                row += 1

    def delete_event(self, event):
        if messagebox.askyesno("Delete Event", "Confirm deleting event?"):
            cur.execute("DELETE FROM EVENT WHERE Event_Code=?", (event[0],))
            messagebox.showinfo("Success", "Event deleted from database!")
            conn.commit()
            self.searchevent()

    def clear(self):
        self.eventcode.set("")
        self.loc.set("")
        self.shour.set(0)
        self.smin.set(0)
        self.ehour.set(0)
        self.emin.set(0)


class Courses:
    def __init__(self, frame):
        self.coursecode = StringVar()
        self.searchcode = StringVar()
        self.key = StringVar()

        listframe = Frame(frame)
        listframe.place(x=30, y=60, width=940, height=440)
        y = Scrollbar(listframe, orient=VERTICAL)
        self.courselist = ttk.Treeview(listframe, columns=("c_code", "c_name"), yscrollcommand=y)
        y.pack(side=RIGHT, fill=Y)
        y.config(command=self.courselist.yview)
        self.courselist.heading("c_code", text="COURSE CODE")
        self.courselist.heading("c_name", text="COURSE NAME")
        self.courselist['show'] = 'headings'
        self.courselist.column("c_code", width=50, anchor="center")
        self.courselist.column("c_name", width=380)
        self.courselist.pack(fill=BOTH, expand=1)
        self.courselist.bind("<Double-1>", self.update_courseframe)

        addcoursebtn = Button(frame, text="ADD", font=("Blinker", 12, "bold"), command=self.add_course_frame,
                              activebackground="Mistyrose2", fg="Gray10", bg="Rosybrown3", activeforeground="Gray10")
        delcoursebtn = Button(frame, text="DELETE", font=("Blinker", 12, "bold"), command=self.deletecourse,
                              activebackground="Mistyrose2", fg="Gray10", bg="Rosybrown3", activeforeground="Gray10")
        addcoursebtn.place(x=30, y=20, height=30, width=80)
        delcoursebtn.place(x=115, y=20, height=30, width=80)

        search_lbl = Label(frame, text="Course   Code: ", fg="Gray10", bg="Mistyrose2", font=("Blinker", 12, "bold"),
                           anchor="e")
        search_ent = Entry(frame, textvariable=self.searchcode, font=("Roboto", 12))
        searchbtn = Label(frame, text="SEARCH", font=("Blinker", 12, "bold"), fg="Gray10", bg="Rosybrown3",
                          relief=RAISED)
        self.searchcode.trace("w", lambda name, index, mode, sv=self.searchcode: self.searchcourse())
        search_lbl.place(x=490, y=20, height=30, width=150)
        search_ent.place(x=640, y=20, height=30, width=250)
        searchbtn.place(x=890, y=20, height=30, width=80)

        self.searchcourse()

    def add_course_frame(self):
        self.addframe = Toplevel()
        self.addframe.title("Add Course")
        self.addframe.resizable(False, False)
        self.addframe.config(bg="Rosybrown3")
        width = 450
        height = 320
        self.addframe.geometry("{}x{}+{}+{}".format(width, height, int((self.addframe.winfo_screenwidth() - width) / 2),
                                                    int((self.addframe.winfo_screenheight() - 60 - height) / 2)))
        self.addframe.grab_set()

        head = Label(self.addframe, text="ADD COURSE", fg="Gray10", bg="Rosybrown3", font=("Bodoni MT", 16, "bold"))
        head.place(x=5, y=10, width=440, height=30)

        ccode_lbl = Label(self.addframe, text=" COURSE ID", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                          anchor="w")
        ccode_ent = Entry(self.addframe, textvariable=self.coursecode, font=("Roboto", 12))
        cname_lbl = Label(self.addframe, text=" COURSE NAME", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                          anchor="w")
        self.cname_text = Text(self.addframe, font=("Roboto", 11,))
        ccode_lbl.place(x=10, y=60, width=150, height=30)
        ccode_ent.place(x=160, y=60, width=270, height=30)
        cname_lbl.place(x=10, y=100, width=150, height=30)
        self.cname_text.place(x=10, y=135, width=420, height=120)

        addbtn = Button(self.addframe, text="ADD", font=("Bodoni MT", 12, "bold"), bg="Mistyrose2", fg="Gray10",
                        activebackground="Rosybrown3", activeforeground="Gray10",
                        command=self.addcourse)
        clearbtn = Button(self.addframe, text="CLEAR", font=("Bodoni MT", 12, "bold"), bg="Mistyrose2", fg="Gray10",
                          activebackground="Rosybrown3", activeforeground="Gray10",
                          command=self.clear)

        addbtn.place(width=100, height=30, y=280, x=240)
        clearbtn.place(width=100, height=30, y=280, x=345)
        self.clear()

    def addcourse(self):
        if self.coursecode.get() == "" or self.cname_text.get(1.0, END) == "":
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        if messagebox.askyesno("Add Course", "Confirm adding course?"):
            try:
                cur.execute("INSERT INTO courses VALUES (?, ?)", (self.coursecode.get(), self.cname_text.get(1.0, END)))
                conn.commit()
                messagebox.showinfo("Success", "Course added into the database")
                self.clear()
                self.addframe.destroy()
                self.searchcourse()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Course ID already in database!")

    def update_courseframe(self, ev):
        selco = self.courselist.focus()
        cont = self.courselist.item(selco)
        rows = cont['values']
        if rows == "":
            messagebox.showerror("Error", "Select a course first!")
            return
        else:
            self.key.set(rows[0])
            self.updateframe = Toplevel()
            self.updateframe.title("Update Course")
            self.updateframe.resizable(False, False)
            width = 450
            height = 320
            self.updateframe.geometry("{}x{}+{}+{}".format(width, height,
                                                           int((self.updateframe.winfo_screenwidth() - width) / 2),
                                                           int((self.updateframe.winfo_screenheight() -
                                                                60 - height)/2)))
            self.updateframe.config(bg="Rosybrown3")
            self.updateframe.grab_set()

            head = Label(self.updateframe, text="UPDATE COURSE", fg="Gray10", bg="Rosybrown3",
                         font=("Bodoni MT", 16, "bold"))
            head.place(x=5, y=10, width=440, height=30)

            self.cname_text = Text(self.updateframe, font=("Roboto", 11,))
            self.clear()
            self.cname_text.insert(END, rows[1])
            self.coursecode.set(rows[0])
            Label(self.updateframe, text=" COURSE ID", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                  anchor="w").place(x=10, y=60, width=150, height=30)
            Entry(self.updateframe, textvariable=self.coursecode, font=("Roboto", 12))\
                .place(x=160, y=60, width=270, height=30)
            Label(self.updateframe, text=" COURSE NAME", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                  anchor="w").place(x=10, y=100, width=150, height=30)
            self.cname_text.place(x=10, y=135, width=420, height=120)

            Button(self.updateframe, text="UPDATE", font=("Bodoni MT", 12, "bold"), command=self.updatecourse,
                   bg="Mistyrose2", fg="Gray10", activebackground="Rosybrown3", activeforeground="Gray10")\
                .place(width=100, height=30, y=280, x=240)
            Button(self.updateframe, text="CLEAR", font=("Bodoni MT", 12, "bold"), command=self.clear,
                   bg="Mistyrose2", fg="Gray10", activebackground="Rosybrown3", activeforeground="Gray10")\
                .place(width=100, height=30, y=280, x=345)

    def updatecourse(self):
        if self.coursecode.get() == "" or self.cname_text.get(1.0, END) == "":
            messagebox.showerror("Error", "Please fill out all fields")
            return
        else:
            if messagebox.askyesno("Update Course", "Confirm updating course?"):
                try:
                    if self.key.get() != self.coursecode.get():
                        cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?",
                                    (self.coursecode.get(), self.cname_text.get(1.0, END).replace("\n", ""),
                                     self.key.get()))
                    else:
                        cur.execute("UPDATE courses SET Course_Name=? WHERE Course_Code=?",
                                    (self.cname_text.get(1.0, END).replace("\n", ""), self.coursecode.get()))
                    conn.commit()
                    messagebox.showinfo("Success", "Course information updated!")
                    self.key.set("")
                    self.clear()
                    self.updateframe.destroy()
                    self.searchcourse()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Course already in database!")
                    return

    def deletecourse(self):
        selco = self.courselist.focus()
        cont = self.courselist.item(selco)
        rows = cont['values']
        if rows == "":
            messagebox.showerror("Error", "Select a course first!")
            return
        else:
            if messagebox.askyesno("Delete Course", "Confirm delete course?"):
                cur.execute("DELETE FROM courses WHERE Course_Code=?", (rows[0],))
                conn.commit()
                messagebox.showinfo("Success", "Course deleted in database!")
                self.searchcourse()
            else:
                return

    def clear(self):
        self.coursecode.set("")
        self.cname_text.delete(1.0, END)

    def searchcourse(self):
        if self.searchcode.get() == "":
            cur.execute("SELECT * FROM courses")
        else:
            cur.execute("SELECT * FROM courses WHERE COURSE_CODE LIKE ?", ('%' + self.searchcode.get() + '%',))
        courses = cur.fetchall()
        self.courselist.delete(*self.courselist.get_children())
        if not courses:
            return
        else:
            for z in courses:
                self.courselist.insert('', END, values=(z[0], z[1]))


def courselist():
    clist = []
    cur.execute("SELECT Course_Code from courses")
    res = cur.fetchall()
    for x in res:
        clist.append(x[0])
    return clist


class Students:
    def __init__(self, frame):
        self.idno = StringVar()
        self.name = StringVar()
        self.year = StringVar()
        self.coursecode = StringVar()
        self.year.set("Choose a year level")
        self.coursecode.set("Choose a course")

        self.key = StringVar()
        self.searchid = StringVar()

        listframe = Frame(frame)
        listframe.place(x=30, y=60, width=940, height=440)
        y = Scrollbar(listframe, orient=VERTICAL)
        self.studlist = ttk.Treeview(listframe, columns=("sid", "sname", "scourse", "syear"))
        y.pack(side=RIGHT, fill=Y)
        y.config(command=self.studlist.yview)
        self.studlist.heading("sid", text="ID NUMBER")
        self.studlist.heading("sname", text="FULL NAME")
        self.studlist.heading("scourse", text="COURSE")
        self.studlist.heading("syear", text="YEAR LEVEL")
        self.studlist['show'] = 'headings'
        self.studlist.column("sid", width=70, anchor="center")
        self.studlist.column("sname", width=250)
        self.studlist.column("scourse", width=70, anchor="center")
        self.studlist.column("syear", width=40, anchor="center")
        self.studlist.pack(fill=BOTH, expand=1)
        self.studlist.bind("<Double-1>", self.upd_studframe)

        Button(frame, text="ADD", font=("Blinker", 12, "bold"), command=self.add_studframe,
               activebackground="Mistyrose2", fg="Gray10", bg="Rosybrown3", activeforeground="Gray10").\
            place(x=30, y=20, height=30, width=80)
        Button(frame, text="DELETE", font=("Blinker", 12, "bold"), command=self.deletestudent,
               activebackground="Mistyrose2", fg="Gray10", bg="Rosybrown3", activeforeground="Gray10")\
            .place(x=115, y=20, height=30, width=80)

        search_lbl = Label(frame, text="ID  Number: ", fg="Gray10", bg="Mistyrose2", font=("Blinker", 12, "bold"),
                           anchor="e")
        search_ent = Entry(frame, textvariable=self.searchid, font=("Roboto", 12))
        searchbtn = Label(frame, text="SEARCH", font=("Blinker", 12, "bold"), fg="Gray10", bg="Rosybrown3",
                          relief=RAISED)
        self.searchid.trace("w", lambda name, index, mode, sv=self.searchid: self.searchstud())
        search_lbl.place(x=490, y=20, height=30, width=150)
        search_ent.place(x=640, y=20, height=30, width=250)
        searchbtn.place(x=890, y=20, height=30, width=80)

        self.searchstud()

    def add_studframe(self):
        self.addsframe = Toplevel()
        self.addsframe.title("Add Course")
        self.addsframe.resizable(False, False)
        self.addsframe.config(bg="Rosybrown3")
        width = 450
        height = 300
        self.addsframe.geometry("{}x{}+{}+{}".format(width, height,
                                                     int((self.addsframe.winfo_screenwidth() - width) / 2),
                                                     int((self.addsframe.winfo_screenheight() - 60 - height) / 2)))
        self.addsframe.grab_set()

        Label(self.addsframe, text="ADD STUDENT", fg="Gray10", bg="Rosybrown3", font=("Bodoni MT", 16, "bold")).\
            place(x=5, y=10, width=440, height=30)
        Label(self.addsframe, text="  ID NUMBER", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"), anchor="w").\
            place(x=10, y=60, width=135, height=35)
        Entry(self.addsframe, textvariable=self.idno, font=("Roboto", 12))\
            .place(x=145, y=60, width=295, height=35)
        Label(self.addsframe, text="  NAME", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"), anchor="w").\
            place(x=10, y=100, width=135, height=35)
        Entry(self.addsframe, textvariable=self.name, font=("Roboto", 11, "bold"))\
            .place(x=145, y=100, width=295, height=35)
        Label(self.addsframe, text="Surname, First Name M.I.", font=("Bebas Neue", 10), anchor="w",
              bg="Rosybrown3", fg="Gray10").place(x=145, y=138, height=22)
        Label(self.addsframe, text="  YEAR LEVEL", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"), anchor="w")\
            .place(x=10, y=165, width=135, height=35)
        ttk.Combobox(self.addsframe, textvariable=self.year, values=["1st Year", "2nd Year", "3rd Year", "4th Year",
                                                                     "5th Year"], font=("Roboto", 12, "bold"))\
            .place(x=145, y=165, width=295, height=35)
        Label(self.addsframe, text="  COURSE", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"), anchor="w")\
            .place(x=10, y=205, width=135, height=35)
        ttk.Combobox(self.addsframe, textvariable=self.coursecode, values=courselist(),
                     font=("Roboto", 12, "bold")).place(x=145, y=205, width=295, height=35)

        Button(self.addsframe, text="ADD", font=("Bodoni MT", 12, "bold"), command=self.addstudent, bg="Mistyrose2",
               fg="Gray10", activebackground="Rosybrown3", activeforeground="Gray10").\
            place(width=100, height=30, y=255, x=240)
        Button(self.addsframe, text="CLEAR", font=("Bodoni MT", 12, "bold"), command=self.clear, bg="Mistyrose2",
               fg="Gray10", activebackground="Rosybrown3", activeforeground="Gray10").\
            place(width=100, height=30, y=255, x=345)
        self.clear()

    def addstudent(self):
        studid = self.idno.get()
        if studid == "" or self.name.get() == "" or self.year.get() == "Choose a year level" or \
                self.coursecode.get() == "Choose a course":
            messagebox.showerror("Error", "Please fill out all fields!")
            return
        elif len(studid) != 9 or studid[4] != '-' or not studid.replace("-", "").isdigit():
            messagebox.showerror("Error", "Invalid ID Number")
            return
        else:
            if messagebox.askyesno("Add Student", "Do you wish to add the student to database?"):
                try:
                    cur.execute("INSERT INTO student VALUES(?, ?, ?, ?)",
                                (studid, self.name.get(), self.year.get(), self.coursecode.get()))
                    messagebox.showinfo("Success", "Student added to database!")
                    conn.commit()
                    self.clear()
                    self.addsframe.destroy()
                    self.searchstud()
                except sqlite3.IntegrityError:
                    if self.coursecode.get() not in self.courselist():
                        messagebox.showerror("Error", "Course ID not in database")
                    else:
                        messagebox.showerror("Error", "Student ID already in database!")

    def upd_studframe(self, ev):
        selstu = self.studlist.focus()
        cont = self.studlist.item(selstu)
        rows = cont['values']
        if rows == "":
            messagebox.showerror("Error", "Select a student first!")
            return
        else:
            self.clear()
            self.key.set(rows[0])
            self.idno.set(rows[0])
            self.name.set(rows[1])
            self.year.set(rows[3])
            self.coursecode.set(rows[2])

            self.updatesframe = Toplevel()
            self.updatesframe.title("Update Course")
            self.updatesframe.resizable(False, False)
            width = 450
            height = 300
            self.updatesframe.geometry("{}x{}+{}+{}".format(width, height,
                                                            int((self.updatesframe.winfo_screenwidth() - width) / 2),
                                                            int((self.updatesframe.winfo_screenheight() - 60 - height)
                                                                / 2)))
            self.updatesframe.config(bg="Rosybrown3")
            self.updatesframe.grab_set()

            Label(self.updatesframe, text="UPDATE STUDENT", fg="Gray10", bg="Rosybrown3",
                  font=("Bodoni MT", 16, "bold")).place(x=5, y=10, width=440, height=30)

            Label(self.updatesframe, text="  ID NUMBER", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                  anchor="w").place(x=10, y=60, width=135, height=35)
            Entry(self.updatesframe, textvariable=self.idno, font=("Roboto", 12))\
                .place(x=145, y=60, width=295, height=35)
            Label(self.updatesframe, text="  NAME", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                  anchor="w").place(x=10, y=100, width=135, height=35)
            Entry(self.updatesframe, textvariable=self.name, font=("Roboto", 11, "bold"))\
                .place(x=145, y=100, width=295, height=35)
            Label(self.updatesframe, text="Surname, First Name M.I.", font=("Bebas Neue", 10), anchor="w",
                  bg="Rosybrown3", fg="Gray10").place(x=145, y=138, height=22)
            Label(self.updatesframe, text="  YEAR LEVEL", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                  anchor="w").place(x=10, y=165, width=135, height=35)
            ttk.Combobox(self.updatesframe, textvariable=self.year, font=("Roboto", 12, "bold"),
                         values=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"]).\
                place(x=145, y=165, width=295, height=35)
            Label(self.updatesframe, text="  COURSE", fg="pink", bg="black", font=("Bodoni MT", 11, "bold"),
                  anchor="w").place(x=10, y=205, width=135, height=35)
            ttk.Combobox(self.updatesframe, textvariable=self.coursecode, values=courselist(),
                         font=("Roboto", 12, "bold")).place(x=145, y=205, width=295, height=35)

            Button(self.updatesframe, text="UPDATE", font=("Bodoni MT", 12, "bold"), command=self.updatestudent,
                   bg="Mistyrose2", fg="Gray10", activebackground="Rosybrown3", activeforeground="Gray10").\
                place(width=100, height=30, y=255, x=240)
            Button(self.updatesframe, text="CLEAR", font=("Bodoni MT", 12, "bold"), command=self.clear,
                   bg="Mistyrose2", fg="Gray10", activebackground="Rosybrown3", activeforeground="Gray10")\
                .place(width=100, height=30, y=255, x=345)

    def updatestudent(self):
        studid = self.idno.get()
        if studid == "" or self.name.get() == "" or self.year.get() == "Choose a year level" or \
                self.coursecode.get() == "Choose a course":
            messagebox.showerror("Error", "Please fill out all fields!")
            return
        elif len(studid) != 9 or studid[4] != '-' or not studid.replace("-", "").isdigit():
            messagebox.showerror("Error", "Invalid ID Number")
            return
        else:
            if messagebox.askyesno("Add Student", "Do you wish to add the student to database?"):
                try:
                    if self.key.get() != studid:
                        cur.execute("UPDATE student SET ID_Number=?, Full_Name=?, Year_Level=?, Course_Code=? "
                                    "WHERE ID_Number=?",
                                    (studid, self.name.get(), self.year.get(), self.coursecode.get(), self.key.get()))
                    else:
                        cur.execute("UPDATE student SET Full_Name=?, Year_Level=?, Course_Code=? "
                                    "WHERE ID_Number=?",
                                    (self.name.get(), self.year.get(), self.coursecode.get(), studid))
                    conn.commit()
                    messagebox.showinfo("Success", "Student information updated!")
                    self.key.set("")
                    self.updatesframe.destroy()
                    self.clear()
                    self.searchstud()
                except sqlite3.IntegrityError:
                    if self.coursecode.get() not in self.courselist():
                        messagebox.showerror("Error", "Course ID not in database")
                    else:
                        messagebox.showerror("Error", "Student ID already in database!")

    def deletestudent(self):
        sel = self.studlist.focus()
        cont = self.studlist.item(sel)
        rows = cont['values']
        if rows == "":
            messagebox.showerror("Error", "Select a student first!")
        else:
            if messagebox.askyesno("Delete Student", "Confirm deleting student?"):
                cur.execute("DELETE FROM student WHERE ID_Number=?", (rows[0],))
                conn.commit()
                messagebox.showinfo("Success", "Student deleted in database!")
                self.clear()
                self.searchstud()
            else:
                return

    def clear(self):
        self.idno.set("")
        self.name.set("")
        self.year.set("Choose a year level")
        self.coursecode.set("Choose a course")

    def searchstud(self):
        if self.searchid.get() == "":
            cur.execute("SELECT * FROM student")
        else:
            cur.execute("SELECT * FROM student WHERE ID_Number LIKE ?", ('%' + self.searchid.get() + '%',))
        search = cur.fetchall()
        self.studlist.delete(*self.studlist.get_children())
        if not search:
            return
        else:
            for x in search:
                self.studlist.insert('', END, values=(x[0], x[1], x[3], x[2]))


class Attendance:
    def __init__(self, event):
        self.atevframe = Toplevel()
        self.atevframe.title("Attendance")
        self.atevframe.resizable(False, False)
        self.studid = StringVar()
        self.searchid = StringVar()
        self.event = event
        width = 980
        height = 630
        self.atevframe.geometry("{}x{}+{}+{}".format(width, height,
                                                     int((self.atevframe.winfo_screenwidth() - width) / 2),
                                                     int((self.atevframe.winfo_screenheight() - 60 - height) / 2)))
        self.atevframe.config(bg="Rosybrown3")
        self.atevframe.grab_set()

        stime = conv_strtime_to_time(event[3])
        etime = conv_strtime_to_time(event[4])

        head = Label(self.atevframe, text="ATTENDANCE", fg="Gray10", bg="Rosybrown3", font=("Bodoni MT", 20, "bold"))
        head.place(x=270, y=20, width=440, height=30)

        details = Frame(self.atevframe, bg="Rosybrown3")
        details.place(x=10, y=70, width=960, height=75)
        Label(details, text=("Event Code: " + event[0]), font=("Blinker", 13, "bold"), bg="Mistyrose2", fg="Gray10",
              anchor="w").place(x=5, y=5, height=30)
        Label(details, text=("Location: " + event[1]), font=("Blinker", 13, "bold"), bg="Mistyrose2", fg="Gray10",
              anchor="w").place(x=5, y=40, height=30)
        Label(details, text=("Date: " + event[2]), font=("Blinker", 13, "bold"), bg="Mistyrose2", fg="Gray10",
              anchor="w").place(x=605, y=5, height=30)
        Label(details, text=("Time: " + stime.strftime('%I:%M %p') + " - " + etime.strftime('%I:%M %p')),
              font=("Blinker", 13, "bold"), anchor="w", bg="Mistyrose2", fg="Gray10").place(x=605, y=40, height=30)

        searchframe = Frame(self.atevframe, bg="Rosybrown3")
        searchframe.place(x=10, y=185, width=310, height=430)
        self.resFrame = LabelFrame(searchframe, text="  Search Result  ", font=("Blinker", 14, "bold"),
                                   bg="Mistyrose2")

        Label(searchframe, text="ID:", font=("Blinker", 13, "bold"), bg="Mistyrose2", fg="Gray10").\
            place(x=5, y=5, width=35, height=25)
        Entry(searchframe, textvariable=self.studid, font=("Bodoni MT", 14)).place(x=40, y=5, height=25, width=280)
        Button(searchframe, command=self.find_stud, bg="Mistyrose2", fg="Gray10", text="SEARCH",
               font=("Blinker", 13, "bold")).place(width=80, height=25, y=35, x=145)
        Button(searchframe, command=self.refresh, bg="Mistyrose2", fg="Gray10", text="REFRESH",
               font=("Blinker", 13, "bold")).place(width=80, height=25, y=35, x=230)

        atlistframe = Frame(self.atevframe, bg="Mistyrose2")
        atlistframe.place(x=330, y=185, width=640, height=430)

        Label(self.atevframe, text="ID:", font=("Blinker", 13, "bold"), bg="Mistyrose2", fg="Gray10"). \
            place(x=685, y=150, width=35, height=25)
        Entry(self.atevframe, textvariable=self.searchid, font=("Bodoni MT", 14))\
            .place(x=720, height=25, width=250, y=150)
        self.searchid.trace("w", lambda name, index, mode, sv=self.searchid: self.display_attendance())

        self.attelist = ttk.Treeview(atlistframe, columns=("sid", "sname", "timein", "timeout"))
        y = Scrollbar(atlistframe, orient=VERTICAL, command=self.attelist.yview)
        x = Scrollbar(atlistframe, orient=HORIZONTAL, command=self.attelist.xview)
        y.pack(side=RIGHT, fill=Y)
        x.pack(side=BOTTOM, fill=X)
        self.attelist.config(xscrollcommand=x.set, yscrollcommand=y.set)
        self.attelist.heading("sid", text="ID NO")
        self.attelist.heading("sname", text="NAME")
        self.attelist.heading("timein", text="TIME IN")
        self.attelist.heading("timeout", text="TIME OUT")
        self.attelist['show'] = 'headings'
        self.attelist.column("sid", width="120", anchor="center")
        self.attelist.column("sname", width="330", anchor="w")
        self.attelist.column("timein", width="80", anchor="center")
        self.attelist.column("timeout", width="80", anchor="center")
        self.attelist.pack(fill=BOTH, expand=1)
        self.attelist.bind("<Double-1>", self.timeout)

        self.clock = Label(searchframe, font=("Blinker", 30, "bold"), anchor='sw', bg="Rosybrown3")
        self.clock.place(x=5, y=360, width=300, height=50)
        self.ldate = Label(searchframe, font=("Blinker", 15, "bold"), bg="Rosybrown3", anchor="sw")
        self.ldate.place(x=5, y=410, height=20, width=300)
        self.time()

        stime = conv_strtime_to_time(event[3])
        self.sadv = timemargin(stime)[0]
        self.scut = timemargin(stime)[1]
        etime = conv_strtime_to_time(event[4])
        self.eadv = timemargin(etime)[0]
        self.ecut = timemargin(etime)[1]

        self.display_attendance()

    def find_stud(self):
        for frame in self.resFrame.winfo_children():
            frame.destroy()
        cur.execute("SELECT * FROM student WHERE ID_Number=?", (self.studid.get(),))
        res = cur.fetchone()
        self.resFrame.place(x=5, y=100, height=240, width=310)
        if not res:
            Label(self.resFrame, text="No results", font=("Blinker", 15, "bold"), bg="Mistyrose2", fg="Rosybrown3").\
                place(width=310, height=240)
        else:
            Label(self.resFrame, text=("Name:" + res[1]), font=("Blinker", 12, "bold"), bg="Mistyrose2", fg="Gray10").\
                place(x=5, y=10, height=40)
            Label(self.resFrame, text=("Year:" + res[2]), font=("Blinker", 12, "bold"), bg="Mistyrose2", fg="Gray10").\
                place(x=5, y=55, height=40)
            Label(self.resFrame, text=("Course:" + res[3]), font=("Blinker", 12, "bold"), bg="Mistyrose2",
                  fg="Gray10").place(x=5, y=100, height=40)
            Button(self.resFrame, text="TIME IN!", bg="Rosybrown3", fg="Gray10", font=("Blinker", 12, "bold"),
                   command=lambda x=res[0]: self.timein(x)).place(width=100, height=30, y=150, x=190)

    def timein(self, stud):
        if get_curtime() < self.sadv:
            messagebox.showwarning("Time-In Error", "Time-in not started!")
            return
        elif get_curtime() > self.scut:
            messagebox.showwarning("Time-In Error", "Time-in already finished")
            return
        else:
            try:
                cur.execute("INSERT INTO ATTENDANCE (Event_Code, ID_Number, Time_In)  VALUES (?, ?, ?)",
                            (self.event[0], stud, get_curtime()))
                conn.commit()
                messagebox.showinfo("Success", ("Student " + stud + " has timed in!"))
                self.display_attendance()
                self.refresh()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Time-In Error", "Student already has timed in!")

    def timeout(self, ev):
        selco = self.attelist.focus()
        cont = self.attelist.item(selco)
        rows = cont['values']
        if get_curtime() < self.eadv:
            messagebox.showwarning("Time-Out Error", "Time-out not started!")
            return
        elif get_curtime() > self.ecut:
            messagebox.showwarning("Time-Out Error", "Time-out already finished")
            return
        else:
            if not rows:
                messagebox.showerror("Error", "Select a student first!")
                return
            else:
                cur.execute("SELECT Time_Out FROM ATTENDANCE WHERE Event_Code=? AND ID_Number=?",
                            (self.event[0], rows[0]))
                res = cur.fetchone()[0]
                if res is None:
                    cur.execute("UPDATE ATTENDANCE SET Time_Out=? WHERE Event_Code=? AND ID_Number=?",
                                (get_curtime(), self.event[0], rows[0]))
                    conn.commit()
                    messagebox.showinfo("Success", ("Student " + rows[0] + " has timed out!"))
                    self.display_attendance()
                    self.refresh()
                else:
                    messagebox.showwarning("Time-Out Error", "Student has already timed out!")
                    return

    def refresh(self):
        self.studid.set("")
        self.resFrame.place_forget()

    def time(self):
        string = datetime.now().strftime('%I:%M:%S %p')
        self.ldate.config(text=datetime.now().strftime("%a, %b %d %Y"))
        self.clock.config(text=string)
        self.clock.after(200, self.time)

    def display_attendance(self):
        self.attelist.delete(*self.attelist.get_children())
        if self.searchid.get() == "":
            cur.execute("SELECT * FROM ATTENDANCE WHERE Event_Code=?", (self.event[0],))
        else:
            cur.execute("SELECT * FROM ATTENDANCE WHERE Event_Code=? AND ID_Number LIKE ?",
                        (self.event[0], '%' + self.searchid.get() + '%',))
        allrec = cur.fetchall()
        if not allrec:
            return
        else:
            for x in allrec:
                cur.execute("SELECT Full_Name FROM student WHERE ID_Number=?", (x[1],))
                sname = cur.fetchone()[0]
                tout = x[3]
                if tout is not None:
                    tout = conv_strtime_to_time(tout).strftime('%I:%M %p')
                self.attelist.insert('', END, values=(x[1], sname, conv_strtime_to_time(x[2]).strftime('%I:%M %p'),
                                                      tout))


root = Tk()
ob = App(root)
root.mainloop()
