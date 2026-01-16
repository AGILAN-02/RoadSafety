import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'storage'
DB_PATH = 'mapping.db'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Ensure storage folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def lookup_website(id_value):
    """Look up website from mapping table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT website FROM mapping WHERE id = ?", (id_value,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_images_for_website(website):
    """Get all images for a website ordered by newest first"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT filename, uploaded_at FROM imageslog WHERE website = ? ORDER BY uploaded_at DESC",
        (website,)
    )
    images = cursor.fetchall()
    conn.close()
    return images

def log_image_upload(website, filename):
    """Log image upload to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO imageslog (website, filename, uploaded_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
        (website, filename)
    )
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Main upload page"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload"""
    # Validate inputs
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    id_value = request.form.get('id', '').strip()
    
    if file.filename == '' or not id_value:
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        return redirect(url_for('index'))
    
    # Lookup website from mapping table
    website = lookup_website(id_value)
    if not website:
        return redirect(url_for('index'))
    
    # Create website folder if it doesn't exist
    website_folder = os.path.join(UPLOAD_FOLDER, website)
    os.makedirs(website_folder, exist_ok=True)
    
    # Generate unique filename with timestamp
    file_ext = secure_filename(file.filename).rsplit('.', 1)[1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]  # microseconds shortened
    filename = f"{timestamp}.{file_ext}"
    
    # Save file
    filepath = os.path.join(website_folder, filename)
    file.save(filepath)
    
    # Log to database
    log_image_upload(website, filename)
    
    # Show success page instead of redirecting
    return render_template('success.html', website=website, filename=filename)

@app.route('/<website>')
def gallery(website):
    """Display gallery for a website"""
    # Get images for this website
    images = get_images_for_website(website)
    
    return render_template('gallery.html', website=website, images=images)

@app.route('/storage/<path:filename>')
def serve_image(filename):
    """Serve images from storage folder"""
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
