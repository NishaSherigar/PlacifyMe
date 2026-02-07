from tkinter import *
import sqlite3
from tkinter import messagebox
import os
import re

# ============ PROFESSIONAL COLOR SCHEME ============
PRIMARY_COLOR = "#0f766e"  # Teal for companies
SECONDARY_COLOR = "#134e4a"
ACCENT_COLOR = "#006b5d"
LIGHT_BG = "#f0fdfa"
WHITE = "#ffffff"
TEXT_PRIMARY = "#1e293b"
TEXT_SECONDARY = "#64748b"
SUCCESS_COLOR = "#059669"

def back():
    window.destroy()
    os.system('python common.py')

window = Tk()
window.title("Company Registration - PlacifyMe")
window.state("zoomed")
window.config(bg=LIGHT_BG)

# ============ FORM VARIABLES ============
company_name_var = StringVar()
industry_var = StringVar()
email_var = StringVar()
phone_var = StringVar()
location_var = StringVar()
hr_contact_var = StringVar()
company_id_var = StringVar()
password_var = StringVar()
confirm_pwd_var = StringVar()
requirements_var = StringVar()

# ============ HEADER ============
header = Frame(window, bg=PRIMARY_COLOR, height=100)
header.pack(fill=X)
Label(header, text="Company Registration", font=("Segoe UI", 32, "bold"), bg=PRIMARY_COLOR, fg=WHITE).pack(pady=20)

# ============ CONTENT AREA ============
content = Frame(window, bg=LIGHT_BG)
content.pack(fill=BOTH, expand=True, padx=100, pady=40)

