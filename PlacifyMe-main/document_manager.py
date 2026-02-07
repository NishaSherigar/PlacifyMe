# document_manager.py
import os
import sqlite3
from tkinter import filedialog, messagebox
from datetime import datetime

class DocumentManager:
    def __init__(self, student_id):
        self.student_id = student_id
        self.documents_dir = "student_documents"
        self.create_documents_dir()
    
    def create_documents_dir(self):
        """Create documents directory structure"""
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)
        
        # Create student-specific folder
        student_dir = os.path.join(self.documents_dir, self.student_id)
        if not os.path.exists(student_dir):
            os.makedirs(student_dir)
    
    def upload_document(self, document_type, description=""):
        """Upload a document"""
        # Define allowed file types based on document type
        file_types = {
            "resume": [("PDF files", "*.pdf"), ("Word documents", "*.doc *.docx")],
            "marksheet_10th": [("PDF files", "*.pdf"), ("Image files", "*.jpg *.jpeg *.png")],
            "marksheet_12th": [("PDF files", "*.pdf"), ("Image files", "*.jpg *.jpeg *.png")],
            "degree": [("PDF files", "*.pdf"), ("Image files", "*.jpg *.jpeg *.png")],
            "id_proof": [("PDF files", "*.pdf"), ("Image files", "*.jpg *.jpeg *.png")],
            "other": [("All files", "*.*")]
        }
        
        file_path = filedialog.askopenfilename(
            title=f"Select {document_type.replace('_', ' ').title()}",
            filetypes=file_types.get(document_type, file_types["other"])
        )
        
        if file_path:
            try:
                # Get file info
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                
                # Check file size (max 10MB)
                if file_size > 10:
                    messagebox.showerror("Error", "File size should be less than 10MB")
                    return None
                
                # Create filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{self.student_id}_{document_type}_{timestamp}{os.path.splitext(file_name)[1]}"
                student_dir = os.path.join(self.documents_dir, self.student_id)
                new_filepath = os.path.join(student_dir, new_filename)
                
                # Copy the file
                with open(file_path, 'rb') as src_file:
                    with open(new_filepath, 'wb') as dst_file:
                        dst_file.write(src_file.read())
                
                # Save to database
                conn = sqlite3.connect('registration_student.db')
                cur = conn.cursor()
                
                # Create documents table if it doesn't exist
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS student_documents_new (
                        doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id TEXT NOT NULL,
                        doc_type TEXT NOT NULL,
                        doc_name TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        file_size REAL,
                        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Save document info
                cur.execute("""
                    INSERT INTO student_documents_new (student_id, doc_type, doc_name, file_path, file_size)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.student_id, document_type, file_name, new_filepath, file_size))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"{document_type.replace('_', ' ').title()} uploaded successfully!")
                return {
                    'name': file_name,
                    'path': new_filepath,
                    'size': f"{file_size:.2f} MB",
                    'type': document_type,
                    'date': timestamp
                }
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload document: {str(e)}")
                return None
        
        return None
    
    def get_student_documents(self):
        """Get all documents for a student"""
        documents = []
        
        try:
            conn = sqlite3.connect('registration_student.db')
            cur = conn.cursor()
            
            # Try to get documents from new table
            cur.execute("""
                SELECT doc_type, doc_name, file_path, file_size, upload_date 
                FROM student_documents_new 
                WHERE student_id=? 
                ORDER BY upload_date DESC
            """, (self.student_id,))
            
            rows = cur.fetchall()
            
            for row in rows:
                documents.append({
                    'type': row[0],
                    'name': row[1],
                    'path': row[2],
                    'size': f"{row[3]:.2f} MB" if row[3] else "N/A",
                    'date': row[4]
                })
            
            conn.close()
            
        except:
            # If table doesn't exist yet, return empty list
            pass
        
        return documents
    
    def open_document(self, file_path):
        """Open a document using default application"""
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            messagebox.showerror("Error", "File not found!")
    
    def delete_document(self, file_path):
        """Delete a document"""
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                
                # Remove from database
                conn = sqlite3.connect('registration_student.db')
                cur = conn.cursor()
                cur.execute("DELETE FROM student_documents_new WHERE file_path=?", (file_path,))
                conn.commit()
                conn.close()
                
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete document: {str(e)}")
                return False
        return False