############################################################
# Streamlit Version of Image Upload + Gallery Demo Project #
############################################################

import streamlit as st
import os
import sqlite3
import time
from PIL import Image

# Streamlit Page Config
st.set_page_config(page_title="Road Safety Demo", layout="wide")

# Database file (local demo)
DB = "mapping.db"

# Ensure storage folder exists
STORAGE = "storage"
os.makedirs(STORAGE, exist_ok=True)


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

st.title("📸 Road Safety Image Demo")

tab1, tab2 = st.tabs(["Upload Image", "View Gallery"])

#############################
# TAB 1 — UPLOAD
#############################

with tab1:
    st.header("Upload Image by ID")

    id_input = st.text_input("Enter ID (example: 605004)")
    uploaded_file = st.file_uploader("Choose Image", type=["jpg", "jpeg", "png"])

    if st.button("Upload"):
        if not id_input:
            st.error("ID is required")
        elif not uploaded_file:
            st.error("Image file is required")
        else:
            website = get_website_from_id(id_input)
            if not website:
                st.error("Invalid ID — No matching website found")
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

                st.success(f"Uploaded to {website} as {filename}")
                st.info(f"View gallery in next tab")


#############################
# TAB 2 — GALLERY
#############################

with tab2:
    st.header("View Images by Website")
    website_query = st.text_input("Enter Website (example: pondicherry.com)")

    if st.button("Show Gallery"):
        images = get_images_for_website(website_query)
        if not images:
            st.warning("No images found for this website")
        else:
            st.write(f"Showing images for **{website_query}**")
            cols = st.columns(3)
            idx = 0
            for img_path in images:
                col = cols[idx % 3]
                col.image(Image.open(img_path), caption=os.path.basename(img_path))
                idx += 1
