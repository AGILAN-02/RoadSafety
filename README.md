# Image Upload & Gallery Demo App

A simple Flask web application for uploading and viewing images organized by website.

## Features

- **Upload Page**: Upload images with an ID that maps to a website
- **Image Gallery**: View all images for a website ordered by newest first
- **Local Storage**: Images stored in `storage/<website>/` directories
- **SQLite Database**: Tracks ID-to-website mappings and image metadata

## Project Structure

```
project/
 ├─ app.py                  # Main Flask application
 ├─ init_db.py              # Database initialization script
 ├─ requirements.txt        # Python dependencies
 ├─ mapping.db              # SQLite database (auto-created)
 ├─ storage/                # Image storage folder
 │     ├─ xyz.com/
 │     ├─ abc.com/
 ├─ templates/
 │     ├─ upload.html       # Upload form page
 │     ├─ gallery.html      # Image gallery page
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

This creates:
- `mapping` table with sample data:
  - 101 → xyz.com
  - 102 → abc.com
- `imageslog` table for tracking uploads

### 3. Run the Application

```bash
python app.py
```

The app will start on: **http://127.0.0.1:5000**

## Usage

### Upload Images

1. Go to **http://127.0.0.1:5000/**
2. Enter an ID (101 or 102)
3. Select an image file
4. Click "Upload"
5. You'll be redirected to the gallery page

### View Gallery

- After upload, view images at **http://127.0.0.1:5000/xyz.com** or **http://127.0.0.1:5000/abc.com**
- Images are displayed newest first
- Each image shows upload timestamp

## Database Schema

### mapping table
```
id TEXT PRIMARY KEY          # e.g., "101"
website TEXT                 # e.g., "xyz.com"
```

### imageslog table
```
id INTEGER PRIMARY KEY AUTOINCREMENT
website TEXT                 # e.g., "xyz.com"
filename TEXT                # e.g., "20240116_143022_456.jpg"
uploaded_at DATETIME         # Auto-generated timestamp
```

## Supported Image Formats

- PNG, JPG, JPEG, GIF, BMP, WEBP

## Adding New Mappings

To add new ID-to-website mappings, edit `init_db.py` and re-run it:

```python
cursor.execute("INSERT INTO mapping (id, website) VALUES (?, ?)", ('103', 'newsite.com'))
```

Then restart the app.

## Notes

- Simple demo application (no authentication)
- Runs on local server only
- Images stored locally on disk
- Each upload gets a unique timestamped filename
- Full image metadata logged to database
