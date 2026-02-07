# company_dashboard.py - COMPLETE WORKING VERSION
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from datetime import datetime, timedelta
import sys
from PIL import Image, ImageTk, ImageDraw, ImageFont
import shutil

class CompanyDashboard:
    def __init__(self, company_id):
        self.company_id = company_id
        self.window = tk.Tk()
        self.window.title(f"PlacifyMe - Company Portal")
        self.window.geometry("1400x800")
        self.window.state("zoomed")
        
        # Professional color scheme for companies
        self.PRIMARY = "#0f766e"  # Teal
        self.SECONDARY = "#134e4a"
        self.SUCCESS = "#059669"
        self.WARNING = "#d97706"
        self.DANGER = "#dc2626"
        self.LIGHT_BG = "#f0fdfa"
        self.WHITE = "#ffffff"
        self.TEXT_DARK = "#1e293b"
        self.TEXT_LIGHT = "#64748b"
        
        # Initialize
        self.init_database()
        self.load_company_data()
        self.setup_ui()
        
    def init_database(self):
        """Initialize database connection"""
        try:
            self.conn = sqlite3.connect('registration_student.db')
            self.cursor = self.conn.cursor()
            print(f"✅ Connected to database for company: {self.company_id}")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect: {str(e)}")
            sys.exit(1)
    
    def load_company_data(self):
        """Load company information from database"""
        try:
            self.cursor.execute("SELECT * FROM company_login WHERE id=?", (self.company_id,))
            company_data = self.cursor.fetchone()
            
            if company_data:
                # Map columns based on your table structure
                self.company_info = {
                    'company_id': self.company_id,
                    'name': company_data[1] if len(company_data) > 1 else self.company_id,
                    'email': company_data[3] if len(company_data) > 3 else '',
                    'phone': company_data[4] if len(company_data) > 4 else '',
                    'industry': company_data[5] if len(company_data) > 5 else '',
                    'location': company_data[6] if len(company_data) > 6 else '',
                    'hr_contact': company_data[7] if len(company_data) > 7 else '',
                    'requirements': company_data[8] if len(company_data) > 8 else '',
                    'website': company_data[9] if len(company_data) > 9 else ''
                }
            else:
                self.company_info = {
                    'company_id': self.company_id,
                    'name': self.company_id,
                    'email': '',
                    'phone': '',
                    'industry': '',
                    'location': '',
                    'hr_contact': '',
                    'requirements': '',
                    'website': ''
                }
                
        except Exception as e:
            print(f"Error loading company data: {e}")
            self.company_info = {
                'company_id': self.company_id,
                'name': self.company_id,
                'email': '',
                'phone': '',
                'industry': '',
                'location': '',
                'hr_contact': '',
                'requirements': '',
                'website': ''
            }
    
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
        
        # Top bar
        self.create_topbar()
        
        # Default view
        self.show_dashboard()
    
    def create_sidebar(self, parent):
        """Create company sidebar"""
        sidebar = tk.Frame(parent, bg=self.SECONDARY, width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo/Header
        header_frame = tk.Frame(sidebar, bg=self.SECONDARY)
        header_frame.pack(fill="x", pady=(30, 20), padx=20)
        
        tk.Label(header_frame, text="🏢", font=("Arial", 40), 
                bg=self.SECONDARY, fg="white").pack()
        tk.Label(header_frame, text="Company Portal", 
                font=("Arial", 16, "bold"), bg=self.SECONDARY, fg="white").pack(pady=5)
        tk.Label(header_frame, text=self.company_info['name'], 
                font=("Arial", 12), bg=self.SECONDARY, fg="#cbd5e1", wraplength=200).pack()
        
        # Navigation Menu
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("📝 Post New Job", self.show_post_job),
            ("📋 Manage Jobs", self.show_manage_jobs),
            ("👥 Applications", self.show_applications),
            ("📅 Interviews", self.show_interviews),
            ("🎯 Shortlisted", self.show_shortlisted),
            ("📊 Analytics", self.show_analytics),
            ("🏢 Company Profile", self.show_company_profile),
            ("🔔 Notifications", self.show_notifications)
        ]
        
        for icon_text, command in menu_items:
            btn = tk.Button(sidebar, text=f"  {icon_text}", 
                          font=("Arial", 12), bg=self.SECONDARY, fg="white",
                          bd=0, anchor="w", padx=25, pady=15, 
                          command=command, cursor="hand2")
            btn.pack(fill="x")
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#0f766e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.SECONDARY))
        
        # Logout button at bottom
        tk.Frame(sidebar, bg=self.SECONDARY, height=20).pack(fill="x", pady=(20, 10))
        tk.Button(sidebar, text="🚪 Logout", font=("Arial", 12, "bold"),
                 bg="#dc2626", fg="white", bd=0, padx=25, pady=15,
                 command=self.logout, cursor="hand2").pack(side="bottom", fill="x", pady=20)
    
    def create_topbar(self):
        """Create company top bar"""
        topbar = tk.Frame(self.content_area, bg=self.WHITE, height=80)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        
        # Left: Welcome and stats
        left_frame = tk.Frame(topbar, bg=self.WHITE)
        left_frame.pack(side="left", padx=30, pady=20)
        
        tk.Label(left_frame, text=f"Welcome, {self.company_info['name']}", 
                font=("Arial", 16, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w")
        
        # Quick stats
        stats = self.get_quick_stats()
        stats_text = f"📊 {stats['active_jobs']} Active Jobs | 👥 {stats['applications']} Applications | 📅 {stats['interviews']} Interviews"
        tk.Label(left_frame, text=stats_text, 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(anchor="w", pady=(5, 0))
        
        # Right: Action buttons
        right_frame = tk.Frame(topbar, bg=self.WHITE)
        right_frame.pack(side="right", padx=30, pady=20)
        
        action_buttons = [
            ("📝 Post Job", self.show_post_job),
            ("🔔 Alerts", self.show_notifications),
            ("🆘 Help", self.show_help)
        ]
        
        for text, command in action_buttons:
            tk.Button(right_frame, text=text, font=("Arial", 10),
                     bg=self.LIGHT_BG, fg=self.PRIMARY, bd=1,
                     padx=15, pady=8, command=command, cursor="hand2").pack(side="left", padx=5)
    
    def get_quick_stats(self):
        """Get real-time statistics for company"""
        stats = {'active_jobs': 0, 'applications': 0, 'interviews': 0}
        
        try:
            # Active jobs count
            self.cursor.execute("SELECT COUNT(*) FROM job_postings WHERE company_id=? AND status='Active'", 
                              (self.company_id,))
            stats['active_jobs'] = self.cursor.fetchone()[0] or 0
            
            # Applications count
            self.cursor.execute("SELECT COUNT(*) FROM student_applications WHERE company_id=?", 
                              (self.company_id,))
            stats['applications'] = self.cursor.fetchone()[0] or 0
            
            # Interviews count
            self.cursor.execute("SELECT COUNT(*) FROM interviews WHERE company_id=?", 
                              (self.company_id,))
            stats['interviews'] = self.cursor.fetchone()[0] or 0
            
        except Exception as e:
            print(f"Error getting stats: {e}")
        
        return stats
    
    def show_dashboard(self):
        """Show company dashboard"""
        self.clear_content()
        
        # Main dashboard container
        dashboard_frame = tk.Frame(self.content_area, bg=self.WHITE)
        dashboard_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Dashboard header
        header_frame = tk.Frame(dashboard_frame, bg=self.WHITE)
        header_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(header_frame, text="Company Dashboard", 
                font=("Arial", 24, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left")
        
        today = datetime.now().strftime("%B %d, %Y")
        tk.Label(header_frame, text=f"📅 {today}", 
                font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="right")
        
        # Stats cards
        self.create_stats_cards(dashboard_frame)
        
        # Recent applications and active jobs side by side
        mid_frame = tk.Frame(dashboard_frame, bg=self.WHITE)
        mid_frame.pack(fill="both", expand=True, pady=20)
        
        # Left: Recent Applications
        left_frame = tk.LabelFrame(mid_frame, text="📋 Recent Applications", 
                                  font=("Arial", 14, "bold"), bg=self.WHITE, 
                                  fg=self.TEXT_DARK, padx=20, pady=20)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.create_recent_applications(left_frame)
        
        # Right: Active Jobs
        right_frame = tk.LabelFrame(mid_frame, text="🏢 Active Jobs", 
                                   font=("Arial", 14, "bold"), bg=self.WHITE, 
                                   fg=self.TEXT_DARK, padx=20, pady=20)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        self.create_active_jobs(right_frame)
        
        # Upcoming Interviews
        interviews_frame = tk.LabelFrame(dashboard_frame, text="📅 Upcoming Interviews", 
                                       font=("Arial", 14, "bold"), bg=self.WHITE, 
                                       fg=self.TEXT_DARK, padx=20, pady=20)
        interviews_frame.pack(fill="both", expand=True, pady=(0, 20))
        self.create_upcoming_interviews(interviews_frame)
    
    def create_stats_cards(self, parent):
        """Create 4 stats cards for company"""
        stats_frame = tk.Frame(parent, bg=self.WHITE)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats_data = self.get_detailed_stats()
        
        cards = [
            ("Active Jobs", stats_data['active_jobs'], f"{stats_data['total_jobs']} total", self.PRIMARY),
            ("Applications", stats_data['total_apps'], f"{stats_data['pending_apps']} pending", self.SUCCESS),
            ("Interviews", stats_data['total_interviews'], f"{stats_data['today_interviews']} today", self.WARNING),
            ("Hired", stats_data['hired'], f"{stats_data['offer_pending']} offers", self.DANGER)
        ]
        
        for i, (title, main_value, sub_value, color) in enumerate(cards):
            card = tk.Frame(stats_frame, bg="white", relief="solid", bd=1)
            card.pack(side="left", fill="both", expand=True, padx=10, pady=10, ipady=25)
            
            tk.Label(card, text=str(main_value), font=("Arial", 28, "bold"), 
                    bg="white", fg=color).pack(pady=(10, 5))
            tk.Label(card, text=title, font=("Arial", 12, "bold"), 
                    bg="white", fg=self.TEXT_DARK).pack()
            tk.Label(card, text=sub_value, font=("Arial", 10), 
                    bg="white", fg=self.TEXT_LIGHT).pack(pady=(5, 10))
    
    def get_detailed_stats(self):
        """Get detailed statistics for company"""
        stats = {
            'active_jobs': 0,
            'total_jobs': 0,
            'total_apps': 0,
            'pending_apps': 0,
            'total_interviews': 0,
            'today_interviews': 0,
            'hired': 0,
            'offer_pending': 0
        }
        
        try:
            # Job stats
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active
                FROM job_postings 
                WHERE company_id=?
            """, (self.company_id,))
            job_result = self.cursor.fetchone()
            if job_result:
                stats['total_jobs'] = job_result[0] or 0
                stats['active_jobs'] = job_result[1] or 0
            
            # Application stats
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'Applied' OR status = 'Pending' THEN 1 ELSE 0 END) as pending
                FROM student_applications 
                WHERE company_id=?
            """, (self.company_id,))
            app_result = self.cursor.fetchone()
            if app_result:
                stats['total_apps'] = app_result[0] or 0
                stats['pending_apps'] = app_result[1] or 0
            
            # Interview stats
            today = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN DATE(scheduled_date) = ? THEN 1 ELSE 0 END) as today
                FROM interviews 
                WHERE company_id=?
            """, (today, self.company_id))
            interview_result = self.cursor.fetchone()
            if interview_result:
                stats['total_interviews'] = interview_result[0] or 0
                stats['today_interviews'] = interview_result[1] or 0
            
            # Hired stats
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as hired,
                    SUM(CASE WHEN offer_status = 'Pending' THEN 1 ELSE 0 END) as pending_offers
                FROM student_applications 
                WHERE company_id=? AND status = 'Selected'
            """, (self.company_id,))
            hired_result = self.cursor.fetchone()
            if hired_result:
                stats['hired'] = hired_result[0] or 0
                stats['offer_pending'] = hired_result[1] or 0
                
        except Exception as e:
            print(f"Error getting detailed stats: {e}")
        
        return stats
    
    def create_recent_applications(self, parent):
        """Show recent applications for company"""
        try:
            self.cursor.execute("""
                SELECT a.application_id, s.Full_name, j.position, a.apply_date, a.status 
                FROM student_applications a
                LEFT JOIN job_postings j ON a.job_id = j.job_id
                LEFT JOIN student_table s ON a.student_id = s.Registration_no
                WHERE a.company_id = ?
                ORDER BY a.apply_date DESC
                LIMIT 5
            """, (self.company_id,))
            
            apps = self.cursor.fetchall()
            
            if apps:
                for app_id, student_name, position, date, status in apps:
                    app_frame = tk.Frame(parent, bg=self.LIGHT_BG)
                    app_frame.pack(fill="x", pady=8, padx=10, ipady=10)
                    
                    # Application header
                    header = tk.Frame(app_frame, bg=self.LIGHT_BG)
                    header.pack(fill="x", padx=15, pady=5)
                    
                    tk.Label(header, text=student_name or "Unknown Student", 
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
                    
                    tk.Label(details, text=f"💼 {position}", 
                            font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(side="left", padx=(0, 15))
                    tk.Label(details, text=f"📅 {date[:10] if date else 'N/A'}", 
                            font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(side="left")
                    
                    # Action buttons
                    actions = tk.Frame(app_frame, bg=self.LIGHT_BG)
                    actions.pack(fill="x", padx=15, pady=(5, 0))
                    
                    tk.Button(actions, text="View Profile", font=("Arial", 9), 
                             bg=self.PRIMARY, fg="white", padx=10, pady=2,
                             command=lambda aid=app_id: self.view_application_details(aid),
                             cursor="hand2").pack(side="left", padx=2)
                    
                    if status == 'Applied':
                        tk.Button(actions, text="Shortlist", font=("Arial", 9), 
                                 bg=self.SUCCESS, fg="white", padx=10, pady=2,
                                 command=lambda aid=app_id: self.shortlist_application(aid),
                                 cursor="hand2").pack(side="left", padx=2)
                        
                        tk.Button(actions, text="Schedule Interview", font=("Arial", 9), 
                                 bg=self.WARNING, fg="white", padx=10, pady=2,
                                 command=lambda aid=app_id: self.schedule_interview_dialog(aid),
                                 cursor="hand2").pack(side="left", padx=2)
            else:
                tk.Label(parent, text="No applications yet", 
                        font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=30)
                
        except Exception as e:
            print(f"Error loading applications: {e}")
            tk.Label(parent, text="Error loading applications", 
                    font=("Arial", 12), bg=self.WHITE, fg=self.DANGER).pack(pady=30)
        
        # View all applications button
        tk.Button(parent, text="View All Applications →", 
                 font=("Arial", 11), bg=self.PRIMARY, fg="white",
                 command=self.show_applications, cursor="hand2", 
                 padx=20, pady=10).pack(pady=10)
    
    def create_active_jobs(self, parent):
        """Show company's active jobs"""
        try:
            self.cursor.execute("""
                SELECT job_id, position, position_count, application_deadline, 
                       (SELECT COUNT(*) FROM student_applications WHERE job_id = job_postings.job_id) as app_count
                FROM job_postings 
                WHERE company_id = ? AND status = 'Active'
                ORDER BY posting_date DESC
                LIMIT 5
            """, (self.company_id,))
            
            jobs = self.cursor.fetchall()
            
            if jobs:
                for job_id, title, positions, deadline, app_count in jobs:
                    job_frame = tk.Frame(parent, bg="white", relief="solid", bd=1)
                    job_frame.pack(fill="x", pady=8, padx=10, ipady=15)
                    
                    # Job title
                    tk.Label(job_frame, text=title, font=("Arial", 13, "bold"), 
                            bg="white", fg=self.TEXT_DARK).pack(anchor="w", padx=15, pady=5)
                    
                    # Job details
                    details = tk.Frame(job_frame, bg="white")
                    details.pack(fill="x", padx=15, pady=5)
                    
                    tk.Label(details, text=f"📋 Positions: {positions}", 
                            font=("Arial", 11), bg="white", fg=self.TEXT_DARK).pack(side="left", padx=(0, 15))
                    tk.Label(details, text=f"📝 Applications: {app_count}", 
                            font=("Arial", 11), bg="white", fg=self.TEXT_DARK).pack(side="left", padx=(0, 15))
                    
                    if deadline:
                        deadline_date = deadline if isinstance(deadline, str) else str(deadline)
                        tk.Label(details, text=f"⏰ Deadline: {deadline_date}", 
                                font=("Arial", 11), bg="white", fg=self.DANGER).pack(side="left")
                    
                    # Action buttons
                    actions = tk.Frame(job_frame, bg="white")
                    actions.pack(fill="x", padx=15, pady=(5, 0))
                    
                    tk.Button(actions, text="View Applications", font=("Arial", 10), 
                             bg=self.PRIMARY, fg="white", padx=10, pady=3,
                             command=lambda jid=job_id: self.view_job_applications(jid),
                             cursor="hand2").pack(side="left", padx=2)
                    
                    tk.Button(actions, text="Edit", font=("Arial", 10), 
                             bg=self.WARNING, fg="white", padx=10, pady=3,
                             command=lambda jid=job_id: self.edit_job(jid),
                             cursor="hand2").pack(side="left", padx=2)
                    
                    tk.Button(actions, text="Close Job", font=("Arial", 10), 
                             bg=self.DANGER, fg="white", padx=10, pady=3,
                             command=lambda jid=job_id: self.close_job(jid),
                             cursor="hand2").pack(side="left", padx=2)
            else:
                tk.Label(parent, text="No active job postings", 
                        font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=30)
                
                # Post job button
                tk.Button(parent, text="Post Your First Job", font=("Arial", 12, "bold"), 
                         bg=self.PRIMARY, fg="white", command=self.show_post_job,
                         cursor="hand2", padx=30, pady=12).pack(pady=20)
                
        except Exception as e:
            print(f"Error loading jobs: {e}")
            tk.Label(parent, text="Error loading jobs", 
                    font=("Arial", 12), bg=self.WHITE, fg=self.DANGER).pack(pady=30)
    
    def create_upcoming_interviews(self, parent):
        """Show upcoming interviews for company"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("""
                SELECT i.interview_id, s.Full_name, j.position, i.scheduled_date, 
                       i.status, i.venue, i.interview_mode
                FROM interviews i
                LEFT JOIN job_postings j ON i.job_id = j.job_id
                LEFT JOIN student_table s ON i.student_id = s.Registration_no
                WHERE i.company_id = ? AND DATE(i.scheduled_date) >= ?
                ORDER BY i.scheduled_date ASC
                LIMIT 5
            """, (self.company_id, today))
            
            interviews = self.cursor.fetchall()
            
            if interviews:
                for interview in interviews:
                    interview_id, student_name, position, scheduled, status, venue, mode = interview
                    
                    interview_frame = tk.Frame(parent, bg=self.LIGHT_BG)
                    interview_frame.pack(fill="x", pady=8, padx=10, ipady=10)
                    
                    # Interview header
                    tk.Label(interview_frame, text=student_name or "Unknown Student", 
                            font=("Arial", 11, "bold"), bg=self.LIGHT_BG, fg=self.TEXT_DARK).pack(anchor="w", padx=15, pady=5)
                    
                    # Position
                    tk.Label(interview_frame, text=f"💼 {position}", 
                            font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15)
                    
                    # Date and time
                    if scheduled:
                        try:
                            formatted_date = datetime.strptime(scheduled, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %I:%M %p")
                            tk.Label(interview_frame, text=f"📅 {formatted_date}", 
                                    font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15)
                        except:
                            tk.Label(interview_frame, text=f"📅 {scheduled}", 
                                    font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15)
                    
                    # Venue and mode
                    if venue:
                        tk.Label(interview_frame, text=f"📍 {venue} ({mode})", 
                                font=("Arial", 10), bg=self.LIGHT_BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15)
                    
                    # Status and actions
                    bottom_frame = tk.Frame(interview_frame, bg=self.LIGHT_BG)
                    bottom_frame.pack(fill="x", padx=15, pady=(5, 0))
                    
                    # Status
                    status_color = '#10b981' if status == 'Scheduled' else '#f59e0b'
                    tk.Label(bottom_frame, text=f"Status: {status}", 
                            font=("Arial", 10, "bold"), bg=self.LIGHT_BG, fg=status_color).pack(side="left")
                    
                    # Action buttons
                    if status == 'Scheduled':
                        tk.Button(bottom_frame, text="Update Status", font=("Arial", 9), 
                                 bg=self.PRIMARY, fg="white", padx=10, pady=2,
                                 command=lambda iid=interview_id: self.update_interview_status(iid),
                                 cursor="hand2").pack(side="right", padx=2)
                        
                        tk.Button(bottom_frame, text="Reschedule", font=("Arial", 9), 
                                 bg=self.WARNING, fg="white", padx=10, pady=2,
                                 command=lambda iid=interview_id: self.reschedule_interview(iid),
                                 cursor="hand2").pack(side="right", padx=2)
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
    
    def show_post_job(self):
        """Show job posting form - COMPLETE WORKING VERSION"""
        self.clear_content()
        
        frame = tk.Frame(self.content_area, bg=self.WHITE)
        frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="Post New Job", font=("Arial", 24, "bold"), 
                bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 30))
        
        # Form container with scrollbar
        form_container = tk.Frame(frame, bg=self.WHITE)
        form_container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(form_container, bg=self.WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        form_frame = tk.Frame(canvas, bg=self.WHITE)
        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        
        # Form fields
        fields = [
            ("Job Title *", "entry", "job_title", ""),
            ("Job Type", "combo", "job_type", ["Full-time", "Internship", "Part-time", "Contract"]),
            ("Location", "entry", "location", ""),
            ("Salary Package", "entry", "salary", "e.g., ₹8,00,000 - ₹12,00,000 per annum"),
            ("Number of Positions *", "entry", "positions", "1"),
            ("Minimum CGPA", "entry", "cgpa_cutoff", "0.0"),
            ("Eligible Branches", "entry", "branches", "IT, EXTC, MECH, COMP, ELECTRICAL"),
            ("Application Deadline", "entry", "deadline", datetime.now().strftime("%Y-%m-%d")),
            ("Work Mode", "combo", "work_mode", ["On-site", "Remote", "Hybrid"]),
            ("Job Description *", "text", "description", "Enter detailed job description..."),
            ("Requirements *", "text", "requirements", "Enter job requirements..."),
            ("Interview Process", "text", "interview_process", "Describe interview rounds..."),
            ("Benefits", "text", "benefits", "List benefits offered...")
        ]
        
        self.post_job_entries = {}
        
        for i, (label, field_type, key, default_value) in enumerate(fields):
            row = tk.Frame(form_frame, bg=self.WHITE)
            row.pack(fill="x", pady=12, padx=50)
            
            tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK, width=20, anchor="w").pack(side="left")
            
            if field_type == "entry":
                entry = tk.Entry(row, font=("Arial", 11), width=40)
                entry.insert(0, default_value)
                entry.pack(side="left", padx=10)
                self.post_job_entries[key] = entry
                
            elif field_type == "combo":
                var = tk.StringVar(value=default_value[0] if default_value else "")
                combo = ttk.Combobox(row, textvariable=var, values=default_value, 
                                    state="readonly", width=37, font=("Arial", 11))
                combo.pack(side="left", padx=10)
                self.post_job_entries[key] = var
                
            elif field_type == "text":
                text_frame = tk.Frame(row, bg=self.WHITE)
                text_frame.pack(side="left", padx=10, fill="x", expand=True)
                
                scrollbar = tk.Scrollbar(text_frame)
                scrollbar.pack(side="right", fill="y")
                
                text_widget = tk.Text(text_frame, height=4, width=40, font=("Arial", 11),
                                     yscrollcommand=scrollbar.set)
                text_widget.insert("1.0", default_value)
                text_widget.pack(side="left", fill="both", expand=True)
                scrollbar.config(command=text_widget.yview)
                self.post_job_entries[key] = text_widget
        
        # Update scroll region
        form_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Submit button
        submit_frame = tk.Frame(frame, bg=self.WHITE)
        submit_frame.pack(pady=30)
        
        tk.Button(submit_frame, text="Post Job", font=("Arial", 14, "bold"), 
                 bg=self.PRIMARY, fg="white", command=self.post_job,
                 cursor="hand2", padx=40, pady=12).pack()
    
    def post_job(self):
        """Post a new job - COMPLETE WORKING"""
        try:
            # Get values from entries
            job_title = self.post_job_entries['job_title'].get()
            job_type = self.post_job_entries['job_type'].get()
            location = self.post_job_entries['location'].get()
            salary = self.post_job_entries['salary'].get()
            positions = self.post_job_entries['positions'].get()
            cgpa_cutoff = self.post_job_entries['cgpa_cutoff'].get()
            branches = self.post_job_entries['branches'].get()
            deadline = self.post_job_entries['deadline'].get()
            work_mode = self.post_job_entries['work_mode'].get()
            description = self.post_job_entries['description'].get("1.0", "end-1c")
            requirements = self.post_job_entries['requirements'].get("1.0", "end-1c")
            interview_process = self.post_job_entries['interview_process'].get("1.0", "end-1c")
            benefits = self.post_job_entries['benefits'].get("1.0", "end-1c")
            
            # Validation
            if not job_title or not description or not requirements:
                messagebox.showerror("Error", "Please fill all required fields (*)")
                return
            
            if not positions.isdigit() or int(positions) <= 0:
                messagebox.showerror("Error", "Please enter valid number of positions")
                return
            
            # Insert into database
            self.cursor.execute("""
                INSERT INTO job_postings 
                (company_id, company_name, position, job_type, location, salary, 
                 position_count, cgpa_cutoff, eligible_branches, application_deadline,
                 description, requirements, work_mode, interview_process, benefits,
                 posting_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active')
            """, (
                self.company_id,
                self.company_info['name'],
                job_title,
                job_type,
                location,
                salary,
                int(positions),
                float(cgpa_cutoff) if cgpa_cutoff else 0.0,
                branches,
                deadline,
                description,
                requirements,
                work_mode,
                interview_process,
                benefits,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            self.conn.commit()
            
            # Create notification for students
            job_id = self.cursor.lastrowid
            notification_msg = f"New job posted: {job_title} at {self.company_info['name']}"
            
            # Get eligible branches
            if branches:
                branch_list = [b.strip() for b in branches.split(',')]
                for branch in branch_list:
                    self.cursor.execute("""
                        INSERT INTO notifications (user_id, user_type, title, message)
                        SELECT Registration_no, 'student', 'New Job Alert', ?
                        FROM student_table WHERE Branch = ?
                    """, (notification_msg, branch))
            
            self.conn.commit()
            
            messagebox.showinfo("Success", "Job posted successfully!")
            self.show_dashboard()  # Return to dashboard
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to post job: {str(e)}")
    
    def show_manage_jobs(self):
        """Show job management page - COMPLETE WORKING"""
        self.clear_content()
        
        frame = tk.Frame(self.content_area, bg=self.WHITE)
        frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="Manage Jobs", font=("Arial", 24, "bold"), 
                bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Search and filter
        search_frame = tk.Frame(frame, bg=self.WHITE)
        search_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(search_frame, text="Search:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left", padx=(0, 10))
        
        self.job_search_entry = tk.Entry(search_frame, font=("Arial", 11), width=40)
        self.job_search_entry.pack(side="left", padx=(0, 10))
        
        tk.Button(search_frame, text="🔍 Search", 
                 font=("Arial", 11), bg=self.PRIMARY, fg="white",
                 command=self.search_jobs, cursor="hand2", padx=20, pady=8).pack(side="left", padx=(0, 10))
        
        tk.Button(search_frame, text="🔄 Reset", 
                 font=("Arial", 11), bg=self.LIGHT_BG, fg=self.PRIMARY, bd=1,
                 command=self.reset_job_search, cursor="hand2", padx=20, pady=8).pack(side="left")
        
        # Filter by status
        filter_frame = tk.Frame(frame, bg=self.WHITE)
        filter_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(filter_frame, text="Filter by Status:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left", padx=(0, 10))
        
        self.job_status_var = tk.StringVar(value="All")
        statuses = ["All", "Active", "Closed", "Draft"]
        
        for status in statuses:
            tk.Radiobutton(filter_frame, text=status, variable=self.job_status_var, value=status,
                         font=("Arial", 10), bg=self.WHITE, fg=self.TEXT_DARK,
                         command=self.filter_jobs_by_status).pack(side="left", padx=5)
        
        # Jobs table
        table_frame = tk.Frame(frame, bg=self.WHITE)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("Job ID", "Position", "Applications", "Positions", "Deadline", "Status", "Actions")
        self.jobs_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        col_widths = [80, 150, 100, 80, 100, 80, 150]
        for i, col in enumerate(columns):
            self.jobs_tree.heading(col, text=col)
            self.jobs_tree.column(col, width=col_widths[i])
        
        # Load jobs
        self.load_manage_jobs_table()
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.jobs_tree.yview)
        self.jobs_tree.configure(yscrollcommand=scrollbar.set)
        
        self.jobs_tree.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Context menu
        self.jobs_menu = tk.Menu(self.window, tearoff=0)
        self.jobs_menu.add_command(label="View Details", command=self.view_job_details)
        self.jobs_menu.add_command(label="Edit Job", command=self.edit_job_from_table)
        self.jobs_menu.add_command(label="Close/Reopen", command=self.toggle_job_status)
        self.jobs_menu.add_command(label="Delete Job", command=self.delete_job)
        
        self.jobs_tree.bind("<Button-3>", self.show_jobs_context_menu)
    
    def load_manage_jobs_table(self, search_term="", status_filter="All"):
        """Load jobs into management table"""
        # Clear existing items
        for item in self.jobs_tree.get_children():
            self.jobs_tree.delete(item)
        
        try:
            query = """
                SELECT j.job_id, j.position, 
                       (SELECT COUNT(*) FROM student_applications WHERE job_id = j.job_id) as app_count,
                       j.position_count, j.application_deadline, j.status
                FROM job_postings j
                WHERE j.company_id = ?
            """
            params = [self.company_id]
            
            if search_term:
                query += " AND (j.position LIKE ? OR j.description LIKE ?)"
                params.extend([f'%{search_term}%', f'%{search_term}%'])
            
            if status_filter != "All":
                query += " AND j.status = ?"
                params.append(status_filter)
            
            query += " ORDER BY j.posting_date DESC"
            
            self.cursor.execute(query, params)
            jobs = self.cursor.fetchall()
            
            for job in jobs:
                job_id, position, app_count, positions, deadline, status = job
                
                # Format deadline
                deadline_str = deadline[:10] if deadline else "N/A"
                
                # Status color
                status_color = '#10b981' if status == 'Active' else '#dc2626' if status == 'Closed' else '#d97706'
                
                self.jobs_tree.insert('', 'end', values=(
                    job_id, position, app_count, positions, deadline_str, status, "View/Edit"
                ), tags=(job_id, status))
                
                # Configure tag colors
                self.jobs_tree.tag_configure(status, foreground=status_color)
            
        except Exception as e:
            print(f"Error loading jobs: {e}")
    
    def search_jobs(self):
        """Search jobs in management"""
        search_term = self.job_search_entry.get()
        status_filter = self.job_status_var.get()
        self.load_manage_jobs_table(search_term, status_filter)
    
    def reset_job_search(self):
        """Reset job search"""
        self.job_search_entry.delete(0, tk.END)
        self.job_status_var.set("All")
        self.load_manage_jobs_table()
    
    def filter_jobs_by_status(self):
        """Filter jobs by status"""
        status_filter = self.job_status_var.get()
        search_term = self.job_search_entry.get()
        self.load_manage_jobs_table(search_term, status_filter)
    
    def show_jobs_context_menu(self, event):
        """Show context menu for jobs"""
        item = self.jobs_tree.identify_row(event.y)
        if item:
            self.jobs_tree.selection_set(item)
            self.selected_job_id = self.jobs_tree.item(item, "values")[0]
            self.jobs_menu.post(event.x_root, event.y_root)
    
    def view_job_details(self):
        """View job details from management"""
        if hasattr(self, 'selected_job_id'):
            self.view_job_details_dialog(self.selected_job_id)
    
    def edit_job_from_table(self):
        """Edit job from management table"""
        if hasattr(self, 'selected_job_id'):
            self.edit_job(self.selected_job_id)
    
    def toggle_job_status(self):
        """Toggle job status (Active/Closed)"""
        if hasattr(self, 'selected_job_id'):
            job_id = self.selected_job_id
            item = self.jobs_tree.selection()[0]
            current_status = self.jobs_tree.item(item, "values")[5]
            
            new_status = 'Closed' if current_status == 'Active' else 'Active'
            
            try:
                self.cursor.execute("UPDATE job_postings SET status=? WHERE job_id=?", 
                                  (new_status, job_id))
                self.conn.commit()
                
                messagebox.showinfo("Success", f"Job status changed to {new_status}")
                self.load_manage_jobs_table()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update job status: {str(e)}")
    
    def delete_job(self):
        """Delete job from management"""
        if hasattr(self, 'selected_job_id'):
            job_id = self.selected_job_id
            
            if messagebox.askyesno("Confirm Delete", 
                                 f"Are you sure you want to delete job #{job_id}?\n\nThis will also delete all associated applications."):
                try:
                    # Delete applications first
                    self.cursor.execute("DELETE FROM student_applications WHERE job_id=?", (job_id,))
                    # Delete job
                    self.cursor.execute("DELETE FROM job_postings WHERE job_id=?", (job_id,))
                    self.conn.commit()
                    
                    messagebox.showinfo("Success", "Job deleted successfully!")
                    self.load_manage_jobs_table()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete job: {str(e)}")
    
    def view_job_details_dialog(self, job_id):
        """View job details in dialog"""
        try:
            self.cursor.execute("SELECT * FROM job_postings WHERE job_id=?", (job_id,))
            job = self.cursor.fetchone()
            
            if job:
                details_window = tk.Toplevel(self.window)
                details_window.title(f"Job Details - #{job_id}")
                details_window.geometry("600x500")
                details_window.configure(bg=self.WHITE)
                
                # Create scrollable frame
                canvas = tk.Canvas(details_window, bg=self.WHITE, highlightthickness=0)
                scrollbar = tk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
                canvas.configure(yscrollcommand=scrollbar.set)
                
                scrollbar.pack(side="right", fill="y")
                canvas.pack(side="left", fill="both", expand=True)
                
                content_frame = tk.Frame(canvas, bg=self.WHITE)
                canvas.create_window((0, 0), window=content_frame, anchor="nw")
                
                # Job title
                tk.Label(content_frame, text=job[3],  # position
                        font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(20, 10), padx=20)
                
                # Basic info
                info_labels = [
                    ("Company:", job[2]),
                    ("Job Type:", job[12] if len(job) > 12 else "N/A"),
                    ("Location:", job[5]),
                    ("Salary:", job[4]),
                    ("Positions:", str(job[9])),
                    ("CGPA Cutoff:", str(job[10])),
                    ("Deadline:", job[11] if len(job) > 11 else "N/A"),
                    ("Status:", job[17] if len(job) > 17 else "N/A")
                ]
                
                for label, value in info_labels:
                    if value:
                        row = tk.Frame(content_frame, bg=self.WHITE)
                        row.pack(fill="x", pady=5, padx=20)
                        
                        tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                                bg=self.WHITE, fg=self.TEXT_DARK, width=15, anchor="w").pack(side="left")
                        tk.Label(row, text=value, font=("Arial", 11), 
                                bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="left", padx=10)
                
                # Description
                if job[6]:  # description
                    tk.Label(content_frame, text="Description:", 
                            font=("Arial", 12, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(15, 5), padx=20, anchor="w")
                    
                    desc_frame = tk.Frame(content_frame, bg=self.WHITE)
                    desc_frame.pack(fill="x", padx=20)
                    tk.Label(desc_frame, text=job[6], wraplength=500, justify="left",
                            font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack()
                
                # Requirements
                if job[7]:  # requirements
                    tk.Label(content_frame, text="Requirements:", 
                            font=("Arial", 12, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(15, 5), padx=20, anchor="w")
                    
                    req_frame = tk.Frame(content_frame, bg=self.WHITE)
                    req_frame.pack(fill="x", padx=20)
                    tk.Label(req_frame, text=job[7], wraplength=500, justify="left",
                            font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack()
                
                # Update scroll region
                content_frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load job details: {str(e)}")
    
    def edit_job(self, job_id):
        """Edit existing job"""
        try:
            self.cursor.execute("SELECT * FROM job_postings WHERE job_id=?", (job_id,))
            job = self.cursor.fetchone()
            
            if not job:
                messagebox.showerror("Error", "Job not found!")
                return
            
            # Create edit window
            edit_window = tk.Toplevel(self.window)
            edit_window.title(f"Edit Job - #{job_id}")
            edit_window.geometry("600x700")
            edit_window.configure(bg=self.WHITE)
            
            tk.Label(edit_window, text=f"Edit Job: {job[3]}", 
                    font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=20)
            
            # Form fields
            fields_frame = tk.Frame(edit_window, bg=self.WHITE)
            fields_frame.pack(fill="both", expand=True, padx=30)
            
            # Job Title
            tk.Label(fields_frame, text="Job Title:", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            title_entry = tk.Entry(fields_frame, font=("Arial", 11), width=50)
            title_entry.insert(0, job[3])
            title_entry.pack(fill="x", pady=(0, 15))
            
            # Description
            tk.Label(fields_frame, text="Description:", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            desc_text = tk.Text(fields_frame, font=("Arial", 11), height=4, width=50)
            desc_text.insert("1.0", job[6] if len(job) > 6 else "")
            desc_text.pack(fill="x", pady=(0, 15))
            
            # Requirements
            tk.Label(fields_frame, text="Requirements:", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            req_text = tk.Text(fields_frame, font=("Arial", 11), height=4, width=50)
            req_text.insert("1.0", job[7] if len(job) > 7 else "")
            req_text.pack(fill="x", pady=(0, 15))
            
            # Salary
            tk.Label(fields_frame, text="Salary:", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            salary_entry = tk.Entry(fields_frame, font=("Arial", 11), width=50)
            salary_entry.insert(0, job[4] if len(job) > 4 else "")
            salary_entry.pack(fill="x", pady=(0, 15))
            
            # Positions
            tk.Label(fields_frame, text="Number of Positions:", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            positions_entry = tk.Entry(fields_frame, font=("Arial", 11), width=50)
            positions_entry.insert(0, job[9] if len(job) > 9 else "1")
            positions_entry.pack(fill="x", pady=(0, 15))
            
            # Status
            tk.Label(fields_frame, text="Status:", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            status_var = tk.StringVar(value=job[17] if len(job) > 17 else "Active")
            status_combo = ttk.Combobox(fields_frame, textvariable=status_var, 
                                       values=["Active", "Closed", "Draft"], state="readonly", width=47)
            status_combo.pack(fill="x", pady=(0, 25))
            
            # Save button
            def save_changes():
                try:
                    self.cursor.execute("""
                        UPDATE job_postings 
                        SET position=?, description=?, requirements=?, salary=?, 
                            position_count=?, status=?
                        WHERE job_id=?
                    """, (
                        title_entry.get(),
                        desc_text.get("1.0", "end-1c"),
                        req_text.get("1.0", "end-1c"),
                        salary_entry.get(),
                        int(positions_entry.get()),
                        status_var.get(),
                        job_id
                    ))
                    
                    self.conn.commit()
                    messagebox.showinfo("Success", "Job updated successfully!")
                    edit_window.destroy()
                    self.load_manage_jobs_table()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update job: {str(e)}")
            
            tk.Button(edit_window, text="Save Changes", font=("Arial", 12, "bold"), 
                     bg=self.PRIMARY, fg="white", command=save_changes,
                     cursor="hand2", padx=30, pady=12).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load job for editing: {str(e)}")
    
    def close_job(self, job_id):
        """Close a job posting"""
        try:
            self.cursor.execute("UPDATE job_postings SET status='Closed' WHERE job_id=?", (job_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Job closed successfully!")
            self.show_dashboard()  # Refresh
        except Exception as e:
            messagebox.showerror("Error", f"Failed to close job: {str(e)}")
    
    def show_applications(self):
        """Show all applications for company - COMPLETE WORKING"""
        self.clear_content()
        
        apps_frame = tk.Frame(self.content_area, bg=self.WHITE)
        apps_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(apps_frame, text="Job Applications", font=("Arial", 24, "bold"), 
                bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Filter options
        filter_frame = tk.Frame(apps_frame, bg=self.WHITE)
        filter_frame.pack(fill="x", pady=(0, 20))
        
        # Filter by job
        tk.Label(filter_frame, text="Filter by Job:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left", padx=(0, 10))
        
        self.job_filter_var = tk.StringVar(value="All Jobs")
        job_options = ["All Jobs"]
        
        try:
            self.cursor.execute("SELECT job_id, position FROM job_postings WHERE company_id=? AND status='Active'", 
                              (self.company_id,))
            jobs = self.cursor.fetchall()
            for job_id, position in jobs:
                job_options.append(f"{job_id}: {position}")
        except:
            pass
        
        job_filter_menu = ttk.Combobox(filter_frame, textvariable=self.job_filter_var, 
                                      values=job_options, state="readonly", width=30)
        job_filter_menu.pack(side="left", padx=(0, 20))
        
        # Filter by status
        tk.Label(filter_frame, text="Filter by Status:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left", padx=(0, 10))
        
        self.status_filter_var = tk.StringVar(value="All")
        status_options = ["All", "Applied", "Shortlisted", "Selected", "Rejected", "Pending"]
        
        for status in status_options:
            tk.Radiobutton(filter_frame, text=status, variable=self.status_filter_var, value=status,
                         font=("Arial", 10), bg=self.WHITE, fg=self.TEXT_DARK,
                         command=self.filter_applications).pack(side="left", padx=5)
        
        # Applications table
        table_frame = tk.Frame(apps_frame, bg=self.WHITE)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("App ID", "Student", "Job", "Applied Date", "CGPA", "Status", "Actions")
        self.apps_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        col_widths = [80, 150, 150, 100, 80, 100, 150]
        for i, col in enumerate(columns):
            self.apps_tree.heading(col, text=col)
            self.apps_tree.column(col, width=col_widths[i])
        
        # Load applications
        self.load_applications_table()
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.apps_tree.yview)
        self.apps_tree.configure(yscrollcommand=scrollbar.set)
        
        self.apps_tree.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Context menu for applications
        self.apps_menu = tk.Menu(self.window, tearoff=0)
        self.apps_menu.add_command(label="View Profile", command=self.view_student_profile)
        self.apps_menu.add_command(label="Shortlist", command=self.shortlist_application)
        self.apps_menu.add_command(label="Schedule Interview", command=self.schedule_interview)
        self.apps_menu.add_command(label="Reject", command=self.reject_application)
        self.apps_menu.add_command(label="Make Offer", command=self.make_offer)
        
        self.apps_tree.bind("<Button-3>", self.show_apps_context_menu)
    
    def load_applications_table(self, job_filter="All Jobs", status_filter="All"):
        """Load applications into table"""
        # Clear existing items
        for item in self.apps_tree.get_children():
            self.apps_tree.delete(item)
        
        try:
            query = """
                SELECT a.application_id, s.Full_name, j.position, a.apply_date, 
                       s.CGPA, a.status, a.student_id
                FROM student_applications a
                LEFT JOIN job_postings j ON a.job_id = j.job_id
                LEFT JOIN student_table s ON a.student_id = s.Registration_no
                WHERE a.company_id = ?
            """
            params = [self.company_id]
            
            if job_filter != "All Jobs":
                job_id = job_filter.split(":")[0].strip()
                query += " AND a.job_id = ?"
                params.append(job_id)
            
            if status_filter != "All":
                query += " AND a.status = ?"
                params.append(status_filter)
            
            query += " ORDER BY a.apply_date DESC"
            
            self.cursor.execute(query, params)
            applications = self.cursor.fetchall()
            
            for app in applications:
                app_id, student_name, position, apply_date, cgpa, status, student_id = app
                
                # Format CGPA
                cgpa_str = f"{cgpa:.2f}" if cgpa else "N/A"
                
                # Status colors
                status_colors = {
                    'Applied': '#3b82f6',
                    'Shortlisted': '#10b981',
                    'Selected': '#059669',
                    'Rejected': '#dc2626',
                    'Pending': '#d97706'
                }
                status_color = status_colors.get(status, '#6b7280')
                
                self.apps_tree.insert('', 'end', values=(
                    app_id, student_name or "Unknown", position, 
                    apply_date[:10] if apply_date else "N/A",
                    cgpa_str, status, "Actions"
                ), tags=(app_id, student_id, status))
                
                # Configure tag colors
                self.apps_tree.tag_configure(status, foreground=status_color)
            
        except Exception as e:
            print(f"Error loading applications: {e}")
    
    def filter_applications(self):
        """Filter applications"""
        job_filter = self.job_filter_var.get()
        status_filter = self.status_filter_var.get()
        self.load_applications_table(job_filter, status_filter)
    
    def show_apps_context_menu(self, event):
        """Show context menu for applications"""
        item = self.apps_tree.identify_row(event.y)
        if item:
            self.apps_tree.selection_set(item)
            values = self.apps_tree.item(item, "values")
            self.selected_app_id = values[0]
            self.selected_student_id = self.apps_tree.item(item, "tags")[1]
            self.selected_app_status = self.apps_tree.item(item, "tags")[2]
            self.apps_menu.post(event.x_root, event.y_root)
    
    def view_student_profile(self):
        """View student profile"""
        if hasattr(self, 'selected_student_id'):
            self.view_student_profile_dialog(self.selected_student_id)
    
    def view_student_profile_dialog(self, student_id):
        """View student profile in dialog"""
        try:
            self.cursor.execute("SELECT * FROM student_table WHERE Registration_no=?", (student_id,))
            student = self.cursor.fetchone()
            
            if student:
                profile_window = tk.Toplevel(self.window)
                profile_window.title(f"Student Profile - {student_id}")
                profile_window.geometry("500x600")
                profile_window.configure(bg=self.WHITE)
                
                tk.Label(profile_window, text="Student Profile", 
                        font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=20)
                
                # Student info
                info_frame = tk.Frame(profile_window, bg=self.WHITE)
                info_frame.pack(fill="both", expand=True, padx=30, pady=10)
                
                student_info = [
                    ("Student ID:", student_id),
                    ("Full Name:", student[0]),
                    ("Email:", student[1]),
                    ("Phone:", student[2]),
                    ("Gender:", student[3]),
                    ("Branch:", student[5]),
                    ("Year:", student[6]),
                    ("CGPA:", str(student[7]) if student[7] else "N/A"),
                    ("CET/JEE Score:", str(student[8]) if len(student) > 8 and student[8] else "N/A"),
                    ("Current Company:", student[9] if len(student) > 9 and student[9] else "Not placed")
                ]
                
                for label, value in student_info:
                    row = tk.Frame(info_frame, bg=self.WHITE)
                    row.pack(fill="x", pady=8)
                    
                    tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                            bg=self.WHITE, fg=self.TEXT_DARK, width=15, anchor="w").pack(side="left")
                    tk.Label(row, text=value, font=("Arial", 11), 
                            bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="left", padx=10)
                
                # Close button
                tk.Button(profile_window, text="Close", font=("Arial", 12), 
                         bg=self.PRIMARY, fg="white", command=profile_window.destroy,
                         cursor="hand2", padx=30, pady=10).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load student profile: {str(e)}")
    
    def shortlist_application(self):
        """Shortlist an application"""
        if hasattr(self, 'selected_app_id'):
            try:
                self.cursor.execute("UPDATE student_applications SET status='Shortlisted' WHERE application_id=?", 
                                  (self.selected_app_id,))
                self.conn.commit()
                
                # Create notification for student
                self.cursor.execute("""
                    INSERT INTO notifications (user_id, user_type, title, message)
                    SELECT student_id, 'student', 'Application Shortlisted', 
                           'Your application has been shortlisted by ' || ?
                    FROM student_applications WHERE application_id = ?
                """, (self.company_info['name'], self.selected_app_id))
                
                self.conn.commit()
                
                messagebox.showinfo("Success", "Application shortlisted!")
                self.filter_applications()  # Refresh table
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to shortlist application: {str(e)}")
    
    def schedule_interview(self):
        """Schedule interview for application"""
        if hasattr(self, 'selected_app_id'):
            self.schedule_interview_dialog(self.selected_app_id)
    
    def schedule_interview_dialog(self, application_id):
        """Schedule interview dialog"""
        try:
            # Get application details
            self.cursor.execute("""
                SELECT a.student_id, a.job_id, j.position, s.Full_name
                FROM student_applications a
                LEFT JOIN job_postings j ON a.job_id = j.job_id
                LEFT JOIN student_table s ON a.student_id = s.Registration_no
                WHERE a.application_id = ?
            """, (application_id,))
            
            app_details = self.cursor.fetchone()
            if not app_details:
                messagebox.showerror("Error", "Application not found!")
                return
            
            student_id, job_id, position, student_name = app_details
            
            # Create interview window
            interview_window = tk.Toplevel(self.window)
            interview_window.title("Schedule Interview")
            interview_window.geometry("500x600")
            interview_window.configure(bg=self.WHITE)
            
            tk.Label(interview_window, text="Schedule Interview", 
                    font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=20)
            
            # Form frame
            form_frame = tk.Frame(interview_window, bg=self.WHITE)
            form_frame.pack(fill="both", expand=True, padx=30)
            
            # Student info
            tk.Label(form_frame, text=f"Student: {student_name or 'Unknown'}", 
                    font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(0, 10))
            tk.Label(form_frame, text=f"Position: {position or 'Unknown'}", 
                    font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(0, 20))
            
            # Interview date
            tk.Label(form_frame, text="Interview Date *", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            date_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
            date_entry.pack(fill="x", pady=(0, 15))
            try:
                date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            except:
                pass
            
            # Interview time
            tk.Label(form_frame, text="Interview Time *", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            time_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
            time_entry.pack(fill="x", pady=(0, 15))
            try:
                time_entry.insert(0, "10:00")
            except:
                pass
            
            # Interview mode
            tk.Label(form_frame, text="Interview Mode *", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            mode_var = tk.StringVar(value="Online")
            mode_combo = ttk.Combobox(form_frame, textvariable=mode_var, 
                                     values=["Online", "In-person", "Phone"], state="readonly", width=27)
            mode_combo.pack(fill="x", pady=(0, 15))
            
            # Venue/Platform
            tk.Label(form_frame, text="Venue/Platform *", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            venue_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
            venue_entry.pack(fill="x", pady=(0, 15))
            try:
                venue_entry.insert(0, "Google Meet / College Campus")
            except:
                pass
            
            # Interviewer
            tk.Label(form_frame, text="Interviewer Name", font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            interviewer_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
            interviewer_entry.pack(fill="x", pady=(0, 25))
            try:
                interviewer_entry.insert(0, self.company_info.get('hr_contact', ''))
            except:
                pass
            
            def schedule():
                try:
                    if not date_entry.get() or not time_entry.get() or not venue_entry.get():
                        messagebox.showwarning("Warning", "Please fill all required fields!")
                        return
                    
                    # Combine date and time
                    interview_datetime = f"{date_entry.get()} {time_entry.get()}:00"
                    
                    # Insert interview record
                    self.cursor.execute("""
                        INSERT INTO interviews 
                        (application_id, student_id, company_id, 
                         scheduled_date, interview_mode, venue, interviewer_name, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'Scheduled')
                    """, (
                        application_id,
                        student_id,
                        self.company_id,
                        interview_datetime,
                        mode_var.get(),
                        venue_entry.get(),
                        interviewer_entry.get()
                    ))
                    
                    # Update application status
                    self.cursor.execute("UPDATE student_applications SET status='Shortlisted' WHERE application_id=?", 
                                      (application_id,))
                    
                    self.conn.commit()
                    
                    # Create notification for student
                    self.cursor.execute("""
                        INSERT INTO notifications (user_id, user_type, title, message)
                        VALUES (?, 'student', 'Interview Scheduled', ?)
                    """, (student_id, f"Interview scheduled for {position} on {date_entry.get()} at {time_entry.get()}"))
                    
                    self.conn.commit()
                    
                    messagebox.showinfo("Success", "Interview scheduled successfully!")
                    interview_window.destroy()
                    self.filter_applications()  # Refresh
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to schedule interview: {str(e)}")
            
            def close_window():
                interview_window.destroy()
            
            # Button frame
            button_frame = tk.Frame(interview_window, bg=self.WHITE)
            button_frame.pack(pady=20, fill="x", padx=30)
            
            tk.Button(button_frame, text="Schedule Interview", font=("Arial", 12, "bold"), 
                     bg=self.PRIMARY, fg="white", command=schedule,
                     cursor="hand2", padx=30, pady=12).pack(side="left", padx=5)
            
            tk.Button(button_frame, text="Close", font=("Arial", 12, "bold"), 
                     bg="#6b7280", fg="white", command=close_window,
                     cursor="hand2", padx=30, pady=12).pack(side="left", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load application details: {str(e)}")
    
    def reject_application(self):
        """Reject an application"""
        if hasattr(self, 'selected_app_id'):
            try:
                self.cursor.execute("UPDATE student_applications SET status='Rejected' WHERE application_id=?", 
                                  (self.selected_app_id,))
                self.conn.commit()
                
                # Create notification for student
                self.cursor.execute("""
                    INSERT INTO notifications (user_id, user_type, title, message)
                    SELECT student_id, 'student', 'Application Update', 
                           'Your application status has been updated'
                    FROM student_applications WHERE application_id = ?
                """, (self.selected_app_id,))
                
                self.conn.commit()
                
                messagebox.showinfo("Success", "Application rejected!")
                self.filter_applications()  # Refresh table
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reject application: {str(e)}")
    
    def make_offer(self):
        """Make job offer to applicant"""
        if hasattr(self, 'selected_app_id'):
            try:
                # Get application details
                self.cursor.execute("""
                    SELECT a.student_id, j.position
                    FROM student_applications a
                    LEFT JOIN job_postings j ON a.job_id = j.job_id
                    WHERE a.application_id = ?
                """, (self.selected_app_id,))
                
                app_details = self.cursor.fetchone()
                if not app_details:
                    messagebox.showerror("Error", "Application not found!")
                    return
                
                student_id, position = app_details
                
                # Create offer window
                offer_window = tk.Toplevel(self.window)
                offer_window.title("Make Job Offer")
                offer_window.geometry("400x300")
                offer_window.configure(bg=self.WHITE)
                
                tk.Label(offer_window, text="Make Job Offer", 
                        font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=20)
                
                # Offer details
                tk.Label(offer_window, text=f"Position: {position}", 
                        font=("Arial", 12), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=10)
                
                tk.Label(offer_window, text="Package Offered:", 
                        font=("Arial", 11, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", padx=50, pady=(10, 5))
                package_entry = tk.Entry(offer_window, font=("Arial", 11), width=30)
                package_entry.pack(pady=(0, 15))
                
                tk.Label(offer_window, text="Joining Date:", 
                        font=("Arial", 11, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", padx=50, pady=(10, 5))
                join_date_entry = tk.Entry(offer_window, font=("Arial", 11), width=30)
                join_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
                join_date_entry.pack(pady=(0, 25))
                
                def make_offer_action():
                    try:
                        # Update application status
                        self.cursor.execute("""
                            UPDATE student_applications 
                            SET status='Selected', 
                                package_offered=?,
                                offer_date=?,
                                offer_status='Pending'
                            WHERE application_id=?
                        """, (
                            package_entry.get(),
                            join_date_entry.get(),
                            self.selected_app_id
                        ))
                        
                        self.conn.commit()
                        
                        # Create notification for student
                        self.cursor.execute("""
                            INSERT INTO notifications (user_id, user_type, title, message)
                            VALUES (?, 'student', 'Job Offer Received', ?)
                        """, (student_id, f"Congratulations! You received an offer for {position} from {self.company_info['name']}"))
                        
                        self.conn.commit()
                        
                        messagebox.showinfo("Success", "Job offer sent successfully!")
                        offer_window.destroy()
                        self.filter_applications()  # Refresh table
                        
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to send offer: {str(e)}")
                
                tk.Button(offer_window, text="Send Offer", font=("Arial", 12, "bold"), 
                         bg=self.SUCCESS, fg="white", command=make_offer_action,
                         cursor="hand2", padx=30, pady=12).pack(pady=20)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process offer: {str(e)}")
    
    def view_job_applications(self, job_id):
        """View applications for specific job"""
        self.show_applications()  # Go to applications page
        # Set the job filter
        self.job_filter_var.set(f"{job_id}: {self.get_job_title(job_id)}")
        self.filter_applications()
    
    def get_job_title(self, job_id):
        """Get job title by ID"""
        try:
            self.cursor.execute("SELECT position FROM job_postings WHERE job_id=?", (job_id,))
            result = self.cursor.fetchone()
            return result[0] if result else "Unknown Job"
        except:
            return "Unknown Job"
    
    def show_interviews(self):
        """Show interviews management page - COMPLETE WORKING"""
        self.clear_content()
        
        frame = tk.Frame(self.content_area, bg=self.WHITE)
        frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="Interview Management", font=("Arial", 24, "bold"), 
                bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Filter options
        filter_frame = tk.Frame(frame, bg=self.WHITE)
        filter_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(filter_frame, text="Filter by Status:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left", padx=(0, 10))
        
        self.interview_status_var = tk.StringVar(value="All")
        status_options = ["All", "Scheduled", "Completed", "Cancelled", "Rescheduled"]
        
        for status in status_options:
            tk.Radiobutton(filter_frame, text=status, variable=self.interview_status_var, value=status,
                         font=("Arial", 10), bg=self.WHITE, fg=self.TEXT_DARK,
                         command=self.filter_interviews).pack(side="left", padx=5)
        
        # Date filter
        tk.Label(filter_frame, text="Date:", 
                font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(side="left", padx=(20, 10))
        
        self.interview_date_var = tk.StringVar(value="All Dates")
        date_options = ["All Dates", "Today", "This Week", "This Month", "Upcoming"]
        
        date_menu = ttk.Combobox(filter_frame, textvariable=self.interview_date_var, 
                                values=date_options, state="readonly", width=15)
        date_menu.pack(side="left", padx=(0, 10))
        date_menu.bind("<<ComboboxSelected>>", lambda e: self.filter_interviews())
        
        # Interviews table
        table_frame = tk.Frame(frame, bg=self.WHITE)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Student", "Date & Time", "Mode", "Venue", "Status", "Actions")
        self.interviews_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        col_widths = [60, 140, 140, 100, 120, 100, 100]
        for i, col in enumerate(columns):
            self.interviews_tree.heading(col, text=col)
            self.interviews_tree.column(col, width=col_widths[i])
        
        # Load interviews
        self.load_interviews_table()
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.interviews_tree.yview)
        self.interviews_tree.configure(yscrollcommand=scrollbar.set)
        
        self.interviews_tree.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Context menu for interviews
        self.interview_menu = tk.Menu(self.window, tearoff=0)
        self.interview_menu.add_command(label="Update Status", command=self.update_interview_status)
        self.interview_menu.add_command(label="Reschedule", command=self.reschedule_interview)
        self.interview_menu.add_command(label="Add Feedback", command=self.add_interview_feedback)
        self.interview_menu.add_command(label="Cancel Interview", command=self.cancel_interview)
        
        self.interviews_tree.bind("<Button-3>", self.show_interview_context_menu)
    
    def load_interviews_table(self, status_filter="All", date_filter="All Dates"):
        """Load interviews into table"""
        # Clear existing items
        for item in self.interviews_tree.get_children():
            self.interviews_tree.delete(item)
        
        try:
            query = """
                SELECT i.interview_id, s.Full_name, i.scheduled_date, 
                       i.interview_mode, i.venue, i.status
                FROM interviews i
                LEFT JOIN student_table s ON i.student_id = s.Registration_no
                WHERE i.company_id = ?
            """
            params = [self.company_id]
            
            if status_filter != "All":
                query += " AND i.status = ?"
                params.append(status_filter)
            
            if date_filter != "All Dates":
                today = datetime.now().strftime("%Y-%m-%d")
                if date_filter == "Today":
                    query += " AND DATE(i.scheduled_date) = ?"
                    params.append(today)
                elif date_filter == "This Week":
                    query += " AND i.scheduled_date >= date('now', 'weekday 0', '-7 days')"
                elif date_filter == "This Month":
                    query += " AND strftime('%Y-%m', i.scheduled_date) = strftime('%Y-%m', 'now')"
                elif date_filter == "Upcoming":
                    query += " AND i.scheduled_date >= datetime('now')"
            
            query += " ORDER BY i.scheduled_date"
            
            self.cursor.execute(query, params)
            interviews = self.cursor.fetchall()
            
            for interview in interviews:
                interview_id, student_name, scheduled, mode, venue, status = interview
                
                # Format date
                if scheduled:
                    try:
                        formatted_date = datetime.strptime(scheduled, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %I:%M %p")
                    except:
                        formatted_date = scheduled
                else:
                    formatted_date = "N/A"
                
                # Status color
                status_colors = {
                    'Scheduled': '#10b981',
                    'Completed': '#059669',
                    'Cancelled': '#dc2626',
                    'Rescheduled': '#d97706'
                }
                status_color = status_colors.get(status, '#6b7280')
                
                self.interviews_tree.insert('', 'end', values=(
                    interview_id, student_name or "Unknown", formatted_date, 
                    formatted_date, mode or "N/A", venue or "N/A", 
                    status, "Actions"
                ), tags=(interview_id, status))
                
                # Configure tag colors
                self.interviews_tree.tag_configure(status, foreground=status_color)
            
        except Exception as e:
            print(f"Error loading interviews: {e}")
    
    def filter_interviews(self):
        """Filter interviews"""
        status_filter = self.interview_status_var.get()
        date_filter = self.interview_date_var.get()
        self.load_interviews_table(status_filter, date_filter)
    
    def show_interview_context_menu(self, event):
        """Show context menu for interviews"""
        item = self.interviews_tree.identify_row(event.y)
        if item:
            self.interviews_tree.selection_set(item)
            self.selected_interview_id = self.interviews_tree.item(item, "values")[0]
            self.interview_menu.post(event.x_root, event.y_root)
    
    def update_interview_status(self):
        """Update interview status"""
        if hasattr(self, 'selected_interview_id'):
            status_window = tk.Toplevel(self.window)
            status_window.title("Update Interview Status")
            status_window.geometry("300x200")
            status_window.configure(bg=self.WHITE)
            
            tk.Label(status_window, text="Select New Status:", 
                    font=("Arial", 12, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=20)
            
            status_var = tk.StringVar(value="Completed")
            status_options = ["Completed", "Scheduled", "Cancelled", "Rescheduled", "No Show"]
            
            for status in status_options:
                tk.Radiobutton(status_window, text=status, variable=status_var, value=status,
                             font=("Arial", 11), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", padx=50, pady=5)
            
            def update_status():
                try:
                    self.cursor.execute("UPDATE interviews SET status=? WHERE interview_id=?", 
                                      (status_var.get(), self.selected_interview_id))
                    self.conn.commit()
                    
                    messagebox.showinfo("Success", "Interview status updated!")
                    status_window.destroy()
                    self.filter_interviews()  # Refresh
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update status: {str(e)}")
            
            tk.Button(status_window, text="Update", font=("Arial", 12, "bold"), 
                     bg=self.PRIMARY, fg="white", command=update_status,
                     cursor="hand2", padx=20, pady=10).pack(pady=20)
    
    def reschedule_interview(self):
        """Reschedule interview"""
        if hasattr(self, 'selected_interview_id'):
            messagebox.showinfo("Info", "Use the 'Schedule Interview' feature to reschedule.")
    
    def add_interview_feedback(self):
        """Add interview feedback"""
        if hasattr(self, 'selected_interview_id'):
            feedback_window = tk.Toplevel(self.window)
            feedback_window.title("Add Interview Feedback")
            feedback_window.geometry("400x300")
            feedback_window.configure(bg=self.WHITE)
            
            tk.Label(feedback_window, text="Interview Feedback", 
                    font=("Arial", 16, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=20)
            
            tk.Label(feedback_window, text="Feedback:", 
                    font=("Arial", 11, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", padx=30, pady=(10, 5))
            
            feedback_text = tk.Text(feedback_window, font=("Arial", 11), height=8, width=40)
            feedback_text.pack(padx=30, pady=(0, 20))
            
            def save_feedback():
                try:
                    feedback = feedback_text.get("1.0", "end-1c")
                    self.cursor.execute("UPDATE interviews SET feedback=? WHERE interview_id=?", 
                                      (feedback, self.selected_interview_id))
                    self.conn.commit()
                    
                    messagebox.showinfo("Success", "Feedback saved successfully!")
                    feedback_window.destroy()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save feedback: {str(e)}")
            
            tk.Button(feedback_window, text="Save Feedback", font=("Arial", 12, "bold"), 
                     bg=self.PRIMARY, fg="white", command=save_feedback,
                     cursor="hand2", padx=20, pady=10).pack(pady=10)
    
    def cancel_interview(self):
        """Cancel interview"""
        if hasattr(self, 'selected_interview_id'):
            if messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel this interview?"):
                try:
                    self.cursor.execute("UPDATE interviews SET status='Cancelled' WHERE interview_id=?", 
                                      (self.selected_interview_id,))
                    self.conn.commit()
                    
                    messagebox.showinfo("Success", "Interview cancelled!")
                    self.filter_interviews()  # Refresh
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to cancel interview: {str(e)}")
    
    def show_shortlisted(self):
        """Show shortlisted candidates - COMPLETE WORKING"""
        self.clear_content()
        
        frame = tk.Frame(self.content_area, bg=self.WHITE)
        frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="Shortlisted Candidates", font=("Arial", 24, "bold"), 
                bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        try:
            self.cursor.execute("""
                SELECT a.application_id, s.Full_name, j.position, s.CGPA, s.Branch,
                       a.apply_date, a.status
                FROM student_applications a
                LEFT JOIN job_postings j ON a.job_id = j.job_id
                LEFT JOIN student_table s ON a.student_id = s.Registration_no
                WHERE a.company_id = ? AND a.status IN ('Shortlisted', 'Selected')
                ORDER BY a.apply_date DESC
            """, (self.company_id,))
            
            candidates = self.cursor.fetchall()
            
            if candidates:
                # Create table
                columns = ("Name", "Position", "CGPA", "Branch", "Applied Date", "Status", "Actions")
                tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
                
                col_widths = [120, 150, 80, 100, 100, 100, 100]
                for i, col in enumerate(columns):
                    tree.heading(col, text=col)
                    tree.column(col, width=col_widths[i])
                
                for candidate in candidates:
                    app_id, name, position, cgpa, branch, apply_date, status = candidate
                    
                    cgpa_str = f"{cgpa:.2f}" if cgpa else "N/A"
                    
                    tree.insert('', 'end', values=(
                        name or "Unknown", position, cgpa_str, branch or "N/A",
                        apply_date[:10] if apply_date else "N/A", status, "View"
                    ), tags=(app_id,))
                
                scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                
                tree.pack(side="left", fill="both", expand=True, padx=(0, 10))
                scrollbar.pack(side="right", fill="y")
                
                # Double click to view
                tree.bind("<Double-1>", lambda e: self.view_shortlisted_details(tree))
                
            else:
                tk.Label(frame, text="No shortlisted candidates yet", 
                        font=("Arial", 16), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=100)
                
        except Exception as e:
            print(f"Error loading shortlisted: {e}")
            tk.Label(frame, text="Error loading shortlisted candidates", 
                    font=("Arial", 16), bg=self.WHITE, fg=self.DANGER).pack(pady=100)
    
    def view_shortlisted_details(self, tree):
        """View shortlisted candidate details"""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            app_id = item['tags'][0]
            self.view_application_details(app_id)
    
    def view_application_details(self, application_id):
        """View application details"""
        try:
            self.cursor.execute("""
                SELECT a.*, s.*, j.position
                FROM student_applications a
                LEFT JOIN student_table s ON a.student_id = s.Registration_no
                LEFT JOIN job_postings j ON a.job_id = j.job_id
                WHERE a.application_id = ?
            """, (application_id,))
            
            app = self.cursor.fetchone()
            
            if app:
                details_window = tk.Toplevel(self.window)
                details_window.title("Application Details")
                details_window.geometry("500x400")
                details_window.configure(bg=self.WHITE)
                
                tk.Label(details_window, text="Application Details", 
                        font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=20)
                
                # Application info
                info_frame = tk.Frame(details_window, bg=self.WHITE)
                info_frame.pack(fill="both", expand=True, padx=30, pady=10)
                
                app_info = [
                    ("Application ID:", application_id),
                    ("Student Name:", app[12] if len(app) > 12 else "Unknown"),
                    ("Position:", app[24] if len(app) > 24 else "Unknown"),
                    ("Applied Date:", app[6] if len(app) > 6 else "N/A"),
                    ("Status:", app[7] if len(app) > 7 else "N/A"),
                    ("CGPA:", str(app[19]) if len(app) > 19 and app[19] else "N/A"),
                    ("Branch:", app[17] if len(app) > 17 else "N/A")
                ]
                
                for label, value in app_info:
                    row = tk.Frame(info_frame, bg=self.WHITE)
                    row.pack(fill="x", pady=8)
                    
                    tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                            bg=self.WHITE, fg=self.TEXT_DARK, width=15, anchor="w").pack(side="left")
                    tk.Label(row, text=value, font=("Arial", 11), 
                            bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="left", padx=10)
                
                # Close button
                tk.Button(details_window, text="Close", font=("Arial", 12), 
                         bg=self.PRIMARY, fg="white", command=details_window.destroy,
                         cursor="hand2", padx=30, pady=10).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load application details: {str(e)}")
    
    def show_analytics(self):
        """Show company analytics - COMPLETE WORKING"""
        self.clear_content()
        
        frame = tk.Frame(self.content_area, bg=self.WHITE)
        frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="Company Analytics", font=("Arial", 24, "bold"), 
                bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        try:
            # Get analytics data
            self.cursor.execute("""
                SELECT 
                    COUNT(DISTINCT job_id) as total_jobs,
                    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_jobs,
                    SUM(position_count) as total_positions
                FROM job_postings 
                WHERE company_id = ?
            """, (self.company_id,))
            job_stats = self.cursor.fetchone()
            
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total_apps,
                    SUM(CASE WHEN status = 'Selected' THEN 1 ELSE 0 END) as hired,
                    SUM(CASE WHEN status = 'Shortlisted' THEN 1 ELSE 0 END) as shortlisted
                FROM student_applications 
                WHERE company_id = ?
            """, (self.company_id,))
            app_stats = self.cursor.fetchone()
            
            # Stats cards
            stats_frame = tk.Frame(frame, bg=self.WHITE)
            stats_frame.pack(fill="x", pady=20)
            
            if job_stats and app_stats:
                total_jobs, active_jobs, total_positions = job_stats
                total_apps, hired, shortlisted = app_stats
                
                stats_cards = [
                    ("Total Jobs", total_jobs or 0, self.PRIMARY),
                    ("Active Jobs", active_jobs or 0, self.SUCCESS),
                    ("Total Positions", total_positions or 0, self.WARNING),
                    ("Total Applications", total_apps or 0, self.DANGER),
                    ("Hired Candidates", hired or 0, "#059669"),
                    ("Shortlisted", shortlisted or 0, "#d97706")
                ]
                
                for i, (title, value, color) in enumerate(stats_cards):
                    row = i // 3
                    col = i % 3
                    
                    if col == 0:
                        row_frame = tk.Frame(stats_frame, bg=self.WHITE)
                        row_frame.pack(fill="x", pady=10)
                    
                    card = tk.Frame(row_frame, bg="white", relief="solid", bd=1)
                    card.pack(side="left", fill="both", expand=True, padx=10, pady=10, ipady=25)
                    
                    tk.Label(card, text=str(value), font=("Arial", 28, "bold"), 
                            bg="white", fg=color).pack(pady=(10, 5))
                    tk.Label(card, text=title, font=("Arial", 12), 
                            bg="white", fg=self.TEXT_DARK).pack()
            
            # Applications by status chart
            tk.Label(frame, text="Applications by Status", 
                    font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(40, 10))
            
            self.cursor.execute("""
                SELECT status, COUNT(*) 
                FROM student_applications 
                WHERE company_id = ?
                GROUP BY status
            """, (self.company_id,))
            
            status_data = self.cursor.fetchall()
            
            if status_data:
                for status, count in status_data:
                    row = tk.Frame(frame, bg=self.WHITE)
                    row.pack(fill="x", pady=5, padx=100)
                    
                    tk.Label(row, text=status, font=("Arial", 11), 
                            bg=self.WHITE, fg=self.TEXT_DARK, width=15, anchor="w").pack(side="left")
                    
                    # Progress bar
                    max_count = max([c for _, c in status_data])
                    progress_width = 200
                    fill_width = (count / max_count) * progress_width if max_count > 0 else 0
                    
                    progress_bg = tk.Frame(row, bg="#e5e7eb", width=progress_width, height=20)
                    progress_bg.pack(side="left", padx=10)
                    progress_bg.pack_propagate(False)
                    
                    progress_fill = tk.Frame(progress_bg, bg=self.PRIMARY, width=fill_width)
                    progress_fill.pack(side="left", fill="y")
                    
                    tk.Label(row, text=str(count), font=("Arial", 11), 
                            bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="left", padx=10)
            
            # Top performing jobs
            tk.Label(frame, text="Top Performing Jobs", 
                    font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(40, 10))
            
            self.cursor.execute("""
                SELECT j.position, 
                       COUNT(a.application_id) as app_count,
                       SUM(CASE WHEN a.status = 'Selected' THEN 1 ELSE 0 END) as hired_count
                FROM job_postings j
                LEFT JOIN student_applications a ON j.job_id = a.job_id
                WHERE j.company_id = ?
                GROUP BY j.job_id
                ORDER BY app_count DESC
                LIMIT 5
            """, (self.company_id,))
            
            top_jobs = self.cursor.fetchall()
            
            if top_jobs:
                for position, app_count, hired_count in top_jobs:
                    row = tk.Frame(frame, bg=self.WHITE)
                    row.pack(fill="x", pady=5, padx=100)
                    
                    tk.Label(row, text=position, font=("Arial", 11), 
                            bg=self.WHITE, fg=self.TEXT_DARK, width=30, anchor="w").pack(side="left")
                    
                    tk.Label(row, text=f"📝 {app_count} apps", font=("Arial", 11), 
                            bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="left", padx=10)
                    
                    tk.Label(row, text=f"✅ {hired_count} hired", font=("Arial", 11), 
                            bg=self.WHITE, fg=self.SUCCESS).pack(side="left", padx=10)
            
        except Exception as e:
            print(f"Error loading analytics: {e}")
            tk.Label(frame, text="Error loading analytics", 
                    font=("Arial", 16), bg=self.WHITE, fg=self.DANGER).pack(pady=100)
    
    def show_company_profile(self):
        """Show company profile - COMPLETE WORKING"""
        self.clear_content()
        
        frame = tk.Frame(self.content_area, bg=self.WHITE)
        frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="Company Profile", font=("Arial", 24, "bold"), 
                bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        # Profile info
        info_frame = tk.Frame(frame, bg=self.WHITE, relief="solid", bd=1)
        info_frame.pack(fill="x", pady=10, padx=50, ipady=20)
        
        company_info = [
            ("Company ID:", self.company_info['company_id']),
            ("Company Name:", self.company_info['name']),
            ("Email:", self.company_info['email']),
            ("Phone:", self.company_info['phone']),
            ("Industry:", self.company_info['industry']),
            ("Location:", self.company_info['location']),
            ("HR Contact:", self.company_info['hr_contact']),
            ("Website:", self.company_info['website']),
            ("Requirements:", self.company_info['requirements'])
        ]
        
        for label, value in company_info:
            row = tk.Frame(info_frame, bg=self.WHITE)
            row.pack(fill="x", pady=8, padx=30)
            
            tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK, width=15, anchor="w").pack(side="left")
            tk.Label(row, text=value or "Not provided", font=("Arial", 11), 
                    bg=self.WHITE, fg=self.TEXT_LIGHT).pack(side="left", padx=10)
        
        # Edit button
        tk.Button(frame, text="Edit Profile", font=("Arial", 12, "bold"), 
                 bg=self.PRIMARY, fg="white", command=self.edit_company_profile,
                 cursor="hand2", padx=30, pady=12).pack(pady=30)
    
    def edit_company_profile(self):
        """Edit company profile"""
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Edit Company Profile")
        edit_window.geometry("500x600")
        edit_window.configure(bg=self.WHITE)
        
        tk.Label(edit_window, text="Edit Company Profile", 
                font=("Arial", 18, "bold"), bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=20)
        
        # Form fields
        form_frame = tk.Frame(edit_window, bg=self.WHITE)
        form_frame.pack(fill="both", expand=True, padx=30)
        
        fields = [
            ("Company Name:", "name", self.company_info['name']),
            ("Email:", "email", self.company_info['email']),
            ("Phone:", "phone", self.company_info['phone']),
            ("Industry:", "industry", self.company_info['industry']),
            ("Location:", "location", self.company_info['location']),
            ("HR Contact:", "hr_contact", self.company_info['hr_contact']),
            ("Website:", "website", self.company_info['website']),
            ("Requirements:", "requirements", self.company_info['requirements'])
        ]
        
        entries = {}
        
        for label, key, value in fields:
            tk.Label(form_frame, text=label, font=("Arial", 11, "bold"), 
                    bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w", pady=(10, 5))
            
            if key == "requirements":
                text_frame = tk.Frame(form_frame, bg=self.WHITE)
                text_frame.pack(fill="x", pady=(0, 15))
                
                scrollbar = tk.Scrollbar(text_frame)
                scrollbar.pack(side="right", fill="y")
                
                entry = tk.Text(text_frame, height=4, font=("Arial", 11),
                               yscrollcommand=scrollbar.set)
                entry.insert("1.0", value or "")
                entry.pack(side="left", fill="both", expand=True)
                scrollbar.config(command=entry.yview)
                entries[key] = entry
            else:
                entry = tk.Entry(form_frame, font=("Arial", 11), width=40)
                entry.insert(0, value or "")
                entry.pack(fill="x", pady=(0, 15))
                entries[key] = entry
        
        def save_profile():
            try:
                self.cursor.execute("""
                    UPDATE company_login 
                    SET name=?, email=?, phone=?, industry=?, location=?, 
                        hr_contact=?, website=?, requirements=?
                    WHERE id=?
                """, (
                    entries['name'].get(),
                    entries['email'].get(),
                    entries['phone'].get(),
                    entries['industry'].get(),
                    entries['location'].get(),
                    entries['hr_contact'].get(),
                    entries['website'].get(),
                    entries['requirements'].get("1.0", "end-1c") if 'requirements' in entries else entries['requirements'].get(),
                    self.company_id
                ))
                
                self.conn.commit()
                self.load_company_data()  # Reload data
                
                messagebox.showinfo("Success", "Profile updated successfully!")
                edit_window.destroy()
                self.show_company_profile()  # Refresh view
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {str(e)}")
        
        tk.Button(edit_window, text="Save Changes", font=("Arial", 12, "bold"), 
                 bg=self.PRIMARY, fg="white", command=save_profile,
                 cursor="hand2", padx=30, pady=12).pack(pady=20)
    
    def show_notifications(self):
        """Show company notifications - COMPLETE WORKING"""
        self.clear_content()
        
        frame = tk.Frame(self.content_area, bg=self.WHITE)
        frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="Notifications", font=("Arial", 24, "bold"), 
                bg=self.WHITE, fg=self.TEXT_DARK).pack(pady=(0, 20))
        
        try:
            self.cursor.execute("""
                SELECT notification_id, title, message, created_at, is_read
                FROM notifications
                WHERE user_id = ? AND user_type = 'company'
                ORDER BY created_at DESC
            """, (self.company_id,))
            
            notifications = self.cursor.fetchall()
            
            if notifications:
                for notif_id, title, message, created_at, is_read in notifications:
                    bg_color = self.LIGHT_BG if not is_read else self.WHITE
                    fg_color = self.TEXT_DARK if not is_read else self.TEXT_LIGHT
                    
                    notif_card = tk.Frame(frame, bg=bg_color, relief="solid", bd=1)
                    notif_card.pack(fill="x", pady=5, padx=20, ipady=15)
                    
                    # Notification content
                    content_frame = tk.Frame(notif_card, bg=bg_color)
                    content_frame.pack(fill="x", padx=20, pady=10)
                    
                    tk.Label(content_frame, text=title, 
                            font=("Arial", 12, "bold"), bg=bg_color, fg=fg_color).pack(anchor="w")
                    tk.Label(content_frame, text=message, 
                            font=("Arial", 11), bg=bg_color, fg=fg_color, wraplength=800, justify="left").pack(anchor="w", pady=(5, 0))
                    
                    # Date and mark as read
                    bottom_frame = tk.Frame(notif_card, bg=bg_color)
                    bottom_frame.pack(fill="x", padx=20, pady=(0, 10))
                    
                    tk.Label(bottom_frame, text=created_at[:10], 
                            font=("Arial", 10), bg=bg_color, fg=self.TEXT_LIGHT).pack(side="left")
                    
                    if not is_read:
                        tk.Button(bottom_frame, text="Mark as read", 
                                 font=("Arial", 10), bg=self.PRIMARY, fg="white",
                                 command=lambda nid=notif_id: self.mark_notification_read(nid),
                                 cursor="hand2", padx=10, pady=3).pack(side="right")
            
            else:
                tk.Label(frame, text="No notifications", 
                        font=("Arial", 16), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=100)
                
        except Exception as e:
            print(f"Error loading notifications: {e}")
            tk.Label(frame, text="No notifications available", 
                    font=("Arial", 16), bg=self.WHITE, fg=self.TEXT_LIGHT).pack(pady=100)
    
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        try:
            self.cursor.execute("UPDATE notifications SET is_read=1 WHERE notification_id=?", (notification_id,))
            self.conn.commit()
            self.show_notifications()  # Refresh
        except Exception as e:
            print(f"Error marking notification as read: {e}")
    
    def show_help(self):
        """Show help information"""
        messagebox.showinfo("Help", 
                          "For assistance, please contact:\n\n"
                          "📧 Email: placement@college.edu\n"
                          "📱 Phone: +91-XXXX-XXXXXX\n"
                          "🏢 Office: Training & Placement Cell\n\n"
                          "Or visit our help desk during college hours.")
    
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
        os.system('python cmp_login.py')

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    # For testing
    if len(sys.argv) > 1:
        company_id = sys.argv[1]
    else:
        company_id = "CMP001"  # Default for testing
    
    app = CompanyDashboard(company_id)
    app.run()