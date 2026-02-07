import sqlite3
from tkinter import messagebox
import tkinter as tk
import os

win = tk.Tk()
win.state('zoomed')  # Maximize window

# Professional color scheme
PRIMARY = "#0f766e"  # Teal for companies
SECONDARY = "#134e4a"
LIGHT_BG = "#f0fdfa"
WHITE = "#ffffff"
TEXT_DARK = "#1e293b"
TEXT_LIGHT = "#64748b"

def cancel():
    win.destroy()
    os.system('python common.py')

def clear():
    userentry.delete(0, tk.END)
    passentry.delete(0, tk.END)

def login():
    if user_id.get() == "" or password.get() == "":
        messagebox.showerror("Error", "Enter Company ID And Password")
    else:
        try:
            conn = sqlite3.connect('registration_student.db')
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM company_login WHERE id=? AND password=?",
                (user_id.get(), password.get())
            )
            row = cur.fetchone()
            if row:
                messagebox.showinfo("Success", "Successfully Login")
                win.destroy()
                # Use new dashboard
                os.system(f'python company_dashboard.py "{user_id.get()}"')
            else:
                messagebox.showerror("Error", "Invalid Company ID Or Password")
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}")

def signup():
    win.destroy()
    os.system('python cmp_signup.py')

win.title("PlacifyMe - Company Login")
win.config(bg=LIGHT_BG)

# Create main container
main_frame = tk.Frame(win, bg=LIGHT_BG)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create center frame with card design
center_frame = tk.Frame(main_frame, bg=WHITE)
center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=520)

# Header
header_frame = tk.Frame(center_frame, bg=PRIMARY)
header_frame.pack(fill=tk.X)

heading = tk.Label(header_frame, text="Company Login", font=('Arial', 24, 'bold'), bg=PRIMARY, fg=WHITE)
heading.pack(pady=25)

# Form frame
form_frame = tk.Frame(center_frame, bg=WHITE)
form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

company_id_label = tk.Label(form_frame, text="Company ID", font=('Arial', 12, 'bold'), bg=WHITE, fg=TEXT_DARK)
company_id_label.pack(anchor=tk.W, pady=(0, 8))

user_id = tk.StringVar()
userentry = tk.Entry(form_frame, textvariable=user_id, font=('Arial', 12), width=40, bd=1, relief=tk.SOLID)
userentry.pack(fill=tk.X, pady=(0, 25), ipady=8)

pwd_label = tk.Label(form_frame, text="Password", font=('Arial', 12, 'bold'), bg=WHITE, fg=TEXT_DARK)
pwd_label.pack(anchor=tk.W, pady=(0, 8))

password = tk.StringVar()
passentry = tk.Entry(form_frame, textvariable=password, font=('Arial', 12), width=40, show="*", bd=1, relief=tk.SOLID)
passentry.pack(fill=tk.X, pady=(0, 35), ipady=8)

# Buttons frame
button_frame = tk.Frame(form_frame, bg=WHITE)
button_frame.pack(fill=tk.X, pady=(10, 0))

tk.Button(button_frame, text="Login", font=('Arial', 12, 'bold'), command=login, bg=PRIMARY, fg=WHITE, padx=30, pady=12, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Clear", font=('Arial', 12, 'bold'), command=clear, bg=TEXT_LIGHT, fg=WHITE, padx=30, pady=12, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Sign Up", font=('Arial', 12, 'bold'), command=signup, bg=SECONDARY, fg=WHITE, padx=30, pady=12, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Home", font=('Arial', 12, 'bold'), command=cancel, bg="#6b7280", fg=WHITE, padx=30, pady=12, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)

win.mainloop()
