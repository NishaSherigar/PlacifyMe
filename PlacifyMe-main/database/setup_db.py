# setup_db_correct.py - Place this in main folder and run
import sqlite3
import hashlib
from datetime import datetime
import os

def setup_database():
    print("🚀 Setting up PlacifyMe Database...")
    
    # Backup old database if exists
    if os.path.exists('registration_student.db'):
        backup_name = f'registration_student_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        os.rename('registration_student.db', backup_name)
        print(f"📦 Backed up old database as: {backup_name}")
    
    # Connect to new database
    conn = sqlite3.connect('registration_student.db')
    cur = conn.cursor()
    
    print("📊 Creating essential tables...")
    
    # 1. STUDENT SIGNUP (your original table)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_signUP (
        name TEXT NOT NULL,
        student_id TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        branch TEXT,
        year TEXT,
        cgpa REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("✅ Created student_signUP table")
    
    # 2. STUDENT TABLE (your original)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_table (
        Full_name TEXT,
        Email_Id TEXT,
        Phone_no TEXT,
        Gender TEXT,
        Registration_no TEXT PRIMARY KEY,
        Branch TEXT,
        Year TEXT,
        CGPA REAL,
        CET_JEE INTEGER,
        Company_Name TEXT
    )
    """)
    print("✅ Created student_table")
    
    # 3. COMPANY LOGIN (your original)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS company_login (
        name TEXT NOT NULL,
        id TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        industry TEXT,
        location TEXT,
        hr_contact TEXT,
        requirements TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("✅ Created company_login table")
    
    # 4. ADMIN (your original)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        user_name TEXT PRIMARY KEY,
        Password TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        role TEXT,
        department TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("✅ Created admin table")
    
    # 5. JOB POSTINGS (enhanced)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS job_postings (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id TEXT NOT NULL,
        company_name TEXT NOT NULL,
        position TEXT NOT NULL,
        salary TEXT,
        location TEXT,
        description TEXT,
        requirements TEXT,
        cgpa_cutoff REAL DEFAULT 0.0,
        eligible_branches TEXT,
        position_count INTEGER DEFAULT 1,
        application_deadline DATE,
        posting_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Active'
    )
    """)
    print("✅ Created job_postings table")
    
    # 6. STUDENT APPLICATIONS (enhanced)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_applications (
        application_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        job_id INTEGER NOT NULL,
        company_id TEXT NOT NULL,
        company_name TEXT NOT NULL,
        position TEXT NOT NULL,
        apply_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Applied',
        resume_path TEXT,
        interview_date TIMESTAMP,
        interview_status TEXT,
        offer_date DATE,
        package_offered TEXT
    )
    """)
    print("✅ Created student_applications table")
    
    # 7. NOTIFICATIONS (enhanced)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        user_type TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("✅ Created notifications table")
    
    # 8. INTERVIEWS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        interview_id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER NOT NULL,
        student_id TEXT NOT NULL,
        company_id TEXT NOT NULL,
        round_number INTEGER DEFAULT 1,
        interview_type TEXT,
        scheduled_date TIMESTAMP,
        interviewer_name TEXT,
        interview_mode TEXT,
        venue TEXT,
        status TEXT DEFAULT 'Scheduled',
        feedback TEXT
    )
    """)
    print("✅ Created interviews table")
    
    # 9. PLACEMENTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS placements (
        placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        company_id TEXT NOT NULL,
        job_id INTEGER NOT NULL,
        placement_date DATE,
        package TEXT,
        joining_date DATE,
        status TEXT DEFAULT 'Active'
    )
    """)
    print("✅ Created placements table")
    
    # 10. STUDENT DOCUMENTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_documents (
        doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        doc_type TEXT NOT NULL,
        file_path TEXT NOT NULL,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(student_id, doc_type)
    )
    """)
    print("✅ Created student_documents table")
    
    # 11. EVENTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        event_type TEXT,
        organizer TEXT,
        event_date TIMESTAMP,
        venue TEXT,
        status TEXT DEFAULT 'Upcoming'
    )
    """)
    print("✅ Created events table")
    
    # Insert default admin
    admin_password = "admin123"
    cur.execute("""
    INSERT OR IGNORE INTO admin (user_name, Password, email, role, department)
    VALUES (?, ?, ?, ?, ?)
    """, ('admin', admin_password, 'admin@college.edu', 'Administrator', 'Management'))
    
    # Insert TPO user
    cur.execute("""
    INSERT OR IGNORE INTO admin (user_name, Password, email, role, department)
    VALUES (?, ?, ?, ?, ?)
    """, ('tpo', 'tpo@123', 'tpo@college.edu', 'Placement Officer', 'Training & Placement'))
    
    # Insert sample company
    cur.execute("""
    INSERT OR IGNORE INTO company_login (name, id, password, email, industry)
    VALUES (?, ?, ?, ?, ?)
    """, ('Google', 'CMP001', 'google123', 'hr@google.com', 'IT'))
    
    # Insert sample student
    cur.execute("""
    INSERT OR IGNORE INTO student_signUP (name, student_id, password, email, branch, year)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ('John Doe', 'STU001', 'student123', 'john@college.edu', 'IT', '2024'))
    
    # Insert sample job
    cur.execute("""
    INSERT OR IGNORE INTO job_postings 
    (company_id, company_name, position, salary, location, description, cgpa_cutoff, eligible_branches)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ('CMP001', 'Google', 'Software Engineer', '₹12,00,000', 'Bangalore', 
          'Looking for talented software engineers', 7.5, 'IT,COMP'))
    
    conn.commit()
    
    print("\n🎉 Database setup completed!")
    print("\n📋 Default accounts created:")
    print("   Admin: admin / admin123")
    print("   TPO: tpo / tpo@123")
    print("   Student: STU001 / student123")
    print("   Company: CMP001 / google123")
    
    # Verify tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    
    print(f"\n📊 Total tables created: {len(tables)}")
    for table in tables:
        print(f"   ✓ {table[0]}")
    
    conn.close()

if __name__ == "__main__":
    setup_database()