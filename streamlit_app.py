############################################################
# Streamlit Version - Road Safety Image Upload + Gallery   #
############################################################

import streamlit as st
import os
import sqlite3
import time
from PIL import Image
from datetime import datetime

# Database file
DB = "mapping.db"

# Ensure storage folder exists
STORAGE = "storage"
os.makedirs(STORAGE, exist_ok=True)

# Custom CSS to match the new design theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling */
    h1 {
        background: linear-gradient(135deg, #ff6b00 0%, #ffc107 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        letter-spacing: -1px;
        font-size: 42px !important;
        margin-bottom: 10px;
    }
    
    h2 {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
        font-size: 24px !important;
    }
    
    h3 {
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        font-weight: 600;
        padding: 12px 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff6b00 0%, #ffc107 100%);
        border-color: transparent;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
        font-family: 'Poppins', sans-serif;
        padding: 14px 18px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff6b00;
        box-shadow: 0 0 20px rgba(255, 107, 0, 0.3);
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b00 0%, #ffc107 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px 32px;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 107, 0, 0.5);
    }
    
    /* Success/Error/Warning messages */
    .stSuccess {
        background: rgba(76, 175, 80, 0.2);
        border: 1px solid rgba(76, 175, 80, 0.5);
        border-radius: 12px;
        color: #8BC34A;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.2);
        border: 1px solid rgba(244, 67, 54, 0.5);
        border-radius: 12px;
        color: #EF5350;
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.2);
        border: 1px solid rgba(255, 193, 7, 0.5);
        border-radius: 12px;
        color: #FFC107;
    }
    
    /* Info box */
    .stInfo {
        background: rgba(33, 150, 243, 0.2);
        border: 1px solid rgba(33, 150, 243, 0.5);
        border-radius: 12px;
        color: #42A5F5;
    }
    
    /* Labels */
    label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 13px !important;
    }
    
    /* Container background */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Image styling */
    img {
        border-radius: 16px;
        transition: transform 0.3s;
    }
    
    img:hover {
        transform: scale(1.05);
    }
    
    /* Markdown text */
    .stMarkdown {
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* Column spacing */
    div[data-testid="column"] {
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Page Config
st.set_page_config(
    page_title="🚦 Road Safety Demo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

#############################
# DB FUNCTIONS
#############################

def get_website_from_id(id_value):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT website FROM mapping WHERE id=?", (id_value,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def log_image(filename, website):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO imageslog (filename, website) VALUES (?,?)", (filename, website))
    conn.commit()
    conn.close()


def get_images_for_website(website):
    folder = os.path.join(STORAGE, website)
    if not os.path.exists(folder):
        return []
    files = sorted(os.listdir(folder), reverse=True)
    return [os.path.join(folder, f) for f in files]


#############################
# PAGE LOGIC
#############################

# Header with icon
st.markdown("<div style='text-align: center; font-size: 80px; margin-bottom: 20px;'>🚦</div>", unsafe_allow_html=True)
st.title("Road Safety Image Demo")
st.markdown("<p style='text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 16px; margin-bottom: 40px;'>Upload and monitor road safety conditions</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📤 Upload Image", "🖼️ View Gallery"])

#############################
# TAB 1 — UPLOAD
#############################

with tab1:
    st.markdown("### Upload Image by Location ID")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        id_input = st.text_input("📍 Location ID", placeholder="e.g., 605004", help="Enter the location ID")
        uploaded_file = st.file_uploader("📷 Choose Image", type=["jpg", "jpeg", "png", "webp"])
    
    with col2:
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        st.info("💡 **Tip:** Make sure you have the correct location ID before uploading.")

    if st.button("🚀 Upload Image"):
        if not id_input:
            st.error("❌ Location ID is required")
        elif not uploaded_file:
            st.error("❌ Image file is required")
        else:
            website = get_website_from_id(id_input)
            if not website:
                st.error("❌ Invalid ID — No matching website found")
            else:
                # Ensure per-website folder exists
                folder = os.path.join(STORAGE, website)
                os.makedirs(folder, exist_ok=True)

                # Save image with timestamp
                ts = int(time.time())
                ext = uploaded_file.name.split(".")[-1]
                filename = f"{ts}.{ext}"
                save_path = os.path.join(folder, filename)

                with open(save_path, "wb") as f:
                    f.write(uploaded_file.read())

                log_image(filename, website)

                st.success(f"✅ Successfully uploaded to **{website}** as `{filename}`")
                st.balloons()
                st.info("🎉 View your image in the **View Gallery** tab!")
                
                # Show preview
                st.markdown("### Preview")
                st.image(save_path, caption=f"Uploaded: {filename}", use_container_width=True)


#############################
# TAB 2 — GALLERY
#############################

with tab2:
    st.markdown("### View Images by Website")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        website_query = st.text_input("🌐 Website", placeholder="e.g., pondicherry.com")
    
    with col2:
        st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
        show_gallery = st.button("🔍 Show Gallery")

    if show_gallery and website_query:
        images = get_images_for_website(website_query)
        
        if not images:
            st.warning("⚠️ No images found for this website")
            st.markdown("""
            <div style='text-align: center; padding: 60px 20px; background: rgba(255, 255, 255, 0.05); 
                 border: 2px dashed rgba(255, 255, 255, 0.2); border-radius: 24px; margin-top: 30px;'>
                <div style='font-size: 80px; opacity: 0.3;'>📸</div>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 20px; margin-top: 20px;'>No images uploaded yet</div>
                <div style='color: rgba(255, 255, 255, 0.5); font-size: 14px; margin-top: 10px;'>Start by uploading your first road safety image</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"### 📍 {website_query}")
            st.markdown(f"**{len(images)} images found** (newest first)")
            
            # Stats
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Images", len(images), delta=None)
            with col2:
                st.metric("Location", "🚦 Active", delta=None)
            
            st.markdown("---")
            
            # Display images in grid
            cols = st.columns(3)
            for idx, img_path in enumerate(images):
                with cols[idx % 3]:
                    try:
                        img = Image.open(img_path)
                        st.image(img, caption=os.path.basename(img_path), use_container_width=True)
                        st.caption(f"🕐 {datetime.fromtimestamp(int(os.path.basename(img_path).split('.')[0])).strftime('%Y-%m-%d %H:%M:%S')}")
                    except:
                        st.caption(os.path.basename(img_path))
    elif not website_query and show_gallery:
        st.warning("⚠️ Please enter a website to view the gallery")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: rgba(255, 255, 255, 0.5); font-size: 12px;'>🚦 Road Safety Monitoring System | Built with Streamlit</p>", unsafe_allow_html=True)
