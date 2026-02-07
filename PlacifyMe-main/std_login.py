import sqlite3
from tkinter import messagebox
from tkinter import *
import os

win = Tk()
win.state('zoomed')  # Maximize window

# Professional color scheme
PRIMARY = "#4f46e5"
SECONDARY = "#3730a3"
LIGHT_BG = "#f8fafc"
WHITE = "#ffffff"
TEXT_DARK = "#1e293b"
TEXT_LIGHT = "#64748b"

def cancel():
    win.destroy()
    os.system('python common.py')

def clear():
    userentry.delete(0, END)
    passentry.delete(0, END)

def login():
    if user_name.get() == "" or password.get() == "":
        messagebox.showerror("Error", "Enter User ID And Password", parent=win)
    else:
        try:
            con = sqlite3.connect('registration_student.db')
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM student_signUP WHERE student_id=? AND password=?",
                (user_name.get().strip(), password.get().strip())
            )
            row = cur.fetchone()
            if row:
                messagebox.showinfo("Success", "Successfully Login")
                win.destroy()
                # Launch the student dashboard
                os.system(f'python student_dashboard.py "{user_name.get()}"')
            else:
                messagebox.showerror("Error", "Invalid User ID Or Password")
            con.close()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to : {str(es)}")

def signup():
    win.destroy()
    os.system('python std_signup.py')

win.title("PlacifyMe - Student Login")
win.config(bg=LIGHT_BG)

# Create main container
main_frame = Frame(win, bg=LIGHT_BG)
main_frame.pack(fill=BOTH, expand=True)

# Create center frame with card design
center_frame = Frame(main_frame, bg=WHITE)
center_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=520)

# Header
header_frame = Frame(center_frame, bg=PRIMARY)
header_frame.pack(fill=X)

heading = Label(header_frame, text="Student Login", font=('Arial', 24, 'bold'), bg=PRIMARY, fg=WHITE)
heading.pack(pady=25)

# Form frame
form_frame = Frame(center_frame, bg=WHITE)
form_frame.pack(fill=BOTH, expand=True, padx=50, pady=30)

username_label = Label(form_frame, text="User ID", font=('Arial', 12, 'bold'), bg=WHITE, fg=TEXT_DARK)
username_label.pack(anchor=W, pady=(0, 8))

user_name = StringVar()
userentry = Entry(form_frame, textvariable=user_name, font=('Arial', 12), width=40, bd=1, relief=SOLID)
userentry.pack(fill=X, pady=(0, 25), ipady=8)
userentry.focus()

userpass_label = Label(form_frame, text="Password", font=('Arial', 12, 'bold'), bg=WHITE, fg=TEXT_DARK)
userpass_label.pack(anchor=W, pady=(0, 8))

password = StringVar()
passentry = Entry(form_frame, textvariable=password, font=('Arial', 12), width=40, show="*", bd=1, relief=SOLID)
passentry.pack(fill=X, pady=(0, 35), ipady=8)

# Buttons frame
button_frame = Frame(form_frame, bg=WHITE)
button_frame.pack(fill=X, pady=(10, 0))

Button(button_frame, text="Login", font=('Arial', 12, 'bold'), command=login, bg=PRIMARY, fg=WHITE, padx=30, pady=12, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=5)
Button(button_frame, text="Clear", font=('Arial', 12, 'bold'), command=clear, bg=TEXT_LIGHT, fg=WHITE, padx=30, pady=12, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=5)
Button(button_frame, text="Sign Up", font=('Arial', 12, 'bold'), command=signup, bg=SECONDARY, fg=WHITE, padx=30, pady=12, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=5)
Button(button_frame, text="Home", font=('Arial', 12, 'bold'), command=cancel, bg="#6b7280", fg=WHITE, padx=30, pady=12, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=5)

win.mainloop()
