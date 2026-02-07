# 🎓 PlacifyMe – Complete Placement Management System

PlacifyMe is a **comprehensive placement management system** designed for educational institutions to efficiently manage the entire campus placement process. It provides **role-based portals** for **Students, Companies, Training & Placement Officers (TPOs), and Administrators**.

**Key Benefits:**
- ✅ **Centralized Platform**: All placement activities in one place
- ✅ **Automated Processes**: Reduce manual work and errors
- ✅ **Real-time Tracking**: Monitor applications and interviews
- ✅ **Data Analytics**: Generate insights and reports
- ✅ **Secure Access**: Role-based authentication and authorization

**Technology Stack:**
- **Frontend**: Python Tkinter (GUI)
- **Backend**: Python
- **Database**: SQLite
- **Version Control**: Git/GitHub
- **Dependencies**: Pillow, Matplotlib, Pandas

## ✨ Features

### 👨‍🎓 **Student Portal Features**
- **Profile Management**: Create and update personal profiles
- **Job Search**: Browse available job opportunities with filters
- **Application System**: Apply for jobs with one click
- **Document Upload**: Upload resumes, certificates, and other documents
- **Application Tracking**: Real-time status of all applications
- **Notifications**: Get alerts for new jobs, interviews, and updates
- **Interview Schedule**: View and confirm interview timings
- **Placement Status**: Track placement offers and acceptances

### 🏢 **Company Portal Features**
- **Company Registration**: Register and verify company profile
- **Job Posting**: Create detailed job listings with requirements
- **Application Review**: View and filter student applications
- **Candidate Shortlisting**: Shortlist candidates for interviews
- **Interview Scheduling**: Schedule and manage interview rounds
- **Offer Management**: Send job offers to selected candidates
- **Analytics Dashboard**: View application statistics and trends
- **Communication**: Send notifications to applicants

### 👨‍💼 **TPO (Placement Officer) Features**
- **Dashboard**: Overview of all placement activities
- **Student Management**: View and manage student profiles
- **Company Management**: Verify and manage company registrations
- **Job Approval**: Review and approve job postings
- **Placement Coordination**: Coordinate between students and companies
- **Report Generation**: Generate placement reports and statistics
- **Event Management**: Schedule placement drives and events
- **Monitoring**: Track all applications and interviews

### ⚙️ **Administrator Features**
- **System Dashboard**: Complete system overview and analytics
- **User Management**: Manage all users (students, companies, TPOs)
- **Database Management**: Backup, restore, and optimize database
- **System Settings**: Configure application settings
- **Notification Management**: Send system-wide notifications
- **Security Management**: Manage user roles and permissions
- **Audit Logs**: View system activities and logs
- **Data Export**: Export data in CSV/Excel formats

## 🚀 Installation

### Prerequisites
- **Python 3.8 or higher** (Download from [python.org](https://python.org))
- **Git** (for cloning repository)
- **Internet connection** (for downloading dependencies)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/placifyme.git
cd placifyme
```

#### 2. Install Dependencies
```bash
pip install pillow matplotlib pandas
```
*Note: Tkinter comes pre-installed with Python*

#### 3. Setup Database
```bash
python setup_db.py
```

#### 4. Verify Installation
```bash
python runplacifyme.py
```

## 🏁 Quick Start Guide

### For First-Time Users:

1. **Launch the Application:**
   ```bash
   python runplacifyme.py
   ```

2. **Choose Your Role:**
   - 👨‍🎓 Student
   - 🏢 Company
   - 👨‍💼 TPO
   - ⚙️ Administrator

3. **Login with Default Credentials:**

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| Administrator | `admin` | `admin123` | Full system access |
| TPO | `tpo` | `tpo@123` | Placement officer access |
| Student | `STU001` | `student123` | Student demo account |
| Company | `CMP001` | `google123` | Company demo account |

4. **Explore Your Dashboard:**
   - Navigate through sidebar menus
   - Use the top bar for quick actions
   - Check notifications for updates

## 🖼️ Screenshots

### 🔐 Home Page 
*PlacifyME HomePage with different roles*
<img width="1919" height="1007" alt="Image" src="https://github.com/user-attachments/assets/432fdc4c-c940-4c98-9742-ae5bb5355fa0" />

### 📊 Admin Dashboard
*Complete system overview with analytics*
![Admin Dashboard](https://via.placeholder.com/800x450.png?text=Admin+Dashboard+with+Analytics)

### 🏢 Company Portal
*Job posting and candidate management*
![Company Portal](https://via.placeholder.com/800x450.png?text=Company+Portal+-+Job+Management)

### 📈 Analytics Dashboard
*Placement statistics and charts*
![Analytics](https://via.placeholder.com/800x450.png?text=Placement+Analytics+Dashboard)

## 🎮 Usage Guide

### For Students:

#### Applying for Jobs:
1. **Login** to your student account
2. Click **"Browse Jobs"** from the sidebar
3. Use filters to find relevant jobs
4. Click **"Apply"** on desired job
5. Upload required documents
6. Track application status in **"My Applications"**

#### Uploading Documents:
1. Go to **"My Profile"**
2. Click **"Upload Documents"**
3. Select file (PDF/DOC/JPEG)
4. Choose document type
5. Click **"Upload"**
6. Verify upload status

### For Companies:

#### Posting a Job:
1. **Login** to company account
2. Click **"Post New Job"**
3. Fill job details:
   - Job Title & Description
   - Salary Package
   - Location & Work Mode
   - Requirements
   - Eligibility Criteria
4. Set application deadline
5. Click **"Post Job"**

#### Reviewing Applications:
1. Go to **"Applications"**
2. Filter by job or status
3. View applicant profiles
4. Shortlist candidates
5. Schedule interviews
6. Update application status

### For Administrators:

#### User Management:
1. Go to **"User Management"**
2. Select user type (Student/Company/Admin)
3. View all users
4. Add/Edit/Delete users
5. Reset passwords
6. Manage permissions

#### System Backup:
1. Go to **"Backup & Restore"**
2. Click **"Create Backup"**
3. Choose backup location
4. Confirm backup
5. Verify backup file

## 🔧 Troubleshooting

### Common Issues and Solutions:

#### 1. "Database not found" Error
**Problem:** Application can't find database file
**Solution:**
```bash
python setup_db.py
```

#### 2. "Module not found" Error
**Problem:** Missing Python packages
**Solution:**
```bash
pip install pillow matplotlib pandas
```

#### 3. Application Won't Start
**Problem:** GUI doesn't open
**Solutions:**
- Check Python version: `python --version`
- Ensure Tkinter is installed
- Run as administrator/root
- Check system logs

#### 4. Database Connection Issues
**Problem:** Can't connect to database
**Solutions:**
- Check file permissions
- Verify database exists
- Check for corruption
- Restore from backup

#### 5. Performance Issues
**Problem:** Application runs slowly
**Solutions:**
- Close unnecessary applications
- Clear temporary files
- Optimize database: `python -c "import sqlite3; conn = sqlite3.connect('registration_student.db'); conn.execute('VACUUM'); conn.close()"`

### System Requirements:

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10, macOS 10.14+, Ubuntu 18.04+ | Windows 11, macOS 12+, Ubuntu 20.04+ |
| RAM | 2 GB | 4 GB |
| Storage | 500 MB | 1 GB |
| Python | 3.8 | 3.10+ |
| Screen | 1366x768 | 1920x1080 |

