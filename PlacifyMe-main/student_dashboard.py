# student_dashboard.py - COMPLETE WORKING VERSION
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import os
from datetime import datetime
import sys
from PIL import Image, ImageTk, ImageDraw, ImageFont
import webbrowser
import shutil

class StudentDashboard:
    def __init__(self, student_id):
        self.student_id = student_id
        self.window = tk.Tk()
        self.window.title(f"PlacifyMe - Student Portal")
        self.window.geometry("1400x800")
        self.window.state("zoomed")
        
        # Modern color scheme
        self.PRIMARY = "#4f46e5"  # Indigo
        self.SECONDARY = "#3730a3"
        self.SUCCESS = "#059669"
        self.WARNING = "#d97706"
        self.DANGER = "#dc2626"
        self.LIGHT_BG = "#f8fafc"
        self.WHITE = "#ffffff"
        self.TEXT_DARK = "#1e293b"
        self.TEXT_LIGHT = "#64748b"
        
        # Profile photo variables
        self.profile_photo_path = None
        self.profile_photo_image = None
        self.profile_photo_label = None
        
        # Initialize
        self.init_database()
        self.load_student_data()
        self.setup_ui()
        
    def init_database(self):
        """Initialize database connection"""
        try:
            self.conn = sqlite3.connect('registration_student.db')
            self.cursor = self.conn.cursor()
            print(f"✅ Connected to database for student: {self.student_id}")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect: {str(e)}")
            sys.exit(1)
    
    def load_student_data(self):
        """Load all student data from database"""
        try:
            # Get data from student_signUP
            self.cursor.execute("SELECT * FROM student_signUP WHERE student_id=?", (self.student_id,))
            signup_data = self.cursor.fetchone()
            
            # Get data from student_table
            self.cursor.execute("SELECT * FROM student_table WHERE Registration_no=?", (self.student_id,))
            table_data = self.cursor.fetchone()
            
            # Initialize student info with defaults
            self.student_info = {
                'student_id': self.student_id,
                'name': self.student_id,
                'email': '',
                'phone': '',
                'gender': '',
                'branch': '',
                'year': '',
                'cgpa': 0.0,
                'cet_jee': 0,
                'company': '',
                'registration_no': self.student_id,
                'full_name': '',
                'address': '',
                'date_of_birth': '',
                'college_id': '',
                'skills': '',
                'linkedin': '',
                'github': '',
                'profile_summary': ''
            }
            
            # Update from signup table (if exists)
            if signup_data:
                if len(signup_data) > 0: self.student_info['name'] = signup_data[0] or self.student_id
                if len(signup_data) > 3: self.student_info['email'] = signup_data[3] or ''
                if len(signup_data) > 4: self.student_info['phone'] = signup_data[4] or ''
                if len(signup_data) > 5: self.student_info['branch'] = signup_data[5] or ''
                if len(signup_data) > 6: self.student_info['year'] = signup_data[6] or ''
                if len(signup_data) > 7: self.student_info['cgpa'] = signup_data[7] or 0.0
            
            # Update from student_table (if exists)
            if table_data:
                if len(table_data) > 0: self.student_info['full_name'] = table_data[0] or ''
                if len(table_data) > 1: self.student_info['email'] = table_data[1] or self.student_info['email']
                if len(table_data) > 2: self.student_info['phone'] = table_data[2] or self.student_info['phone']
                if len(table_data) > 3: self.student_info['gender'] = table_data[3] or ''
                if len(table_data) > 4: self.student_info['registration_no'] = table_data[4] or self.student_id
                if len(table_data) > 5: self.student_info['branch'] = table_data[5] or self.student_info['branch']
                if len(table_data) > 6: self.student_info['year'] = table_data[6] or self.student_info['year']
                if len(table_data) > 7: self.student_info['cgpa'] = table_data[7] or self.student_info['cgpa']
                if len(table_data) > 8: self.student_info['cet_jee'] = table_data[8] or 0
                if len(table_data) > 9: self.student_info['company'] = table_data[9] or ''
            
            # Ensure we have a name
            if not self.student_info['name'] and self.student_info['full_name']:
                self.student_info['name'] = self.student_info['full_name']
                
        except Exception as e:
            print(f"Error loading student data: {e}")
    
    def setup_ui(self):
        """Setup complete dashboard UI"""
        # Main container
        main_container = tk.Frame(self.window, bg=self.LIGHT_BG)
        main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self.create_sidebar(main_container)
        
        # Content area
        self.content_area = tk.Frame(main_container, bg=self.WHITE)
        self.content_area.pack(side="right", fill="both", expand=True, padx=2, pady=2)
        
        # Top bar with profile photo
        self.create_topbar_with_photo()
        
        # Default view
        self.show_dashboard()
    
    def create_sidebar(self, parent):
        """Create modern sidebar"""
        sidebar = tk.Frame(parent, bg=self.SECONDARY, width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo/Header
        header_frame = tk.Frame(sidebar, bg=self.SECONDARY)
        header_frame.pack(fill="x", pady=(30, 20), padx=20)
        
        tk.Label(header_frame, text="🎓", font=("Arial", 40), 
                bg=self.SECONDARY, fg="white").pack()
        tk.Label(header_frame, text="Student Portal", 
                font=("Arial", 16, "bold"), bg=self.SECONDARY, fg="white").pack(pady=5)
        tk.Label(header_frame, text=self.student_info['name'], 
                font=("Arial", 12), bg=self.SECONDARY, fg="#cbd5e1", wraplength=200).pack()
        
        # Navigation Menu
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("👤 My Profile", self.show_profile),
            ("📁 Documents", self.show_documents),
            ("💼 Job Applications", self.show_applications),
            ("🏢 Browse Jobs", self.show_jobs),
            ("📅 Interviews", self.show_interviews),
            ("📈 Placement Stats", self.show_stats),
            ("🔔 Notifications", self.show_notifications),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for icon_text, command in menu_items:
            btn = tk.Button(sidebar, text=f"  {icon_text}", 
                          font=("Arial", 12), bg=self.SECONDARY, fg="white",
                          bd=0, anchor="w", padx=25, pady=15, 
                          command=command, cursor="hand2")
            btn.pack(fill="x")
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#4f46e5"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.SECONDARY))
        
        # Logout button at bottom
        tk.Frame(sidebar, bg=self.SECONDARY, height=20).pack(fill="x", pady=(20, 10))
        tk.Button(sidebar, text="🚪 Logout", font=("Arial", 12, "bold"),
                 bg="#dc2626", fg="white", bd=0, padx=25, pady=15,
                 command=self.logout, cursor="hand2").pack(side="bottom", fill="x", pady=20)
    
    def create_topbar_with_photo(self):
        """Create top bar with circular profile photo"""
        topbar = tk.Frame(self.content_area, bg=self.WHITE, height=80)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        
        # Left: Welcome
        left_frame = tk.Frame(topbar, bg=self.WHITE)
        left_frame.pack(side="left", padx=30, pady=20)
        
        welcome_text = f"Welcome back, {self.student_info['name'].split()[0] if ' ' in self.student_info['name'] else self.student_info['name']}!"
        tk.Label(left_frame, text=welcome_text, 
                font=("Arial", 16, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w")
        
        # Quick stats
        stats = self.get_quick_stats()
        stats_text = f"📊 {stats['applications']} Applications | 💼 {stats['jobs']} Jobs | 🎯 {stats['interviews']} Interviews"
        tk.Label(left_frame, text=stats_text, 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(anchor="w", pady=(5, 0))
        
        # Right: Profile photo in circle
        right_frame = tk.Frame(topbar, bg=self.WHITE)
        right_frame.pack(side="right", padx=30, pady=15)
        
        # Create circular profile photo
        self.load_profile_photo()
        self.profile_photo_label = tk.Label(right_frame, image=self.profile_photo_image, 
                                           bg=self.WHITE, cursor="hand2")
        self.profile_photo_label.pack()
        self.profile_photo_label.bind("<Button-1>", lambda e: self.show_profile())
        
        # Student ID below photo
        tk.Label(right_frame, text=self.student_id, 
                font=("Arial", 10), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=(5, 0))
    
    def load_profile_photo(self):
        """Load profile photo from file system"""
        # Check for profile photo in profile_photos directory
        photo_dir = "profile_photos"
        if not os.path.exists(photo_dir):
            os.makedirs(photo_dir)
        
        # Check for existing photo
        photo_path = None
        for ext in ['.jpg', '.jpeg', '.png', '.gif']:
            temp_path = os.path.join(photo_dir, f"{self.student_id}{ext}")
            if os.path.exists(temp_path):
                photo_path = temp_path
                break
        
        if photo_path:
            try:
                # Load and create circular image
                image = Image.open(photo_path)
                image = image.resize((50, 50), Image.Resampling.LANCZOS)
                
                # Create circular mask
                mask = Image.new('L', (50, 50), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 50, 50), fill=255)
                
                # Apply mask
                result = Image.new('RGBA', (50, 50))
                result.paste(image, (0, 0), mask)
                
                self.profile_photo_image = ImageTk.PhotoImage(result)
                self.profile_photo_path = photo_path
                
            except Exception as e:
                print(f"Error loading profile photo: {e}")
                self.create_default_avatar()
        else:
            self.create_default_avatar()
    
    def create_default_avatar(self):
        """Create default circular avatar with initials"""
        # Get initials
        name = self.student_info.get('name', 'Student')
        initials = ''.join([n[0].upper() for n in name.split()[:2]]) if ' ' in name else name[0].upper()
        
        # Create image
        img = Image.new('RGB', (50, 50), color=self.PRIMARY)
        draw = ImageDraw.Draw(img)
        
        # Draw circle
        draw.ellipse((0, 0, 50, 50), fill=self.PRIMARY)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (50 - text_width) // 2
        y = (50 - text_height) // 2
        
        draw.text((x, y), initials, fill="white", font=font)
        
        # Create circular mask
        mask = Image.new('L', (50, 50), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 50, 50), fill=255)
        
        # Apply mask
        result = Image.new('RGBA', (50, 50))
        result.paste(img, (0, 0), mask)
        
        self.profile_photo_image = ImageTk.PhotoImage(result)
        self.profile_photo_path = None
    
    def upload_profile_photo(self):
        """Upload a new profile photo"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.gif"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Profile Photo",
            filetypes=file_types
        )
        
        if file_path:
            try:
                # Create profile_photos directory if it doesn't exist
                photo_dir = "profile_photos"
                if not os.path.exists(photo_dir):
                    os.makedirs(photo_dir)
                
                # Get file extension
                _, ext = os.path.splitext(file_path)
                ext = ext.lower()
                
                # Validate file type
                if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                    messagebox.showerror("Error", "Please select a valid image file (JPG, PNG, GIF)")
                    return
                
                # Remove existing photos
                for existing_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    old_path = os.path.join(photo_dir, f"{self.student_id}{existing_ext}")
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except:
                            pass
                
                # Copy new photo
                new_filename = f"{self.student_id}{ext}"
                new_filepath = os.path.join(photo_dir, new_filename)
                shutil.copy2(file_path, new_filepath)
                
                # Update photo display
                self.load_profile_photo()
                if self.profile_photo_label:
                    self.profile_photo_label.config(image=self.profile_photo_image)
                    self.profile_photo_label.image = self.profile_photo_image
                
                messagebox.showinfo("Success", "Profile photo updated successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload photo: {str(e)}")
    
    def get_quick_stats(self):
        """Get real-time statistics"""
        stats = {'applications': 0, 'jobs': 0, 'interviews': 0}
        
        try:
            # Applications count
            self.cursor.execute("SELECT COUNT(*) FROM student_applications WHERE student_id=?", 
                              (self.student_id,))
            stats['applications'] = self.cursor.fetchone()[0] or 0
            
            # Active jobs
            self.cursor.execute("SELECT COUNT(*) FROM job_postings WHERE status='Active'")
            stats['jobs'] = self.cursor.fetchone()[0] or 0
            
            # Interviews scheduled
            self.cursor.execute("SELECT COUNT(*) FROM interviews WHERE student_id=?", 
                              (self.student_id,))
            stats['interviews'] = self.cursor.fetchone()[0] or 0
            
        except Exception as e:
            print(f"Error getting stats: {e}")
        
        return stats
    
    def show_dashboard(self):
        """Show main dashboard"""
        self.clear_content()
        
        # Main dashboard container
        dashboard_frame = tk.Frame(self.content_area, bg=self.WHITE)
        dashboard_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Dashboard header
        header_frame = tk.Frame(dashboard_frame, bg=self.WHITE)
        header_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(header_frame, text="Student Dashboard", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left")
        
        today = datetime.now().strftime("%B %d, %Y")
        tk.Label(header_frame, text=f"📅 {today}", 
                font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="right")
        
        # Stats cards
        stats_frame = tk.Frame(dashboard_frame, bg=self.WHITE)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats = self.get_detailed_stats()
        
        cards = [
            ("Applications", stats['total_apps'], f"{stats['pending_apps']} pending", self.PRIMARY),
            ("Interviews", stats['total_interviews'], f"{stats['upcoming_interviews']} upcoming", self.SUCCESS),
            ("Offers", stats['offers'], f"{stats['offers_pending']} pending", self.WARNING),
            ("Placement Rate", f"{stats['placement_rate']}%", f"CGPA: {self.student_info.get('cgpa', 0.0)}", self.DANGER)
        ]
        
        for title, main_value, sub_value, color in cards:
            card = tk.Frame(stats_frame, bg="white", relief="solid", bd=1)
            card.pack(side="left", fill="both", expand=True, padx=10, pady=10, ipady=25)
            
            tk.Label(card, text=str(main_value), font=("Arial", 28, "bold"), 
                    bg="white", fg=color).pack(pady=(10, 5))
            tk.Label(card, text=title, font=("Arial", 12, "bold"), 
                    bg="white", fg=self.TEXT_DARK).pack()
            tk.Label(card, text=sub_value, font=("Arial", 10), 
                    bg="white", fg=self.TEXT_LIGHT).pack(pady=(5, 10))
        
        # Recent activity and jobs side by side
        mid_frame = tk.Frame(dashboard_frame, bg=self.WHITE)
        mid_frame.pack(fill="both", expand=True, pady=20)
        
        # Left: Recent Applications
        left_frame = tk.LabelFrame(mid_frame, text="📋 Recent Applications", 
                                  font=("Arial", 14, "bold"), bg=self.WHITE, 
                                  fg=self.TEXT_DARK, padx=20, pady=20)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.create_recent_applications(left_frame)
        
        # Right: Upcoming Interviews (REAL DATA)
        right_frame = tk.LabelFrame(mid_frame, text="📅 Upcoming Interviews", 
                                   font=("Arial", 14, "bold"), bg=self.WHITE, 
                                   fg=self.TEXT_DARK, padx=20, pady=20)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        self.create_upcoming_interviews_real(right_frame)
        
        # Available Jobs
        jobs_frame = tk.LabelFrame(dashboard_frame, text="🚀 Recommended Jobs", 
                                  font=("Arial", 14, "bold"), bg=self.WHITE, 
                                  fg=self.TEXT_DARK, padx=20, pady=20)
        jobs_frame.pack(fill="both", expand=True, pady=(0, 20))
        self.create_recommended_jobs(jobs_frame)
    
    def get_detailed_stats(self):
        """Get detailed statistics"""
        stats = {
            'total_apps': 0,
            'pending_apps': 0,
            'total_interviews': 0,
            'upcoming_interviews': 0,
            'offers': 0,
            'offers_pending': 0,
            'placement_rate': 0
        }
        
        try:
            # Application stats
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'Applied' OR status = 'Pending' THEN 1 ELSE 0 END) as pending
                FROM student_applications 
                WHERE student_id=?
            """, (self.student_id,))
            app_result = self.cursor.fetchone()
            if app_result:
                stats['total_apps'] = app_result[0] or 0
                stats['pending_apps'] = app_result[1] or 0
            
            # Interview stats
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN scheduled_date > datetime('now') THEN 1 ELSE 0 END) as upcoming
                FROM interviews 
                WHERE student_id=?
            """, (self.student_id,))
            interview_result = self.cursor.fetchone()
            if interview_result:
                stats['total_interviews'] = interview_result[0] or 0
                stats['upcoming_interviews'] = interview_result[1] or 0
            
            # Offer stats
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total_offers,
                    SUM(CASE WHEN offer_status = 'Pending' THEN 1 ELSE 0 END) as pending_offers
                FROM student_applications 
                WHERE student_id=? AND (status = 'Selected' OR offer_status IS NOT NULL)
            """, (self.student_id,))
            offer_result = self.cursor.fetchone()
            if offer_result:
                stats['offers'] = offer_result[0] or 0
                stats['offers_pending'] = offer_result[1] or 0
            
            # Calculate placement rate based on branch average
            if self.student_info.get('branch'):
                self.cursor.execute("""
                    SELECT AVG(CASE WHEN Company_Name IS NOT NULL THEN 1 ELSE 0 END) * 100
                    FROM student_table 
                    WHERE Branch=?
                """, (self.student_info['branch'],))
                rate_result = self.cursor.fetchone()
                if rate_result and rate_result[0]:
                    stats['placement_rate'] = int(rate_result[0])
                    
        except Exception as e:
            print(f"Error getting detailed stats: {e}")
        
        return stats
    
    def create_recent_applications(self, parent):
        """Show recent applications"""
        try:
            self.cursor.execute("""
                SELECT a.job_id, j.position, c.name, a.apply_date, a.status 
                FROM student_applications a
                LEFT JOIN job_postings j ON a.job_id = j.job_id
                LEFT JOIN company_login c ON j.company_id = c.id
                WHERE a.student_id = ?
                ORDER BY a.apply_date DESC
                LIMIT 5
            """, (self.student_id,))
            
            apps = self.cursor.fetchall()
            
            if apps:
                for job_id, position, company, date, status in apps:
                    app_frame = tk.Frame(parent, bg=self.LIGHT_BG)
                    app_frame.pack(fill="x", pady=8, padx=10, ipady=10)
                    
                    # Application header
                    header = tk.Frame(app_frame, bg=self.LIGHT_BG)
                    header.pack(fill="x", padx=15, pady=5)
                    
                    tk.Label(header, text=position, 
                            font=("Arial", 11, "bold"), bg=self.LIGHT_BG, fg=self.TEXT_DARK).pack(side="left")
                    
                    # Status badge
                    status_colors = {
                        'Applied': '#3b82f6',
                        'Shortlisted': '#10b981',
                        'Selected': '#059669',
                        'Rejected': '#dc2626',
                        'Pending': '#d97706'
                    }
                    status_color = status_colors.get(status, '#6b7280')
                    tk.Label(header, text=status, font=("Arial", 10, "bold"),
                            bg=status_color, fg="white", padx=10, pady=3).pack(side="right")
                    
                    # Application details
                    details = tk.Frame(app_frame, bg=self.LIGHT_BG)
                    details.pack(fill="x", padx=15, pady=(0, 5))
                    
                    tk.Label(details, text=f"🏢 {company}", 
                            font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(side="left", padx=(0, 15))
                    tk.Label(details, text=f"📅 {date[:10]}", 
                            font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(side="left")
                    
            else:
                tk.Label(parent, text="No applications yet", 
                        font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=30)
                
        except Exception as e:
            print(f"Error loading applications: {e}")
            tk.Label(parent, text="Error loading applications", 
                    font=("Arial", 12), bg=self.WHITE, fg=self.DANGER).pack(pady=30)
        
        # View all button
        tk.Button(parent, text="View All Applications →", 
                 font=("Arial", 11), bg=self.PRIMARY, fg="white",
                 command=self.show_applications, cursor="hand2", 
                 padx=20, pady=10).pack(pady=10)
    
    def create_upcoming_interviews_real(self, parent):
        """Show REAL upcoming interviews"""
        try:
            self.cursor.execute("""
                SELECT i.interview_id, c.name, j.position, i.scheduled_date, 
                       i.status, i.venue, i.interview_mode
                FROM interviews i
                LEFT JOIN job_postings j ON i.job_id = j.job_id
                LEFT JOIN company_login c ON i.company_id = c.id
                WHERE i.student_id = ? AND i.scheduled_date > datetime('now')
                ORDER BY i.scheduled_date ASC
                LIMIT 3
            """, (self.student_id,))
            
            interviews = self.cursor.fetchall()
            
            if interviews:
                for interview in interviews:
                    interview_id, company, position, scheduled, status, venue, mode = interview
                    
                    interview_frame = tk.Frame(parent, bg=self.LIGHT_BG)
                    interview_frame.pack(fill="x", pady=8, padx=10, ipady=10)
                    
                    # Interview header
                    tk.Label(interview_frame, text=position, 
                            font=("Arial", 11, "bold"), bg=self.LIGHT_BG, fg=self.TEXT_DARK).pack(anchor="w", padx=15, pady=5)
                    
                    # Company
                    tk.Label(interview_frame, text=f"🏢 {company}", 
                            font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15)
                    
                    # Date and time
                    if scheduled:
                        try:
                            formatted_date = datetime.strptime(scheduled, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %I:%M %p")
                            tk.Label(interview_frame, text=f"📅 {formatted_date}", 
                                    font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15)
                        except:
                            tk.Label(interview_frame, text=f"📅 {scheduled[:10]}", 
                                    font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15)
                    
                    # Venue and mode
                    if venue:
                        tk.Label(interview_frame, text=f"📍 {venue} ({mode})", 
                                font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15)
                    
                    # Status
                    status_color = '#10b981' if status == 'Scheduled' else '#f59e0b'
                    tk.Label(interview_frame, text=f"Status: {status}", 
                            font=("Arial", 10, "bold"), bg=self.LIGHT_BG, fg=status_color).pack(anchor="w", padx=15, pady=(5, 0))
                    
            else:
                tk.Label(parent, text="No upcoming interviews scheduled", 
                        font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=30)
                
        except Exception as e:
            print(f"Error loading interviews: {e}")
            tk.Label(parent, text="No interview data available", 
                    font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=30)
        
        # View all interviews button
        tk.Button(parent, text="View All Interviews →", 
                 font=("Arial", 11), bg=self.PRIMARY, fg="white",
                 command=self.show_interviews, cursor="hand2", 
                 padx=20, pady=10).pack(pady=10)
    
    def create_recommended_jobs(self, parent):
        """Show recommended jobs based on student profile"""
        try:
            # Get jobs matching student's branch
            branch = self.student_info.get('branch', '')
            cgpa = self.student_info.get('cgpa', 0.0)
            
            if branch:
                self.cursor.execute("""
                    SELECT j.job_id, j.position, c.name, j.salary, j.location, j.posting_date,
                           j.cgpa_cutoff, j.eligible_branches
                    FROM job_postings j
                    LEFT JOIN company_login c ON j.company_id = c.id
                    WHERE j.status = 'Active' 
                    AND (j.eligible_branches LIKE ? OR j.eligible_branches = '' OR j.eligible_branches IS NULL)
                    AND (j.cgpa_cutoff <= ? OR j.cgpa_cutoff = 0)
                    ORDER BY j.posting_date DESC
                    LIMIT 5
                """, (f'%{branch}%', cgpa))
            else:
                self.cursor.execute("""
                    SELECT j.job_id, j.position, c.name, j.salary, j.location, j.posting_date
                    FROM job_postings j
                    LEFT JOIN company_login c ON j.company_id = c.id
                    WHERE j.status = 'Active'
                    ORDER BY j.posting_date DESC
                    LIMIT 5
                """)
            
            jobs = self.cursor.fetchall()
            
            if jobs:
                for job_id, position, company, salary, location, date, cutoff, branches in jobs:
                    job_frame = tk.Frame(parent, bg="white", relief="solid", bd=1)
                    job_frame.pack(fill="x", pady=8, padx=10, ipady=15)
                    
                    # Top row
                    top_row = tk.Frame(job_frame, bg="white")
                    top_row.pack(fill="x", padx=15, pady=5)
                    
                    tk.Label(top_row, text=position, font=("Arial", 13, "bold"), 
                            bg="white", fg=self.TEXT_DARK).pack(side="left")
                    
                    # Check if already applied
                    self.cursor.execute("SELECT COUNT(*) FROM student_applications WHERE student_id=? AND job_id=?", 
                                      (self.student_id, job_id))
                    applied = self.cursor.fetchone()[0] > 0
                    
                    if applied:
                        tk.Label(top_row, text="✓ Applied", font=("Arial", 10, "bold"), 
                                bg=self.SUCCESS, fg="white", padx=10, pady=3).pack(side="right")
                    else:
                        tk.Button(top_row, text="Apply Now", font=("Arial", 10, "bold"), 
                                 bg=self.PRIMARY, fg="white", padx=15, pady=5,
                                 command=lambda jid=job_id: self.apply_job(jid), cursor="hand2").pack(side="right")
                    
                    # Middle row - Company and location
                    middle_row = tk.Frame(job_frame, bg="white")
                    middle_row.pack(fill="x", padx=15, pady=5)
                    
                    tk.Label(middle_row, text=f"🏢 {company}", 
                            font=("Arial", 11), bg="white", fg=self.TEXT_DARK).pack(side="left", padx=(0, 20))
                    
                    if location:
                        tk.Label(middle_row, text=f"📍 {location}", 
                                font=("Arial", 11), bg="white", fg=self.TEXT_LIGHT).pack(side="left", padx=(0, 20))
                    
                    if salary:
                        tk.Label(middle_row, text=f"💰 {salary}", 
                                font=("Arial", 11), bg="white", fg=self.SUCCESS).pack(side="left")
                    
                    # Bottom row - Requirements
                    bottom_row = tk.Frame(job_frame, bg="white")
                    bottom_row.pack(fill="x", padx=15, pady=(5, 0))
                    
                    if cutoff and cutoff > 0:
                        tk.Label(bottom_row, text=f"🎯 Min CGPA: {cutoff}", 
                                font=("Arial", 10), bg="white", fg=self.WARNING).pack(side="left", padx=(0, 15))
                    
                    if date:
                        tk.Label(bottom_row, text=f"📅 Posted: {date[:10]}", 
                                font=("Arial", 10), bg="white", fg=self.TEXT_LIGHT).pack(side="left")
                    
                    # View details button
                    tk.Button(job_frame, text="View Details", font=("Arial", 10), 
                             bg=self.LIGHT_BG, fg=self.PRIMARY, bd=1,
                             command=lambda jid=job_id: self.view_job_details(jid),
                             cursor="hand2", padx=10, pady=3).pack(anchor="e", padx=15, pady=(5, 0))
                    
            else:
                tk.Label(parent, text="No jobs available matching your profile", 
                        font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=30)
                
        except Exception as e:
            print(f"Error loading jobs: {e}")
            tk.Label(parent, text="Error loading jobs", 
                    font=("Arial", 12), bg=self.WHITE, fg=self.DANGER).pack(pady=30)
        
        # Browse more jobs button
        tk.Button(parent, text="Browse All Jobs →", 
                 font=("Arial", 11), bg=self.PRIMARY, fg="white",
                 command=self.show_jobs, cursor="hand2", 
                 padx=20, pady=10).pack(pady=10)
    
    def apply_job(self, job_id):
        """Apply for a job"""
        try:
            # Check if already applied
            self.cursor.execute("SELECT COUNT(*) FROM student_applications WHERE student_id=? AND job_id=?", 
                              (self.student_id, job_id))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showinfo("Already Applied", "You have already applied for this job!")
                return
            
            # Get job details
            self.cursor.execute("""
                SELECT company_id, company_name, position 
                FROM job_postings 
                WHERE job_id=?
            """, (job_id,))
            job_details = self.cursor.fetchone()
            
            if not job_details:
                messagebox.showerror("Error", "Job not found!")
                return
            
            company_id, company_name, position = job_details
            
            # Apply
            apply_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("""
                INSERT INTO student_applications 
                (student_id, job_id, company_id, company_name, position, apply_date, status)
                VALUES (?, ?, ?, ?, ?, ?, 'Applied')
            """, (self.student_id, job_id, company_id, company_name, position, apply_date))
            
            self.conn.commit()
            
            # Create notification
            self.cursor.execute("""
                INSERT INTO notifications (user_id, user_type, title, message)
                VALUES (?, 'student', 'Application Submitted', ?)
            """, (self.student_id, f"You applied for {position} at {company_name}"))
            
            self.conn.commit()
            
            messagebox.showinfo("Success", "Application submitted successfully!")
            
            # Send notification to company
            self.cursor.execute("""
                INSERT INTO notifications (user_id, user_type, title, message)
                VALUES (?, 'company', 'New Application', ?)
            """, (company_id, f"New application for {position} from {self.student_info['name']}"))
            
            self.conn.commit()
            
            # Refresh dashboard
            self.show_dashboard()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply: {str(e)}")
    
    def view_job_details(self, job_id):
        """View job details"""
        try:
            self.cursor.execute("""
                SELECT j.*, c.email, c.phone, c.hr_contact, c.website
                FROM job_postings j
                LEFT JOIN company_login c ON j.company_id = c.id
                WHERE j.job_id=?
            """, (job_id,))
            
            job = self.cursor.fetchone()
            
            if job:
                # Create details window
                details_window = tk.Toplevel(self.window)
                details_window.title("Job Details")
                details_window.geometry("600x500")
                details_window.configure(bg=self.WHITE)
                
                # Job title
                tk.Label(details_window, text=job[3],  # position
                        font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(20, 10))
                
                # Company
                tk.Label(details_window, text=f"Company: {job[2]}",
                        font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=5)
                
                # Salary
                if job[4]:  # salary
                    tk.Label(details_window, text=f"Salary: {job[4]}",
                            font=("Arial", 12), bg=self.WHITE, fg=self.SUCCESS).pack(pady=5)
                
                # Location
                if job[5]:  # location
                    tk.Label(details_window, text=f"Location: {job[5]}",
                            font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=5)
                
                # Requirements
                if job[7]:  # requirements
                    tk.Label(details_window, text="Requirements:", 
                            font=("Arial", 12, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(15, 5))
                    
                    req_frame = tk.Frame(details_window, bg=self.WHITE)
                    req_frame.pack(fill="x", padx=50)
                    tk.Label(req_frame, text=job[7], wraplength=500, justify="left",
                            font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack()
                
                # Description
                if job[6]:  # description
                    tk.Label(details_window, text="Description:", 
                            font=("Arial", 12, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(15, 5))
                    
                    desc_frame = tk.Frame(details_window, bg=self.WHITE)
                    desc_frame.pack(fill="x", padx=50)
                    tk.Label(desc_frame, text=job[6], wraplength=500, justify="left",
                            font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack()
                
                # Check if applied
                self.cursor.execute("SELECT COUNT(*) FROM student_applications WHERE student_id=? AND job_id=?", 
                                  (self.student_id, job_id))
                applied = self.cursor.fetchone()[0] > 0
                
                # Apply button
                if not applied:
                    tk.Button(details_window, text="Apply Now", 
                             font=("Arial", 12, "bold"), bg=self.PRIMARY, fg="white",
                             command=lambda: [self.apply_job(job_id), details_window.destroy()],
                             padx=30, pady=10, cursor="hand2").pack(pady=20)
                else:
                    tk.Label(details_window, text="✓ Already Applied", 
                            font=("Arial", 12, "bold"), bg=self.WHITE, fg=self.SUCCESS).pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load job details: {str(e)}")
    
    def show_profile(self):
        """Show COMPLETE editable profile page"""
        self.clear_content()
        
        profile_frame = tk.Frame(self.content_area, bg=self.WHITE)
        profile_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Profile header with large profile photo
        header_frame = tk.Frame(profile_frame, bg=self.WHITE)
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Left: Large profile photo
        left_header = tk.Frame(header_frame, bg=self.WHITE)
        left_header.pack(side="left")
        
        # Load large profile photo
        large_photo = self.get_large_profile_photo()
        photo_label = tk.Label(left_header, image=large_photo, bg=self.WHITE, cursor="hand2")
        photo_label.pack()
        photo_label.image = large_photo
        
        tk.Button(left_header, text="Change Photo", 
                 font=("Arial", 10), bg=self.PRIMARY, fg="white",
                 command=self.upload_profile_photo, cursor="hand2", 
                 padx=15, pady=5).pack(pady=10)
        
        # Right: Profile info header
        right_header = tk.Frame(header_frame, bg=self.WHITE)
        right_header.pack(side="left", padx=30, fill="both", expand=True)
        
        tk.Label(right_header, text="My Profile", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w")
        
        tk.Label(right_header, text="Manage your personal and academic information", 
                font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(anchor="w", pady=(5, 0))
        
        # Profile content with tabs
        notebook = ttk.Notebook(profile_frame)
        notebook.pack(fill="both", expand=True)
        
        # Tab 1: Personal Information (EDITABLE)
        personal_frame = tk.Frame(notebook, bg=self.WHITE)
        notebook.add(personal_frame, text="Personal Information")
        self.create_editable_personal_info(personal_frame)
        
        # Tab 2: Academic Information (EDITABLE)
        academic_frame = tk.Frame(notebook, bg=self.WHITE)
        notebook.add(academic_frame, text="Academic Information")
        self.create_editable_academic_info(academic_frame)
        
        # Tab 3: Career Information (EDITABLE)
        career_frame = tk.Frame(notebook, bg=self.WHITE)
        notebook.add(career_frame, text="Career Information")
        self.create_editable_career_info(career_frame)
    
    def get_large_profile_photo(self, size=(120, 120)):
        """Get large circular profile photo"""
        # Check for existing photo
        photo_dir = "profile_photos"
        photo_path = None
        
        for ext in ['.jpg', '.jpeg', '.png', '.gif']:
            temp_path = os.path.join(photo_dir, f"{self.student_id}{ext}")
            if os.path.exists(temp_path):
                photo_path = temp_path
                break
        
        if photo_path:
            try:
                # Load and create circular image
                image = Image.open(photo_path)
                image = image.resize(size, Image.Resampling.LANCZOS)
                
                # Create circular mask
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, size[0], size[1]), fill=255)
                
                # Apply mask
                result = Image.new('RGBA', size)
                result.paste(image, (0, 0), mask)
                
                return ImageTk.PhotoImage(result)
                
            except Exception as e:
                print(f"Error loading large profile photo: {e}")
        
        # Create default avatar
        name = self.student_info.get('name', 'Student')
        initials = ''.join([n[0].upper() for n in name.split()[:2]]) if ' ' in name else name[0].upper()
        
        img = Image.new('RGB', size, color=self.PRIMARY)
        draw = ImageDraw.Draw(img)
        
        # Draw circle
        draw.ellipse((0, 0, size[0], size[1]), fill=self.PRIMARY)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), initials, fill="white", font=font)
        
        # Create circular mask
        mask = Image.new('L', size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        # Apply mask
        result = Image.new('RGBA', size)
        result.paste(img, (0, 0), mask)
        
        return ImageTk.PhotoImage(result)
    
    def create_editable_personal_info(self, parent):
        """Create editable personal information form"""
        # Create a scrollable frame
        canvas = tk.Canvas(parent, bg=self.WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        form_frame = tk.Frame(scrollable_frame, bg=self.WHITE)
        form_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        # Form fields - ALL EDITABLE
        fields = [
            ("Full Name:", "name", self.student_info.get('name', ''), True),
            ("Email Address:", "email", self.student_info.get('email', ''), True),
            ("Phone Number:", "phone", self.student_info.get('phone', ''), True),
            ("Gender:", "gender", self.student_info.get('gender', ''), True),
            ("Date of Birth:", "dob", self.student_info.get('date_of_birth', ''), True),
            ("Address:", "address", self.student_info.get('address', ''), True),
            ("LinkedIn URL:", "linkedin", self.student_info.get('linkedin', ''), True),
            ("GitHub URL:", "github", self.student_info.get('github', ''), True),
            ("Profile Summary:", "summary", self.student_info.get('profile_summary', ''), True)
        ]
        
        self.personal_entries = {}
        
        for i, (label, key, value, editable) in enumerate(fields):
            row = tk.Frame(form_frame, bg=self.WHITE)
            row.pack(fill="x", pady=12)
            
            tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK, width=20, anchor="w").pack(side="left")
            
            if key == "gender":
                # Dropdown for gender
                gender_var = tk.StringVar(value=value)
                options = ["Male", "Female", "Other", "Prefer not to say"]
                entry = ttk.Combobox(row, textvariable=gender_var, values=options, 
                                    state="readonly", width=30, font=("Arial", 11))
                entry.pack(side="left", padx=10)
                self.personal_entries[key] = gender_var
                
            elif key == "summary":
                # Text area for summary
                text_frame = tk.Frame(row, bg=self.WHITE)
                text_frame.pack(side="left", padx=10, fill="x", expand=True)
                
                scrollbar_inner = tk.Scrollbar(text_frame)
                scrollbar_inner.pack(side="right", fill="y")
                
                entry = tk.Text(text_frame, height=4, width=40, font=("Arial", 11),
                               yscrollcommand=scrollbar_inner.set)
                entry.insert("1.0", value)
                entry.pack(side="left", fill="both", expand=True)
                scrollbar_inner.config(command=entry.yview)
                self.personal_entries[key] = entry
                
            else:
                # Regular text entry
                entry = tk.Entry(row, font=("Arial", 11), width=35)
                entry.insert(0, value)
                entry.pack(side="left", padx=10)
                self.personal_entries[key] = entry
        
        # Save button - placed below all fields in scrollable area
        button_frame = tk.Frame(form_frame, bg=self.WHITE)
        button_frame.pack(fill="x", pady=30)
        
        tk.Button(button_frame, text="Save Personal Information", 
                 font=("Arial", 12, "bold"), bg=self.PRIMARY, fg="white",
                 command=self.save_personal_info, cursor="hand2", 
                 padx=30, pady=12).pack()
    
    def create_editable_academic_info(self, parent):
        """Create editable academic information form"""
        # Create a scrollable frame
        canvas = tk.Canvas(parent, bg=self.WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        form_frame = tk.Frame(scrollable_frame, bg=self.WHITE)
        form_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        # Form fields - ALL EDITABLE
        fields = [
            ("Student ID:", "student_id", self.student_info.get('student_id', ''), False),
            ("Registration No:", "registration_no", self.student_info.get('registration_no', ''), True),
            ("College ID:", "college_id", self.student_info.get('college_id', ''), True),
            ("Branch:", "branch", self.student_info.get('branch', ''), True),
            ("Year:", "year", self.student_info.get('year', ''), True),
            ("CGPA:", "cgpa", str(self.student_info.get('cgpa', 0.0)), True),
            ("CET/JEE Score:", "cet_jee", str(self.student_info.get('cet_jee', 0)), True),
            ("Skills (comma separated):", "skills", self.student_info.get('skills', ''), True)
        ]
        
        self.academic_entries = {}
        
        for label, key, value, editable in fields:
            row = tk.Frame(form_frame, bg=self.WHITE)
            row.pack(fill="x", pady=12)
            
            tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK, width=25, anchor="w").pack(side="left")
            
            if key == "branch":
                # Dropdown for branch
                branch_var = tk.StringVar(value=value)
                options = ["IT", "EXTC", "COMP", "MECH", "ELECTRICAL", "CHEMICAL", "CIVIL"]
                entry = ttk.Combobox(row, textvariable=branch_var, values=options, 
                                    state="readonly", width=30, font=("Arial", 11))
                entry.pack(side="left", padx=10)
                self.academic_entries[key] = branch_var
                
            elif key == "year":
                # Dropdown for year
                year_var = tk.StringVar(value=value)
                options = ["FE", "SE", "TE", "BE", "Final Year"]
                entry = ttk.Combobox(row, textvariable=year_var, values=options, 
                                    state="readonly", width=30, font=("Arial", 11))
                entry.pack(side="left", padx=10)
                self.academic_entries[key] = year_var
                
            else:
                # Regular text entry
                state = "normal" if editable else "readonly"
                entry = tk.Entry(row, font=("Arial", 11), width=35, state=state)
                entry.insert(0, value)
                entry.pack(side="left", padx=10)
                self.academic_entries[key] = entry
        
        # Save button - with better sizing
        button_frame = tk.Frame(form_frame, bg=self.WHITE)
        button_frame.pack(fill="x", pady=30)
        
        tk.Button(button_frame, text="Save Academic Information", 
                 font=("Arial", 12, "bold"), bg=self.PRIMARY, fg="white",
                 command=self.save_academic_info, cursor="hand2", 
                 padx=35, pady=15).pack()
    
    def create_editable_career_info(self, parent):
        """Create editable career information form"""
        form_frame = tk.Frame(parent, bg=self.WHITE, padx=50, pady=30)
        form_frame.pack(fill="both", expand=True)
        
        # Form fields
        fields = [
            ("Current Company:", "company", self.student_info.get('company', ''), True),
            ("Expected Salary (₹):", "expected_salary", "", True),
            ("Preferred Location:", "preferred_location", "", True),
            ("Job Type Preference:", "job_type", "", True),
            ("Notice Period (days):", "notice_period", "", True),
            ("Resume Headline:", "resume_headline", "", True)
        ]
        
        self.career_entries = {}
        
        for label, key, value, editable in fields:
            row = tk.Frame(form_frame, bg=self.WHITE)
            row.pack(fill="x", pady=12)
            
            tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK, width=25, anchor="w").pack(side="left")
            
            if key == "job_type":
                # Dropdown for job type
                job_var = tk.StringVar(value=value)
                options = ["Full-time", "Internship", "Part-time", "Contract", "Remote"]
                entry = ttk.Combobox(row, textvariable=job_var, values=options, 
                                    state="readonly", width=30, font=("Arial", 11))
                entry.pack(side="left", padx=10)
                self.career_entries[key] = job_var
            else:
                # Regular text entry
                entry = tk.Entry(row, font=("Arial", 11), width=35)
                if value:
                    entry.insert(0, value)
                entry.pack(side="left", padx=10)
                self.career_entries[key] = entry
        
        # Save button
        tk.Button(form_frame, text="Save Career Information", 
                 font=("Arial", 12, "bold"), bg=self.PRIMARY, fg="white",
                 command=self.save_career_info, cursor="hand2", 
                 padx=30, pady=12).pack(pady=30)
    
    def save_personal_info(self):
        """Save personal information"""
        try:
            # Get values from entries
            name = self.personal_entries['name'].get() if isinstance(self.personal_entries['name'], tk.Entry) else self.personal_entries['name']
            email = self.personal_entries['email'].get() if isinstance(self.personal_entries['email'], tk.Entry) else self.personal_entries['email']
            phone = self.personal_entries['phone'].get() if isinstance(self.personal_entries['phone'], tk.Entry) else self.personal_entries['phone']
            gender = self.personal_entries['gender'].get() if isinstance(self.personal_entries['gender'], tk.StringVar) else self.personal_entries['gender']
            dob = self.personal_entries['dob'].get() if isinstance(self.personal_entries['dob'], tk.Entry) else self.personal_entries['dob']
            address = self.personal_entries['address'].get() if isinstance(self.personal_entries['address'], tk.Entry) else self.personal_entries['address']
            linkedin = self.personal_entries['linkedin'].get() if isinstance(self.personal_entries['linkedin'], tk.Entry) else self.personal_entries['linkedin']
            github = self.personal_entries['github'].get() if isinstance(self.personal_entries['github'], tk.Entry) else self.personal_entries['github']
            summary = self.personal_entries['summary'].get("1.0", "end-1c") if isinstance(self.personal_entries['summary'], tk.Text) else self.personal_entries['summary']
            
            # Update student_signUP
            self.cursor.execute("""
                UPDATE student_signUP 
                SET name=?, email=?, phone=?
                WHERE student_id=?
            """, (name, email, phone, self.student_id))
            
            # Update student_table
            self.cursor.execute("SELECT COUNT(*) FROM student_table WHERE Registration_no=?", (self.student_id,))
            if self.cursor.fetchone()[0] > 0:
                self.cursor.execute("""
                    UPDATE student_table 
                    SET Full_name=?, Email_Id=?, Phone_no=?, Gender=?
                    WHERE Registration_no=?
                """, (name, email, phone, gender, self.student_id))
            else:
                self.cursor.execute("""
                    INSERT INTO student_table (Full_name, Email_Id, Phone_no, Gender, Registration_no)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, email, phone, gender, self.student_id))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Personal information saved successfully!")
            self.load_student_data()  # Reload data
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save personal information: {str(e)}")
    
    def save_academic_info(self):
        """Save academic information"""
        try:
            # Get values from entries
            registration_no = self.academic_entries['registration_no'].get() if isinstance(self.academic_entries['registration_no'], tk.Entry) else self.academic_entries['registration_no']
            college_id = self.academic_entries['college_id'].get() if isinstance(self.academic_entries['college_id'], tk.Entry) else self.academic_entries['college_id']
            branch = self.academic_entries['branch'].get() if isinstance(self.academic_entries['branch'], tk.StringVar) else self.academic_entries['branch']
            year = self.academic_entries['year'].get() if isinstance(self.academic_entries['year'], tk.StringVar) else self.academic_entries['year']
            cgpa = float(self.academic_entries['cgpa'].get()) if self.academic_entries['cgpa'].get() else 0.0
            cet_jee = float(self.academic_entries['cet_jee'].get()) if self.academic_entries['cet_jee'].get() else 0.0
            skills = self.academic_entries['skills'].get() if isinstance(self.academic_entries['skills'], tk.Entry) else self.academic_entries['skills']
            
            # Update student_signUP
            self.cursor.execute("""
                UPDATE student_signUP 
                SET branch=?, year=?, cgpa=?
                WHERE student_id=?
            """, (branch, year, cgpa, self.student_id))
            
            # Update student_table
            self.cursor.execute("SELECT COUNT(*) FROM student_table WHERE Registration_no=?", (self.student_id,))
            if self.cursor.fetchone()[0] > 0:
                self.cursor.execute("""
                    UPDATE student_table 
                    SET Branch=?, Year=?, CGPA=?, CET_JEE=?
                    WHERE Registration_no=?
                """, (branch, year, cgpa, cet_jee, self.student_id))
            else:
                self.cursor.execute("""
                    INSERT INTO student_table (Registration_no, Branch, Year, CGPA, CET_JEE)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.student_id, branch, year, cgpa, cet_jee))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Academic information saved successfully!")
            self.load_student_data()  # Reload data
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for CGPA and CET/JEE Score")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save academic information: {str(e)}")
    
    def save_career_info(self):
        """Save career information"""
        try:
            # Get values from entries
            company = self.career_entries['company'].get() if isinstance(self.career_entries['company'], tk.Entry) else self.career_entries['company']
            
            # Update student_table with company
            self.cursor.execute("SELECT COUNT(*) FROM student_table WHERE Registration_no=?", (self.student_id,))
            if self.cursor.fetchone()[0] > 0:
                self.cursor.execute("""
                    UPDATE student_table 
                    SET Company_Name=?
                    WHERE Registration_no=?
                """, (company, self.student_id))
            else:
                self.cursor.execute("""
                    INSERT INTO student_table (Registration_no, Company_Name)
                    VALUES (?, ?)
                """, (self.student_id, company))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Career information saved successfully!")
            self.load_student_data()  # Reload data
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save career information: {str(e)}")
    
    def show_documents(self):
        """Show documents page with REAL file management"""
        self.clear_content()
        
        docs_frame = tk.Frame(self.content_area, bg=self.WHITE)
        docs_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(docs_frame, text="My Documents", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Create documents directory if it doesn't exist
        doc_dir = f"student_documents/{self.student_id}"
        if not os.path.exists(doc_dir):
            os.makedirs(doc_dir)
        
        # Upload section
        upload_frame = tk.LabelFrame(docs_frame, text="Upload Documents", 
                                    font=("Arial", 14, "bold"), bg=self.WHITE, 
                                    fg=self.TEXT_DARK, padx=20, pady=20)
        upload_frame.pack(fill="x", pady=(0, 20))
        
        # Document type selection
        type_frame = tk.Frame(upload_frame, bg=self.WHITE)
        type_frame.pack(fill="x", pady=10)
        
        tk.Label(type_frame, text="Document Type:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left", padx=(0, 10))
        
        self.doc_type_var = tk.StringVar(value="Resume")
        doc_types = ["Resume", "10th Marksheet", "12th Marksheet", "Degree Certificate", 
                    "ID Proof", "Other Certificate", "Cover Letter"]
        doc_type_menu = ttk.Combobox(type_frame, textvariable=self.doc_type_var, 
                                    values=doc_types, state="readonly", width=20)
        doc_type_menu.pack(side="left", padx=(0, 20))
        
        # Upload button
        tk.Button(type_frame, text="📁 Choose File", 
                 font=("Arial", 11), bg=self.PRIMARY, fg="white",
                 command=self.upload_document_real, cursor="hand2", 
                 padx=20, pady=8).pack(side="left")
        
        # Document list section
        list_frame = tk.LabelFrame(docs_frame, text="Uploaded Documents", 
                                  font=("Arial", 14, "bold"), bg=self.WHITE, 
                                  fg=self.TEXT_DARK, padx=20, pady=20)
        list_frame.pack(fill="both", expand=True)
        
        # Create table for documents
        columns = ("Document Name", "Type", "Size", "Upload Date", "Actions")
        self.doc_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        col_widths = [250, 120, 80, 100, 150]
        for i, col in enumerate(columns):
            self.doc_tree.heading(col, text=col)
            self.doc_tree.column(col, width=col_widths[i])
        
        # Load documents
        self.load_documents_list()
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.doc_tree.yview)
        self.doc_tree.configure(yscrollcommand=scrollbar.set)
        
        self.doc_tree.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Context menu for documents
        self.doc_menu = tk.Menu(self.window, tearoff=0)
        self.doc_menu.add_command(label="Open", command=self.open_document)
        self.doc_menu.add_command(label="Rename", command=self.rename_document)
        self.doc_menu.add_command(label="Delete", command=self.delete_document)
        
        self.doc_tree.bind("<Button-3>", self.show_doc_context_menu)
    
    def upload_document_real(self):
        """Upload document to local file system (NO DATABASE PATH SAVING)"""
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Image files", "*.jpg *.jpeg *.png"),
                ("Word documents", "*.doc *.docx"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Get file info
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                
                # Check file size (max 20MB)
                if file_size > 20 * 1024 * 1024:
                    messagebox.showerror("Error", "File size must be less than 20MB")
                    return
                
                # Create student directory
                student_dir = f"student_documents/{self.student_id}"
                if not os.path.exists(student_dir):
                    os.makedirs(student_dir)
                
                # Create type subdirectory
                doc_type = self.doc_type_var.get().replace(" ", "_").lower()
                type_dir = os.path.join(student_dir, doc_type)
                if not os.path.exists(type_dir):
                    os.makedirs(type_dir)
                
                # Copy file to destination
                dest_path = os.path.join(type_dir, file_name)
                
                # Handle duplicate files
                counter = 1
                name, ext = os.path.splitext(file_name)
                while os.path.exists(dest_path):
                    new_name = f"{name}_{counter}{ext}"
                    dest_path = os.path.join(type_dir, new_name)
                    counter += 1
                
                shutil.copy2(file_path, dest_path)
                
                messagebox.showinfo("Success", f"Document uploaded successfully!\n\nSaved to: {dest_path}")
                
                # Refresh document list
                self.load_documents_list()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload document: {str(e)}")
    
    def load_documents_list(self):
        """Load documents from local file system"""
        # Clear existing items
        for item in self.doc_tree.get_children():
            self.doc_tree.delete(item)
        
        student_dir = f"student_documents/{self.student_id}"
        
        if os.path.exists(student_dir):
            for root, dirs, files in os.walk(student_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, student_dir)
                    
                    # Get file info
                    file_size = os.path.getsize(file_path)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d")
                    
                    # Get document type from directory name
                    doc_type = os.path.basename(os.path.dirname(rel_path)).replace("_", " ").title()
                    if doc_type == self.student_id:
                        doc_type = "General"
                    
                    # Format file size
                    if file_size < 1024:
                        size_str = f"{file_size} B"
                    elif file_size < 1024 * 1024:
                        size_str = f"{file_size/1024:.1f} KB"
                    else:
                        size_str = f"{file_size/(1024*1024):.1f} MB"
                    
                    # Add to tree
                    self.doc_tree.insert('', 'end', values=(
                        file, doc_type, size_str, mod_time, "View/Delete"
                    ), tags=(file_path,))
    
    def show_doc_context_menu(self, event):
        """Show context menu for documents"""
        item = self.doc_tree.identify_row(event.y)
        if item:
            self.doc_tree.selection_set(item)
            self.selected_doc_path = self.doc_tree.item(item, "tags")[0]
            self.doc_menu.post(event.x_root, event.y_root)
    
    def open_document(self):
        """Open selected document"""
        if hasattr(self, 'selected_doc_path') and self.selected_doc_path:
            try:
                os.startfile(self.selected_doc_path)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open file: {str(e)}")
    
    def rename_document(self):
        """Rename selected document"""
        if hasattr(self, 'selected_doc_path') and self.selected_doc_path:
            old_path = self.selected_doc_path
            old_name = os.path.basename(old_path)
            
            new_name = simpledialog.askstring("Rename Document", 
                                            f"Enter new name for '{old_name}':",
                                            parent=self.window)
            
            if new_name and new_name != old_name:
                try:
                    new_path = os.path.join(os.path.dirname(old_path), new_name)
                    os.rename(old_path, new_path)
                    messagebox.showinfo("Success", "Document renamed successfully!")
                    self.load_documents_list()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to rename document: {str(e)}")
    
    def delete_document(self):
        """Delete selected document"""
        if hasattr(self, 'selected_doc_path') and self.selected_doc_path:
            if messagebox.askyesno("Confirm Delete", 
                                 f"Are you sure you want to delete this document?\n\n{os.path.basename(self.selected_doc_path)}"):
                try:
                    os.remove(self.selected_doc_path)
                    messagebox.showinfo("Success", "Document deleted successfully!")
                    self.load_documents_list()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete document: {str(e)}")
    
    def show_applications(self):
        """Show all applications"""
        self.clear_content()
        
        apps_frame = tk.Frame(self.content_area, bg=self.WHITE)
        apps_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(apps_frame, text="My Applications", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Filter options
        filter_frame = tk.Frame(apps_frame, bg=self.WHITE)
        filter_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(filter_frame, text="Filter by:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left", padx=(0, 10))
        
        statuses = ["All", "Applied", "Shortlisted", "Selected", "Rejected", "Pending"]
        status_var = tk.StringVar(value="All")
        
        for status in statuses:
            tk.Radiobutton(filter_frame, text=status, variable=status_var, value=status,
                         font=("Arial", 10), bg=self.WHITE, fg=self.TEXT_DARK,
                         command=lambda: self.filter_applications(status_var.get())).pack(side="left", padx=5)
        
        # Applications table
        table_frame = tk.Frame(apps_frame, bg=self.WHITE)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("Company", "Position", "Applied Date", "Status", "Interview", "Actions")
        self.applications_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        col_widths = [150, 150, 120, 100, 120, 100]
        for i, col in enumerate(columns):
            self.applications_tree.heading(col, text=col)
            self.applications_tree.column(col, width=col_widths[i])
        
        # Load applications
        self.load_applications_table()
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.applications_tree.yview)
        self.applications_tree.configure(yscrollcommand=scrollbar.set)
        
        self.applications_tree.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Double click to view details
        self.applications_tree.bind("<Double-1>", lambda e: self.view_application_details())
    
    def load_applications_table(self, status_filter="All"):
        """Load applications into table"""
        # Clear existing items
        for item in self.applications_tree.get_children():
            self.applications_tree.delete(item)
        
        try:
            if status_filter == "All":
                self.cursor.execute("""
                    SELECT a.company_name, a.position, a.apply_date, a.status, 
                           i.scheduled_date, a.application_id
                    FROM student_applications a
                    LEFT JOIN interviews i ON a.application_id = i.application_id
                    WHERE a.student_id = ?
                    ORDER BY a.apply_date DESC
                """, (self.student_id,))
            else:
                self.cursor.execute("""
                    SELECT a.company_name, a.position, a.apply_date, a.status, 
                           i.scheduled_date, a.application_id
                    FROM student_applications a
                    LEFT JOIN interviews i ON a.application_id = i.application_id
                    WHERE a.student_id = ? AND a.status = ?
                    ORDER BY a.apply_date DESC
                """, (self.student_id, status_filter))
            
            applications = self.cursor.fetchall()
            
            for app in applications:
                company, position, date, status, interview_date, app_id = app
                
                # Format interview date
                interview_text = "Not scheduled"
                if interview_date:
                    interview_text = interview_date[:10]
                
                self.applications_tree.insert('', 'end', values=(
                    company, position, date[:10], status, interview_text, "View Details"
                ), tags=(app_id,))
            
            # Configure tag colors
            self.applications_tree.tag_configure('applied', foreground='#3b82f6')
            self.applications_tree.tag_configure('shortlisted', foreground='#10b981')
            self.applications_tree.tag_configure('selected', foreground='#059669')
            self.applications_tree.tag_configure('rejected', foreground='#dc2626')
            self.applications_tree.tag_configure('pending', foreground='#d97706')
            
        except Exception as e:
            print(f"Error loading applications: {e}")
    
    def filter_applications(self, status):
        """Filter applications by status"""
        self.load_applications_table(status)
    
    def view_application_details(self):
        """View application details"""
        selection = self.applications_tree.selection()
        if selection:
            item = self.applications_tree.item(selection[0])
            values = item['values']
            
            details_window = tk.Toplevel(self.window)
            details_window.title("Application Details")
            details_window.geometry("500x400")
            details_window.configure(bg=self.WHITE)
            
            tk.Label(details_window, text="Application Details", 
                    font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=20)
            
            info_frame = tk.Frame(details_window, bg=self.WHITE)
            info_frame.pack(padx=30, pady=10)
            
            details = [
                ("Company:", values[0]),
                ("Position:", values[1]),
                ("Applied Date:", values[2]),
                ("Status:", values[3]),
                ("Interview:", values[4])
            ]
            
            for label, value in details:
                row = tk.Frame(info_frame, bg=self.WHITE)
                row.pack(fill="x", pady=10)
                
                tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                        bg=self.WHITE, fg=self.TEXT_DARK, width=15, anchor="w").pack(side="left")
                tk.Label(row, text=value, font=("Arial", 11), 
                        bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="left", padx=10)
    
    def show_jobs(self):
        """Show all available jobs"""
        self.clear_content()
        
        jobs_frame = tk.Frame(self.content_area, bg=self.WHITE)
        jobs_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(jobs_frame, text="Browse Jobs", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Search and filter
        search_frame = tk.Frame(jobs_frame, bg=self.WHITE)
        search_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(search_frame, text="Search:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left", padx=(0, 10))
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11), width=40)
        self.search_entry.pack(side="left", padx=(0, 10))
        
        tk.Button(search_frame, text="🔍 Search", 
                 font=("Arial", 11), bg=self.PRIMARY, fg="white",
                 command=self.search_jobs, cursor="hand2", padx=20, pady=8).pack(side="left", padx=(0, 10))
        
        tk.Button(search_frame, text="🔄 Reset", 
                 font=("Arial", 11), bg=self.LIGHT_BG, fg=self.PRIMARY, bd=1,
                 command=self.reset_job_search, cursor="hand2", padx=20, pady=8).pack(side="left")
        
        # Jobs table
        table_frame = tk.Frame(jobs_frame, bg=self.WHITE)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("Company", "Position", "Location", "Salary", "Posted", "Eligibility", "Action")
        self.jobs_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        col_widths = [150, 150, 120, 100, 100, 120, 100]
        for i, col in enumerate(columns):
            self.jobs_tree.heading(col, text=col)
            self.jobs_tree.column(col, width=col_widths[i])
        
        # Load jobs
        self.load_jobs_table()
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.jobs_tree.yview)
        self.jobs_tree.configure(yscrollcommand=scrollbar.set)
        
        self.jobs_tree.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Double click to view details
        self.jobs_tree.bind("<Double-1>", lambda e: self.view_job_from_table())
    
    def load_jobs_table(self, search_term=""):
        """Load jobs into table"""
        # Clear existing items
        for item in self.jobs_tree.get_children():
            self.jobs_tree.delete(item)
        
        try:
            if search_term:
                self.cursor.execute("""
                    SELECT j.company_name, j.position, j.location, j.salary, 
                           j.posting_date, j.cgpa_cutoff, j.job_id
                    FROM job_postings j
                    WHERE j.status = 'Active' 
                    AND (j.position LIKE ? OR j.company_name LIKE ? OR j.description LIKE ?)
                    ORDER BY j.posting_date DESC
                """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            else:
                self.cursor.execute("""
                    SELECT j.company_name, j.position, j.location, j.salary, 
                           j.posting_date, j.cgpa_cutoff, j.job_id
                    FROM job_postings j
                    WHERE j.status = 'Active'
                    ORDER BY j.posting_date DESC
                """)
            
            jobs = self.cursor.fetchall()
            
            for job in jobs:
                company, position, location, salary, posted, cgpa_cutoff, job_id = job
                
                # Check eligibility
                student_cgpa = self.student_info.get('cgpa', 0.0)
                eligible = "Eligible" if student_cgpa >= (cgpa_cutoff or 0) else "Not eligible"
                
                # Check if applied
                self.cursor.execute("SELECT COUNT(*) FROM student_applications WHERE student_id=? AND job_id=?", 
                                  (self.student_id, job_id))
                applied = self.cursor.fetchone()[0] > 0
                
                action_text = "Apply" if not applied else "Applied ✓"
                
                self.jobs_tree.insert('', 'end', values=(
                    company, position, location or "N/A", salary or "N/A", 
                    posted[:10] if posted else "N/A", eligible, action_text
                ), tags=(job_id,))
                
                # Configure tag for applied jobs
                if applied:
                    self.jobs_tree.tag_configure(job_id, foreground='#10b981')
            
        except Exception as e:
            print(f"Error loading jobs: {e}")
    
    def search_jobs(self):
        """Search jobs"""
        search_term = self.search_entry.get()
        self.load_jobs_table(search_term)
    
    def reset_job_search(self):
        """Reset job search"""
        self.search_entry.delete(0, tk.END)
        self.load_jobs_table()
    
    def view_job_from_table(self):
        """View job details from table"""
        selection = self.jobs_tree.selection()
        if selection:
            item = self.jobs_tree.item(selection[0])
            job_id = item['tags'][0]
            self.view_job_details(job_id)
    
    def show_interviews(self):
        """Show interviews page"""
        self.clear_content()
        
        interviews_frame = tk.Frame(self.content_area, bg=self.WHITE)
        interviews_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(interviews_frame, text="My Interviews", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Create interview cards
        try:
            self.cursor.execute("""
                SELECT i.interview_id, c.name, i.scheduled_date, 
                       i.status, i.venue, i.interview_mode, i.interviewer_name
                FROM interviews i
                LEFT JOIN company_login c ON i.company_id = c.id
                WHERE i.student_id = ?
                ORDER BY i.scheduled_date DESC
            """, (self.student_id,))
            
            interviews = self.cursor.fetchall()
            
            if interviews:
                for interview in interviews:
                    interview_id, company, scheduled, status, venue, mode, interviewer = interview
                    
                    card = tk.Frame(interviews_frame, bg=self.LIGHT_BG, relief="solid", bd=1)
                    card.pack(fill="x", pady=10, padx=50, ipady=20)
                    
                    # Header row
                    header = tk.Frame(card, bg=self.LIGHT_BG)
                    header.pack(fill="x", padx=20, pady=10)
                    
                    tk.Label(header, text=company or "Company Name Not Found", 
                            font=("Arial", 14, "bold"), bg=self.LIGHT_BG, fg=self.TEXT_DARK).pack(side="left")
                    
                    # Status badge
                    status_color = '#10b981' if status == 'Scheduled' else '#f59e0b' if status == 'Completed' else '#dc2626'
                    tk.Label(header, text=status or "Pending", font=("Arial", 11, "bold"),
                            bg=status_color, fg="white", padx=15, pady=5).pack(side="right")
                    
                    # Details row
                    details = tk.Frame(card, bg=self.LIGHT_BG)
                    details.pack(fill="x", padx=20, pady=5)
                    
                    # Date and time
                    if scheduled:
                        try:
                            formatted_date = datetime.strptime(scheduled, "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y at %I:%M %p")
                            tk.Label(details, text=f"📅 {formatted_date}", 
                                    font=("Arial", 11), bg=self.LIGHT_BG, fg=self.TEXT_DARK).pack(anchor="w", pady=(5, 0))
                        except Exception as e:
                            tk.Label(details, text=f"📅 {scheduled}", 
                                    font=("Arial", 11), bg=self.LIGHT_BG, fg=self.TEXT_DARK).pack(anchor="w", pady=(5, 0))
                    
                    # Venue and mode
                    if venue:
                        tk.Label(details, text=f"📍 {venue} ({mode or 'Mode Unknown'})", 
                                font=("Arial", 11), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", pady=(5, 0))
                    
                    # Interviewer
                    if interviewer:
                        tk.Label(details, text=f"👤 Interviewer: {interviewer}", 
                                font=("Arial", 11), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", pady=(5, 0))
            
            else:
                tk.Label(interviews_frame, text="No interviews scheduled", 
                        font=("Arial", 16), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=100)
                
        except Exception as e:
            print(f"Error loading interviews: {e}")
            tk.Label(interviews_frame, text=f"Error loading interviews: {str(e)}", 
                    font=("Arial", 14), bg=self.WHITE, fg=self.DANGER).pack(pady=50, padx=20)
    
    def show_stats(self):
        """Show REAL placement statistics"""
        self.clear_content()
        
        stats_frame = tk.Frame(self.content_area, bg=self.WHITE)
        stats_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(stats_frame, text="Placement Statistics", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        try:
            # Get real statistics from database
            # 1. Student's personal stats
            self.cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM student_applications WHERE student_id = ?) as applications,
                    (SELECT COUNT(*) FROM student_applications WHERE student_id = ? AND status = 'Selected') as offers,
                    (SELECT COUNT(*) FROM interviews WHERE student_id = ?) as interviews,
                    (SELECT AVG(CGPA) FROM student_table WHERE Registration_no = ?) as cgpa
            """, (self.student_id, self.student_id, self.student_id, self.student_id))
            
            personal_stats = self.cursor.fetchone()
            
            if personal_stats:
                apps, offers, interviews, cgpa = personal_stats
                
                # Personal stats cards
                cards_frame = tk.Frame(stats_frame, bg=self.WHITE)
                cards_frame.pack(fill="x", pady=20)
                
                personal_cards = [
                    ("Your Applications", apps or 0, self.PRIMARY),
                    ("Interview Calls", interviews or 0, self.SUCCESS),
                    ("Job Offers", offers or 0, self.WARNING),
                    ("Your CGPA", f"{cgpa:.2f}" if cgpa else "N/A", self.DANGER)
                ]
                
                for title, value, color in personal_cards:
                    card = tk.Frame(cards_frame, bg="white", relief="solid", bd=1)
                    card.pack(side="left", fill="both", expand=True, padx=10, pady=10, ipady=30)
                    
                    tk.Label(card, text=str(value), font=("Arial", 28, "bold"), 
                            bg="white", fg=color).pack(pady=(10, 5))
                    tk.Label(card, text=title, font=("Arial", 12), 
                            bg="white", fg=self.TEXT_DARK).pack()
            
            # 2. Branch statistics
            branch = self.student_info.get('branch', '')
            if branch:
                tk.Label(stats_frame, text=f"📊 {branch} Branch Statistics", 
                        font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(40, 10))
                
                self.cursor.execute("""
                    SELECT 
                        COUNT(*) as total_students,
                        SUM(CASE WHEN Company_Name IS NOT NULL AND Company_Name != '' THEN 1 ELSE 0 END) as placed,
                        AVG(CGPA) as avg_cgpa,
                        MAX(CGPA) as max_cgpa,
                        MIN(CGPA) as min_cgpa
                    FROM student_table 
                    WHERE Branch = ?
                """, (branch,))
                
                branch_stats = self.cursor.fetchone()
                
                if branch_stats:
                    total, placed, avg_cgpa, max_cgpa, min_cgpa = branch_stats
                    placement_rate = (placed / total * 100) if total > 0 else 0
                    
                    # Branch stats in table
                    table_frame = tk.Frame(stats_frame, bg=self.WHITE)
                    table_frame.pack(fill="x", pady=10, padx=50)
                    
                    stats_data = [
                        ("Total Students", total),
                        ("Placed Students", placed),
                        ("Placement Rate", f"{placement_rate:.1f}%"),
                        ("Average CGPA", f"{avg_cgpa:.2f}" if avg_cgpa else "N/A"),
                        ("Highest CGPA", f"{max_cgpa:.2f}" if max_cgpa else "N/A"),
                        ("Lowest CGPA", f"{min_cgpa:.2f}" if min_cgpa else "N/A")
                    ]
                    
                    for label, value in stats_data:
                        row = tk.Frame(table_frame, bg=self.WHITE)
                        row.pack(fill="x", pady=8)
                        
                        tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                                bg=self.WHITE, fg=self.TEXT_DARK, width=20, anchor="w").pack(side="left")
                        tk.Label(row, text=str(value), font=("Arial", 11), 
                                bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="left", padx=10)
            
            # 3. Top companies hiring from college
            tk.Label(stats_frame, text="🏆 Top Recruiters", 
                    font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(40, 10))
            
            self.cursor.execute("""
                SELECT Company_Name, COUNT(*) as hires
                FROM student_table 
                WHERE Company_Name IS NOT NULL AND Company_Name != ''
                GROUP BY Company_Name
                ORDER BY hires DESC
                LIMIT 5
            """)
            
            top_companies = self.cursor.fetchall()
            
            if top_companies:
                for company, hires in top_companies:
                    row = tk.Frame(stats_frame, bg=self.WHITE)
                    row.pack(fill="x", pady=5, padx=100)
                    
                    tk.Label(row, text=company, font=("Arial", 11), 
                            bg=self.WHITE, fg=self.TEXT_DARK, width=30, anchor="w").pack(side="left")
                    
                    # Progress bar
                    max_hires = max([h for _, h in top_companies])
                    progress_width = 200
                    fill_width = (hires / max_hires) * progress_width if max_hires > 0 else 0
                    
                    progress_bg = tk.Frame(row, bg="#e5e7eb", width=progress_width, height=20)
                    progress_bg.pack(side="left", padx=10)
                    progress_bg.pack_propagate(False)
                    
                    progress_fill = tk.Frame(progress_bg, bg=self.PRIMARY, width=fill_width)
                    progress_fill.pack(side="left", fill="y")
                    
                    tk.Label(row, text=f"{hires} hire{'s' if hires != 1 else ''}", 
                            font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="left", padx=10)
            else:
                tk.Label(stats_frame, text="No placement data available yet", 
                        font=("Arial", 14), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=20)
                
        except Exception as e:
            print(f"Error loading statistics: {e}")
            tk.Label(stats_frame, text="Error loading statistics", 
                    font=("Arial", 14), bg=self.WHITE, fg=self.DANGER).pack(pady=20)
    
    def show_notifications(self):
        """Show notifications"""
        self.clear_content()
        
        notif_frame = tk.Frame(self.content_area, bg=self.WHITE)
        notif_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(notif_frame, text="Notifications", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Mark all as read button
        header_frame = tk.Frame(notif_frame, bg=self.WHITE)
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Button(header_frame, text="Mark all as read", 
                 font=("Arial", 11), bg=self.LIGHT_BG, fg=self.PRIMARY, bd=1,
                 command=self.mark_all_read, cursor="hand2", padx=20, pady=8).pack(side="right")
        
        # Notifications list
        try:
            self.cursor.execute("""
                SELECT notification_id, title, message, created_at, is_read
                FROM notifications
                WHERE user_id = ? AND user_type = 'student'
                ORDER BY created_at DESC
            """, (self.student_id,))
            
            notifications = self.cursor.fetchall()
            
            if notifications:
                for notif_id, title, message, created_at, is_read in notifications:
                    bg_color = self.LIGHT_BG if not is_read else self.WHITE
                    fg_color = self.TEXT_DARK if not is_read else self.TEXT_LIGHT
                    
                    notif_card = tk.Frame(notif_frame, bg=bg_color, relief="solid", bd=1)
                    notif_card.pack(fill="x", pady=5, padx=20, ipady=15)
                    
                    # Notification content
                    content_frame = tk.Frame(notif_card, bg=bg_color)
                    content_frame.pack(fill="x", padx=20, pady=10)
                    
                    # Title
                    title_label = tk.Label(content_frame, text=title, 
                                         font=("Arial", 12, "bold"), bg=bg_color, fg=fg_color)
                    title_label.pack(anchor="w")
                    
                    # Message
                    message_label = tk.Label(content_frame, text=message, 
                                           font=("Arial", 11), bg=bg_color, fg=fg_color, wraplength=800, justify="left")
                    message_label.pack(anchor="w", pady=(5, 0))
                    
                    # Date and actions
                    bottom_frame = tk.Frame(notif_card, bg=bg_color)
                    bottom_frame.pack(fill="x", padx=20, pady=(0, 10))
                    
                    tk.Label(bottom_frame, text=created_at[:10], 
                            font=("Arial", 10), bg=bg_color, fg=self.TEXT_LIGHT).pack(side="left")
                    
                    # Mark as read button
                    if not is_read:
                        tk.Button(bottom_frame, text="Mark as read", 
                                 font=("Arial", 10), bg=self.PRIMARY, fg="white",
                                 command=lambda nid=notif_id: self.mark_as_read(nid),
                                 cursor="hand2", padx=10, pady=3).pack(side="right")
            
            else:
                tk.Label(notif_frame, text="No notifications", 
                        font=("Arial", 16), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=100)
                
        except Exception as e:
            print(f"Error loading notifications: {e}")
            tk.Label(notif_frame, text="No notification data available", 
                    font=("Arial", 16), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=100)
    
    def mark_as_read(self, notification_id):
        """Mark notification as read"""
        try:
            self.cursor.execute("UPDATE notifications SET is_read=1 WHERE notification_id=?", (notification_id,))
            self.conn.commit()
            self.show_notifications()  # Refresh
        except Exception as e:
            print(f"Error marking as read: {e}")
    
    def mark_all_read(self):
        """Mark all notifications as read"""
        try:
            self.cursor.execute("UPDATE notifications SET is_read=1 WHERE user_id=? AND user_type='student'", 
                              (self.student_id,))
            self.conn.commit()
            self.show_notifications()  # Refresh
        except Exception as e:
            print(f"Error marking all as read: {e}")
    
    def show_settings(self):
        """Show settings page"""
        self.clear_content()
        
        settings_frame = tk.Frame(self.content_area, bg=self.WHITE)
        settings_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(settings_frame, text="Settings", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Change password section
        pass_frame = tk.LabelFrame(settings_frame, text="Change Password", 
                                  font=("Arial", 14, "bold"), bg=self.WHITE, 
                                  fg=self.TEXT_DARK, padx=20, pady=20)
        pass_frame.pack(fill="x", pady=10)
        
        # Current password
        tk.Label(pass_frame, text="Current Password:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(0, 5))
        self.current_pass = tk.Entry(pass_frame, font=("Arial", 11), show="*", width=40)
        self.current_pass.pack(fill="x", pady=(0, 15))
        
        # New password
        tk.Label(pass_frame, text="New Password:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(0, 5))
        self.new_pass = tk.Entry(pass_frame, font=("Arial", 11), show="*", width=40)
        self.new_pass.pack(fill="x", pady=(0, 15))
        
        # Confirm new password
        tk.Label(pass_frame, text="Confirm New Password:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(0, 5))
        self.confirm_pass = tk.Entry(pass_frame, font=("Arial", 11), show="*", width=40)
        self.confirm_pass.pack(fill="x", pady=(0, 20))
        
        # Change password button
        tk.Button(pass_frame, text="Change Password", 
                 font=("Arial", 11, "bold"), bg=self.PRIMARY, fg="white",
                 command=self.change_password, cursor="hand2", 
                 padx=20, pady=10).pack()
        
        # Profile settings section
        profile_frame = tk.LabelFrame(settings_frame, text="Profile Settings", 
                                     font=("Arial", 14, "bold"), bg=self.WHITE, 
                                     fg=self.TEXT_DARK, padx=20, pady=20)
        profile_frame.pack(fill="x", pady=20)
        
        settings_options = [
            ("Email Notifications", self.email_notifications),
            ("Job Alerts", self.job_alerts),
            ("Profile Visibility", self.profile_visibility),
            ("Data Sharing", self.data_sharing)
        ]
        
        for text, command in settings_options:
            row = tk.Frame(profile_frame, bg=self.WHITE)
            row.pack(fill="x", pady=10)
            
            tk.Label(row, text=text, font=("Arial", 11), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left")
            
            tk.Button(row, text="Configure", 
                     font=("Arial", 10), bg=self.LIGHT_BG, fg=self.PRIMARY, bd=1,
                     command=command, cursor="hand2", padx=15, pady=5).pack(side="right")
    
    def change_password(self):
        """Change password"""
        current = self.current_pass.get()
        new = self.new_pass.get()
        confirm = self.confirm_pass.get()
        
        if not current or not new or not confirm:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if new != confirm:
            messagebox.showerror("Error", "New passwords don't match!")
            return
        
        if len(new) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters!")
            return
        
        try:
            # Verify current password
            self.cursor.execute("SELECT password FROM student_signUP WHERE student_id=?", (self.student_id,))
            result = self.cursor.fetchone()
            
            if result and result[0] == current:
                # Update password
                self.cursor.execute("UPDATE student_signUP SET password=? WHERE student_id=?", (new, self.student_id))
                self.conn.commit()
                
                # Clear fields
                self.current_pass.delete(0, tk.END)
                self.new_pass.delete(0, tk.END)
                self.confirm_pass.delete(0, tk.END)
                
                messagebox.showinfo("Success", "Password changed successfully!")
            else:
                messagebox.showerror("Error", "Current password is incorrect!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {str(e)}")
    
    def email_notifications(self):
        """Configure email notifications"""
        messagebox.showinfo("Email Notifications", "You will receive email alerts for:\n• New job postings\n• Interview schedules\n• Application updates\n• Important announcements")
    
    def job_alerts(self):
        """Configure job alerts"""
        messagebox.showinfo("Job Alerts", "Configure job alerts based on:\n• Your skills\n• Preferred location\n• Salary expectations\n• Company preferences")
    
    def profile_visibility(self):
        """Configure profile visibility"""
        messagebox.showinfo("Profile Visibility", "Control who can see your profile:\n• Public (all companies)\n• Private (only applied companies)\n• Hidden (no one)")
    
    def data_sharing(self):
        """Configure data sharing"""
        messagebox.showinfo("Data Sharing", "Manage data sharing preferences:\n• Share resume with companies\n• Share academic records\n• Share contact information")
    
    def clear_content(self):
        """Clear content area"""
        for widget in self.content_area.winfo_children():
            if widget.winfo_class() != 'Frame' or 'topbar' in str(widget):
                continue
            widget.destroy()
    
    def logout(self):
        """Logout"""
        self.conn.close()
        self.window.destroy()
        # Return to main login
        os.system('python std_login.py')

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    # For testing
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
    else:
        student_id = "STU001"  # Default for testing
    
    app = StudentDashboard(student_id)
    app.run()