import os
import sys
from threading import Thread
import tkinter as tk
from tkinter import messagebox, ttk
import requests as rq
import time
from functions import login, add_course, extract_seating_data
import sv_ttk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

def find_course(course):
    seating = extract_seating_data()
    for i in seating:
        if course[0] == i['crscode'] and course[1] == str(i['sectno']):
            return i['remainingSeats']
    return -1


def check_course(course):
    if len(course) == 2:
        if find_course(course) > 0:
            return True
    elif len(course) == 3:
        if find_course(course[:-1]) > 0 and find_course(course[::2]) > 0:
            return True
    return False


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


root = tk.Tk()
style = ttk.Style()
sv_ttk.set_theme("dark")
root.title("SQU-Seat-Stealer v2.2")
root.iconbitmap(resource_path("happy.ico"))

tk.Label(text="SQU Seats Stealer", font="Arial 18").pack(pady=(10, 0))

lbl_username = ttk.Label(text="Username", font="Arial 12")
lbl_username.pack(pady=(10, 0))

ent_username = ttk.Entry(font="Arial 15", justify='center')
ent_username.pack(padx=20)

lbl_password = ttk.Label(text="Password", font="Arial 12")
lbl_password.pack(pady=(10, 0))

ent_password = ttk.Entry(font="Arial 15", justify='center')
ent_password.pack(padx=20)

lbl_course = ttk.Label(text="Course", font="Arial 12")
lbl_course.pack(pady=(10, 0))

ent_course = ttk.Entry(font="Arial 15", justify='center')
ent_course.pack(padx=20)


def clicked():
    username = ent_username.get()
    password = ent_password.get()
    course = ent_course.get()
    if username == "" or password == "" or course == "":
        messagebox.showerror("ERROR", "Please fill all entries.")
        return
    btn_register['state'] = 'disabled' 
    s = rq.Session()
    ids = rq.get("https://raw.githubusercontent.com/Mohammed-Alabri/python-projects/main/abcbufc.txt")
    if username.lower() not in ids.text.split():
        messagebox.showerror("ERROR", "Please contact with developer.")
        btn_register['state'] = 'normal'
        return
    values = {
        "username": username,
        "password": password
    }
    if not login(values, s):
        messagebox.showerror("ERROR", "Username or password is incorrect.")
        btn_register['state'] = 'normal'
        return
    course = course.split()
    if not (1 < len(course) < 4):
        messagebox.showerror("ERROR", "Please Enter course correctly.")
        btn_register['state'] = 'normal'
        return
    course[0] = course[0].upper()
    attempt = 0
    status = False
    while not status:
        time.sleep(.8)
        attempt += 1
        lbl_status["text"] = "Status: waiting" + ((attempt % 4) * '.') + "\n" + f"attemp : {attempt}"
        if check_course(course):
            login(values, s)
            if add_course(course, s):
                status = True
                lbl_status["text"] = "Status: DONE!!!" + "\n" + f"attemp : {attempt}"
                lbl_status["foreground"] = "green"
    btn_register['state'] = 'normal'
    
    
def start_clicked():
    t = Thread(target=clicked, daemon=True)
    t.start()


style.configure("register.TButton", font=(None, 15))
btn_register = ttk.Button(text='Register', width=20, command=start_clicked, style="register.TButton")
btn_register.pack(pady=15)

card = ttk.Frame(root, style='Card.TFrame', padding=(5, 6, 7, 8))

lbl_status = ttk.Label(card, text="Status:", justify=tk.CENTER, anchor="center",
                       font=('Arial', 12), width=20)

card.pack(pady=10)
lbl_status.pack()
ttk.Label(text="Made by: Mohammed Al-Abri.", font="Arial 12").pack(pady=(10, 0))

root.resizable(height=False, width=False)

sv_ttk.set_theme("dark")
root.mainloop()