Label(content, text="Register Your Company with PlacifyMe", font=("Segoe UI", 18, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(pady=20)

# ============ FORM FRAME ============
form_container = Frame(content, bg=LIGHT_BG)
form_container.pack(pady=20, fill=BOTH, expand=True)

# Create canvas for scrollable form
canvas = Canvas(form_container, bg=LIGHT_BG, highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(form_container, orient="vertical", command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.config(yscrollcommand=scrollbar.set)

form = Frame(canvas, bg=LIGHT_BG)
canvas.create_window((0, 0), window=form, anchor="nw")

# Row 1: Company Name and Industry
row1 = Frame(form, bg=LIGHT_BG)
row1.pack(fill=X, pady=10)

left_col = Frame(row1, bg=LIGHT_BG)
left_col.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

right_col = Frame(row1, bg=LIGHT_BG)
right_col.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0))

Label(left_col, text='Company Name:', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(left_col, textvariable=company_name_var, width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

Label(right_col, text='Industry:', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(right_col, textvariable=industry_var, width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

# Row 2: Company ID and Password
row2 = Frame(form, bg=LIGHT_BG)
row2.pack(fill=X, pady=10)

left_col2 = Frame(row2, bg=LIGHT_BG)
left_col2.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

right_col2 = Frame(row2, bg=LIGHT_BG)
right_col2.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0))

Label(left_col2, text='Company ID:', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(left_col2, textvariable=company_id_var, width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

Label(right_col2, text='Password:', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(right_col2, textvariable=password_var, show="*", width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

# Row 3: Confirm Password
row3 = Frame(form, bg=LIGHT_BG)
row3.pack(fill=X, pady=10)

Label(row3, text='Confirm Password:', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(row3, textvariable=confirm_pwd_var, show="*", width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

# Row 4: Email and Phone
row4 = Frame(form, bg=LIGHT_BG)
row4.pack(fill=X, pady=10)

left_col4 = Frame(row4, bg=LIGHT_BG)
left_col4.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

right_col4 = Frame(row4, bg=LIGHT_BG)
right_col4.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0))

Label(left_col4, text='Company Email:', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(left_col4, textvariable=email_var, width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

Label(right_col4, text='Phone Number:', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(right_col4, textvariable=phone_var, width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

# Row 5: Location and HR Contact
row5 = Frame(form, bg=LIGHT_BG)
row5.pack(fill=X, pady=10)

left_col5 = Frame(row5, bg=LIGHT_BG)
left_col5.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

right_col5 = Frame(row5, bg=LIGHT_BG)
right_col5.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0))

Label(left_col5, text='Location/City:', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(left_col5, textvariable=location_var, width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

Label(right_col5, text='HR Contact Name:', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(right_col5, textvariable=hr_contact_var, width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

# Row 6: Requirements
row6 = Frame(form, bg=LIGHT_BG)
row6.pack(fill=X, pady=10)

Label(row6, text='Job Requirements (comma-separated):', font=('Segoe UI', 11, "bold"), bg=LIGHT_BG, fg=TEXT_PRIMARY).pack(anchor=W, pady=(0,5))
Entry(row6, textvariable=requirements_var, width=40, font=('Segoe UI', 11), relief=FLAT, bg=WHITE, bd=1).pack(fill=X, ipady=10, pady=5)

# Update scroll region
def on_frame_configure(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

form.bind("<Configure>", on_frame_configure)

# ============ BUTTONS ============
btn_frame = Frame(content, bg=LIGHT_BG)
btn_frame.pack(pady=30, fill=X, padx=100)

def submit_company_registration():
    # Validation
    if not all([company_name_var.get(), industry_var.get(), company_id_var.get(), 
                password_var.get(), email_var.get(), phone_var.get(), location_var.get(), hr_contact_var.get()]):
        messagebox.showerror("Error", "Please fill all required fields")
        return
    
    if password_var.get() != confirm_pwd_var.get():
        messagebox.showerror("Error", "Passwords do not match")
        return
    
    if len(password_var.get()) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters")
        return
    
    # Validate email format
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_var.get()):
        messagebox.showerror("Error", "Invalid email format")
        return
    
    # Validate phone format
    if not phone_var.get().isdigit() or len(phone_var.get()) != 10:
        messagebox.showerror("Error", "Phone must be 10 digits")
        return
    
    try:
        conn = sqlite3.connect('registration_student.db')
        cur = conn.cursor()
        
        cur.execute("INSERT INTO company_login (name, id, password, email, phone, location, hr_contact, industry, requirements) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (company_name_var.get(), company_id_var.get(), password_var.get(), email_var.get(), phone_var.get(),
                    location_var.get(), hr_contact_var.get(), industry_var.get(), requirements_var.get()))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Company registered successfully!\n\nCompany ID: {company_id_var.get()}\nYou can now login.")
        window.destroy()
        import common
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Company ID already exists")
    except Exception as e:
        messagebox.showerror("Error", f"Registration failed: {str(e)}")

Button(btn_frame, text="Register Company", font=("Segoe UI", 11, "bold"), command=submit_company_registration,
       bg=SUCCESS_COLOR, fg=WHITE, padx=30, pady=10, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=5)
Button(btn_frame, text="Back to Login", font=("Segoe UI", 11, "bold"), command=back,
       bg=PRIMARY_COLOR, fg=WHITE, padx=30, pady=10, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=5)

window.mainloop()

def is_strong_password(password):
    if not re.search(r"[A-Z]", password): return False
    if not re.search(r"[a-z]", password): return False
    if not re.search(r"\d", password): return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): return False
    if len(password) < 8: return False
    return True

def submit():
    if not is_strong_password(pwd_var.get()):
        messagebox.showerror("Weak Password", "Password not strong enough")
        return
    conn = sqlite3.connect('registration_student.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS company_login (name TEXT, id TEXT PRIMARY KEY, password TEXT)''')
    cur.execute("INSERT INTO company_login VALUES (?, ?, ?)", (name_var.get(), reg_var.get(), pwd_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Registered successfully")
    window.destroy()
    import common

def cancel():
    window.destroy()
    import common

def reset():
    name_var.set("")
    reg_var.set("")
    pwd_var.set("")

button_frame = Frame(form, bg=LIGHT_BG)
button_frame.pack(pady=30, fill=X)

Button(button_frame, text='Submit', font=('Arial', 11, 'bold'), command=submit, bg=SECONDARY_COLOR, fg=WHITE, padx=25, pady=8, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=5)
Button(button_frame, text='Cancel', font=('Arial', 11, 'bold'), command=cancel, bg=PRIMARY_COLOR, fg=WHITE, padx=25, pady=8, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=5)
Button(button_frame, text='Reset', font=('Arial', 11, 'bold'), command=reset, bg=ACCENT_COLOR, fg=WHITE, padx=25, pady=8, relief=FLAT, cursor="hand2").pack(side=LEFT, padx=5)

window.mainloop()
