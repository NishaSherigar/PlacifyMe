import sqlite3
from tkinter import messagebox, ttk
from tkinter import *
import os
import re

# ============ PROFESSIONAL COLOR SCHEME ============
PRIMARY_COLOR = "#3b82f6"
SECONDARY_COLOR = "#1e293b"
ACCENT_COLOR = "#0f172a"
LIGHT_BG = "#f8fafc"
WHITE = "#ffffff"
TEXT_PRIMARY = "#0f172a"
TEXT_SECONDARY = "#64748b"
SUCCESS_COLOR = "#10b981"
BORDER_COLOR = "#e2e8f0"

def back():
    window.destroy()
    import common

window = Tk()
window.title("Student Registration - PlacifyMe")
window.state("zoomed")
window.config(bg=LIGHT_BG)

# ============ HEADER ============
header = Frame(window, bg=PRIMARY_COLOR, height=100)
header.pack(fill=X)
Label(header, text="Student Registration", font=("Segoe UI", 32, "bold"), bg=PRIMARY_COLOR, fg=WHITE).pack(pady=20)

# ============ MAIN CONTAINER (Left form + Right table) ============
main_container = Frame(window, bg=LIGHT_BG)
main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

# ============ LEFT SIDE - FORM ============
form_frame = Frame(main_container, bg=WHITE, relief=SOLID, bd=1)
form_frame.pack(side=LEFT, fill=BOTH, expand=False, padx=(0, 20), pady=20)

Label(form_frame, text="Create New Account", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT_PRIMARY).pack(pady=15, padx=20, anchor=W)

# Scrollable form
canvas = Canvas(form_frame, bg=WHITE, highlightthickness=0, width=280)
canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

scrollbar = Scrollbar(form_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 10), pady=10)

canvas.config(yscrollcommand=scrollbar.set)

form_inner = Frame(canvas, bg=WHITE)
canvas.create_window((0, 0), window=form_inner, anchor="nw")

# Form variables
name_var = StringVar()
email_var = StringVar()
phone_var = StringVar()
student_id_var = StringVar()
pwd_var = StringVar()
confirm_pwd_var = StringVar()
branch_var = StringVar()
year_var = StringVar()
cgpa_var = StringVar()
cet_var = StringVar()
gender_var = StringVar()

# Helper function to add field
def add_field(parent, label_text, var_obj=None, field_type="entry", options=None):
    Label(parent, text=label_text + ":", font=("Segoe UI", 9, "bold"), bg=WHITE, fg=TEXT_PRIMARY).pack(anchor=W, pady=(10, 3), padx=15)
    
    if field_type == "entry":
        entry = Entry(parent, width=30, font=("Segoe UI", 10), relief=FLAT, bg=LIGHT_BG, bd=1, textvariable=var_obj)
        entry.pack(fill=X, ipady=8, padx=15, pady=(0, 5))
        return entry
    elif field_type == "password":
        entry = Entry(parent, width=30, font=("Segoe UI", 10), relief=FLAT, bg=LIGHT_BG, bd=1, show="*", textvariable=var_obj)
        entry.pack(fill=X, ipady=8, padx=15, pady=(0, 5))
        return entry
    elif field_type == "combo":
        combo = ttk.Combobox(parent, width=27, font=("Segoe UI", 10), state="readonly", textvariable=var_obj)
        combo['values'] = options
        combo.pack(fill=X, ipady=6, padx=15, pady=(0, 5))
        return combo

# Form fields
add_field(form_inner, "Full Name", name_var)
add_field(form_inner, "Email ID", email_var)
add_field(form_inner, "Phone No.", phone_var)
add_field(form_inner, "Gender", gender_var, "combo", ["Male", "Female", "Other"])
add_field(form_inner, "Student ID", student_id_var)
add_field(form_inner, "Branch", branch_var, "combo", ["IT", "EXTC", "MECH", "ELECTRICAL", "COMP", "CHEMICAL"])
add_field(form_inner, "Year", year_var, "combo", ["FE", "TE", "BE"])
add_field(form_inner, "CGPA", cgpa_var)
add_field(form_inner, "CET/JEE Score", cet_var)
add_field(form_inner, "Password", pwd_var, "password")
add_field(form_inner, "Confirm Password", confirm_pwd_var, "password")

# Update scroll region
def on_frame_configure(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))
form_inner.bind("<Configure>", on_frame_configure)

# Buttons
btn_frame = Frame(form_inner, bg=WHITE)
btn_frame.pack(fill=X, pady=20, padx=15)

