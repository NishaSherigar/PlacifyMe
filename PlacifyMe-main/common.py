#!/usr/bin/env python3
"""
PlacifyMe - Professional Placement Management System
Version: 2.0
"""

import sys
import os
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import sqlite3
import hashlib

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class PlacifyMe(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("PlacifyMe - Placement Management System")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        self.state("zoomed")  # Maximize window on startup
        
        # Center window
        self.center_window()
        
        # Initialize database
        self.init_database()
        
        # Load assets
        self.load_assets()
        
        # Create main container
        self.create_main_layout()
        
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def init_database(self):
        """Initialize database connection"""
        try:
            self.conn = sqlite3.connect('registration_student.db')
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            sys.exit(1)
    
    def load_assets(self):
        """Load images and icons"""
        try:
            # Create images directory if not exists
            os.makedirs("assets", exist_ok=True)
            
            # Placeholder images - in real app, add actual images
            self.logo_img = Image.new('RGB', (200, 60), color='#3b82f6')
            self.student_img = Image.new('RGB', (150, 150), color='#10b981')
            self.company_img = Image.new('RGB', (150, 150), color='#f59e0b')
            self.admin_img = Image.new('RGB', (150, 150), color='#ef4444')
            self.tpo_img = Image.new('RGB', (150, 150), color='#8b5cf6')
            
        except Exception as e:
            print(f"Asset loading error: {e}")
    
    def create_main_layout(self):
        """Create main landing page"""
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_header()
        
        # Content
        self.create_landing_content()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Create header with logo and navigation"""
        header_frame = ctk.CTkFrame(self.main_frame, height=80, fg_color="#ffffff")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Logo
        logo_label = ctk.CTkLabel(
            header_frame, 
            text="🎯 PlacifyMe", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1e293b"
        )
        logo_label.pack(side="left", padx=20)
        
        # Tagline
        tagline = ctk.CTkLabel(
            header_frame,
            text="Professional Placement Management System",
            font=ctk.CTkFont(size=14),
            text_color="#64748b"
        )
        tagline.pack(side="left", padx=10)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.pack(side="right", padx=20)
        
        buttons = [
            ("Home", lambda: self.show_landing()),
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                text_color="#3b82f6",
                hover_color="#f1f5f9",
                width=80,
                command=command
            )
            btn.pack(side="left", padx=5)
    
    def create_landing_content(self):
        """Create landing page content"""
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Welcome section
        welcome_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        welcome_frame.pack(fill="x", pady=(0, 40))
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="Welcome to PlacifyMe",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#0f172a"
        )
        welcome_label.pack()
        
        sub_label = ctk.CTkLabel(
            welcome_frame,
            text="Streamlining placement processes for colleges and companies",
            font=ctk.CTkFont(size=16),
            text_color="#64748b"
        )
        sub_label.pack(pady=10)
        
        # Role selection cards
        roles_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        roles_frame.pack(fill="both", expand=True)
        
        roles = [
            ("👨‍🎓 Student", "Login as student to apply for jobs, track applications, and upload documents", 
             "#10b981", self.student_login),
            ("🏢 Company", "Login as company to post jobs, manage applications, and conduct interviews",
             "#f59e0b", self.company_login),
            ("👨‍💼 TPO", "Login as Training & Placement Officer to manage placements, generate reports",
             "#8b5cf6", self.tpo_login),
            ("⚙️ Admin", "Login as administrator to manage users, system settings, and monitor activities",
             "#ef4444", self.admin_login)
        ]
        
        for i, (title, description, color, command) in enumerate(roles):
            card = self.create_role_card(roles_frame, title, description, color, command)
            row = i // 2
            col = i % 2
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Configure grid weights
        roles_frame.grid_columnconfigure(0, weight=1)
        roles_frame.grid_columnconfigure(1, weight=1)
        roles_frame.grid_rowconfigure(0, weight=1)
        roles_frame.grid_rowconfigure(1, weight=1)
    
    def create_role_card(self, parent, title, description, color, command):
        """Create a role selection card"""
        card = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color="white",
            border_width=1,
            border_color="#e2e8f0"
        )
        
        # Top color strip
        top_strip = ctk.CTkFrame(card, height=5, fg_color=color, corner_radius=15)
        top_strip.pack(fill="x", padx=1, pady=(1, 0))
        
        # Content
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1e293b"
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text=description,
            font=ctk.CTkFont(size=14),
            text_color="#64748b",
            wraplength=250,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 20))
        
        # Login button
        login_btn = ctk.CTkButton(
            content_frame,
            text="Login",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=color,
            hover_color=self.darken_color(color),
            height=40,
            command=command
        )
        login_btn.pack(fill="x")
        
        return card
    
    def darken_color(self, color):
        """Darken a hex color"""
        # Simple darkening for hover effect
        r = int(color[1:3], 16) - 20
        g = int(color[3:5], 16) - 20
        b = int(color[5:7], 16) - 20
        return f"#{max(0, r):02x}{max(0, g):02x}{max(0, b):02x}"
    
    def create_footer(self):
        """Create footer"""
        footer_frame = ctk.CTkFrame(self.main_frame, height=60, fg_color="#f8fafc")
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        # Copyright
        copyright_label = ctk.CTkLabel(
            footer_frame,
            text="© 2024 PlacifyMe Placement Management System | Developed for Educational Institutions",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        copyright_label.pack(expand=True)
        
        # Version
        version_label = ctk.CTkLabel(
            footer_frame,
            text="Version 2.0",
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8"
        )
        version_label.pack(side="right", padx=20)
    
    def show_landing(self):
        """Show landing page"""
        self.clear_content()
        self.create_landing_content()
    
    def clear_content(self):
        """Clear main content area"""
        for widget in self.main_frame.winfo_children():
            if widget.winfo_name() != "!ctkframe" or "header" not in str(widget):
                continue
            # Keep header, remove others
            for child in widget.winfo_children():
                if child.winfo_name() == "!ctkframe":  # Main content frame
                    child.destroy()
    
    def student_login(self):
        """Open student login window"""
        import os
        self.destroy()
        os.system('python std_login.py')
    
    def company_login(self):
        """Open company login window"""
        import os
        self.destroy()
        os.system('python cmp_login.py')
    
    def tpo_login(self):
        """Open TPO login window"""
        import os
        self.destroy()
        os.system('python admin_dashboard_new.py')
    
    def admin_login(self):
        """Open admin login window"""
        import os
        self.destroy()
        os.system('python Admin_login.py')
        auth_window.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        self.conn.close()
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = PlacifyMe()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()