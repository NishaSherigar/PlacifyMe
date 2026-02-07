# profile_photo_manager.py
import os
import sqlite3
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import tkinter as tk

class ProfilePhotoManager:
    def __init__(self, student_id):
        self.student_id = student_id
        self.profile_photos_dir = "profile_photos"
        self.create_profile_photos_dir()
        
    def create_profile_photos_dir(self):
        """Create directory for profile photos if it doesn't exist"""
        if not os.path.exists(self.profile_photos_dir):
            os.makedirs(self.profile_photos_dir)
    
    def get_photo_path(self):
        """Get the path for student's profile photo"""
        # Check for common image formats
        extensions = ['.jpg', '.jpeg', '.png', '.gif']
        for ext in extensions:
            photo_path = os.path.join(self.profile_photos_dir, f"{self.student_id}{ext}")
            if os.path.exists(photo_path):
                return photo_path
        return None
    
    def upload_photo(self, parent_window):
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
                # Get file extension
                _, ext = os.path.splitext(file_path)
                ext = ext.lower()
                
                if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                    messagebox.showerror("Error", "Please select a valid image file (JPG, PNG, GIF)")
                    return None
                
                # Create new filename
                new_filename = f"{self.student_id}{ext}"
                new_filepath = os.path.join(self.profile_photos_dir, new_filename)
                
                # Remove old photos if exist
                self.delete_existing_photos()
                
                # Copy the file
                with open(file_path, 'rb') as src_file:
                    with open(new_filepath, 'wb') as dst_file:
                        dst_file.write(src_file.read())
                
                messagebox.showinfo("Success", "Profile photo uploaded successfully!")
                return new_filepath
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload photo: {str(e)}")
                return None
        
        return None
    
    def delete_existing_photos(self):
        """Delete existing profile photos for the student"""
        extensions = ['.jpg', '.jpeg', '.png', '.gif']
        for ext in extensions:
            photo_path = os.path.join(self.profile_photos_dir, f"{self.student_id}{ext}")
            if os.path.exists(photo_path):
                os.remove(photo_path)
    
    def get_photo_image(self, size=(150, 150)):
        """Get photo as ImageTk object for display"""
        photo_path = self.get_photo_path()
        
        if photo_path and os.path.exists(photo_path):
            try:
                # Load and resize image
                image = Image.open(photo_path)
                image = image.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
            except Exception as e:
                print(f"Error loading image: {e}")
        
        # Return default avatar if no photo
        return self.get_default_avatar(size)
    
    def get_default_avatar(self, size=(150, 150)):
        """Generate a default avatar with initials"""
        from PIL import Image, ImageDraw, ImageFont
        import random
        
        # Create a colored avatar
        colors = ['#3b82f6', '#10b981', '#8b5cf6', '#ef4444', '#f59e0b']
        bg_color = random.choice(colors)
        
        # Create image
        img = Image.new('RGB', size, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to get student initials
            conn = sqlite3.connect('registration_student.db')
            cur = conn.cursor()
            cur.execute("SELECT name FROM student_signUP WHERE student_id=?", (self.student_id,))
            result = cur.fetchone()
            conn.close()
            
            if result:
                initials = ''.join([name[0] for name in result[0].split()[:2]]).upper()
            else:
                initials = "SU"
        except:
            initials = "SU"
        
        # Draw initials
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), initials, fill="white", font=font)
        
        return ImageTk.PhotoImage(img)

# Add this function to your student_dashboard.py
def add_profile_photo_section(self, parent_frame):
    """Add profile photo section to dashboard"""
    photo_frame = tk.Frame(parent_frame, bg="white", relief="solid", bd=1)
    photo_frame.pack(pady=10, padx=20, fill="x")
    
    tk.Label(photo_frame, text="Profile Photo", font=("Arial", 12, "bold"), 
            bg="white", fg="#1e293b").pack(pady=10)
    
    # Photo display
    self.photo_manager = ProfilePhotoManager(self.student_id)
    self.profile_photo_image = self.photo_manager.get_photo_image(size=(120, 120))
    
    self.photo_label = tk.Label(photo_frame, image=self.profile_photo_image, bg="white")
    self.photo_label.pack(pady=10)
    
    # Upload button
    tk.Button(photo_frame, text="Upload Photo", font=("Arial", 10), 
             bg=self.PRIMARY, fg="white", padx=15, pady=5,
             command=self.upload_profile_photo, cursor="hand2").pack(pady=10)

def upload_profile_photo(self):
    """Upload profile photo"""
    photo_path = self.photo_manager.upload_photo(self.window)
    if photo_path:
        # Refresh photo display
        self.profile_photo_image = self.photo_manager.get_photo_image(size=(120, 120))
        self.photo_label.config(image=self.profile_photo_image)
        messagebox.showinfo("Success", "Profile photo updated successfully!")