def register():
    name = name_var.get().strip()
    email = email_var.get().strip()
    phone = phone_var.get().strip()
    gender = gender_var.get().strip()
    student_id = student_id_var.get().strip()
    branch = branch_var.get().strip()
    year = year_var.get().strip()
    cgpa = cgpa_var.get().strip()
    cet = cet_var.get().strip()
    pwd = pwd_var.get().strip()
    confirm_pwd = confirm_pwd_var.get().strip()
    
    # Validation
    if not all([name, email, phone, gender, student_id, branch, year, cgpa, cet, pwd, confirm_pwd]):
        messagebox.showerror("Error", "Please fill all fields")
        return
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Error", "Invalid email format")
        return
    
    if len(pwd) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters")
        return
    
    if pwd != confirm_pwd:
        messagebox.showerror("Error", "Passwords do not match")
        return
    
    try:
        # Validate CGPA
        cgpa_val = float(cgpa)
        if cgpa_val < 0 or cgpa_val > 10:
            messagebox.showerror("Error", "CGPA must be between 0 and 10")
            return
        
        # Validate phone
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Error", "Phone must be 10 digits")
            return
        
        conn = sqlite3.connect('registration_student.db')
        cur = conn.cursor()
        
        # Check if student_id already exists
        cur.execute("SELECT * FROM student_signUP WHERE student_id=?", (student_id,))
        if cur.fetchone():
            messagebox.showerror("Error", f"Student ID '{student_id}' already exists")
            conn.close()
            return
        
        # Check if email already exists
        cur.execute("SELECT * FROM student_signUP WHERE email=?", (email,))
        if cur.fetchone():
            messagebox.showerror("Error", f"Email '{email}' already registered")
            conn.close()
            return
        
        # Insert into database
        cur.execute("""INSERT INTO student_signUP 
                      (name, email, phone, gender, student_id, password, branch, year, cgpa, cet_score)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (name, email, phone, gender, student_id, pwd, branch, year, cgpa, cet))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Registration successful!\nStudent ID: {student_id}\nPassword: {pwd}\n\nYou can now login")
        
        # Clear form
        name_var.set("")
        email_var.set("")
        phone_var.set("")
        gender_var.set("")
        student_id_var.set("")
        branch_var.set("")
        year_var.set("")
        cgpa_var.set("")
        cet_var.set("")
        pwd_var.set("")
        confirm_pwd_var.set("")
        
        # Refresh table
        load_registered_students()
        
    except ValueError:
        messagebox.showerror("Error", "CGPA must be a number")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def reset_form():
    name_var.set("")
    email_var.set("")
    phone_var.set("")
    gender_var.set("")
    student_id_var.set("")
    branch_var.set("")
    year_var.set("")
    cgpa_var.set("")
    cet_var.set("")
    pwd_var.set("")
    confirm_pwd_var.set("")

Button(btn_frame, text="Submit", font=("Segoe UI", 9, "bold"), command=register, bg=PRIMARY_COLOR, fg=WHITE, padx=15, pady=8, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=3)
Button(btn_frame, text="Reset", font=("Segoe UI", 9, "bold"), command=reset_form, bg=TEXT_SECONDARY, fg=WHITE, padx=15, pady=8, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=3)
Button(btn_frame, text="Back", font=("Segoe UI", 9, "bold"), command=back, bg=ACCENT_COLOR, fg=WHITE, padx=15, pady=8, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=3)

# ============ RIGHT SIDE - TABLE ============
table_frame = Frame(main_container, bg=WHITE, relief=SOLID, bd=1)
table_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=20)

Label(table_frame, text="Registered Students", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT_PRIMARY).pack(pady=15, padx=20, anchor=W)

# Treeview table
columns = ("Full name", "Email id", "Phone no.", "Gender", "Registration", "Branch", "Year", "CGPA", "CET/JEE")
tree = ttk.Treeview(table_frame, columns=columns, height=20, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=85)

# Add scrollbar to table
table_scroll = Scrollbar(table_frame, orient="vertical", command=tree.yview)
table_scroll.pack(side=RIGHT, fill=Y, padx=(0, 10), pady=10)
tree.config(yscroll=table_scroll.set)

tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

def load_registered_students():
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
    
    try:
        conn = sqlite3.connect('registration_student.db')
        cur = conn.cursor()
        cur.execute("SELECT name, email, phone, student_id, branch, year, cgpa FROM student_signUP ORDER BY rowid DESC LIMIT 100")
        
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load students: {str(e)}")

# Load students on startup
load_registered_students()

window.mainloop()
