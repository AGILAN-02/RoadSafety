import streamlit as st
import os
import sqlite3
import time
from PIL import Image

# STREAMLIT PAGE CONFIG
st.set_page_config(page_title="Road Safety Demo", layout="wide")

DB = "mapping.db"
STORAGE = "storage"

# Ensure storage folder exists
os.makedirs(STORAGE, exist_ok=True)

########################
# DB UTIL FUNCTIONS
########################

def get_website_from_id(id_value):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT website FROM mapping WHERE id=?", (id_value,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def log_image(fname, website):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO imageslog (filename, website) VALUES (?,?)", (fname, website))
    conn.commit()
    conn.close()

def list_imgs(website):
    folder = os.path.join(STORAGE, website)
    if not os.path.exists(folder):
        return []
    files = sorted(os.listdir(folder), reverse=True)
    return [os.path.join(folder, f) for f in files]

########################
# UI LAYOUT
########################

st.title("📸 Road Safety Image Upload Demo")

tab1, tab2 = st.tabs(["Upload Image", "View Gallery"])

########################
# TAB 1 UPLOAD
########################

with tab1:
    st.subheader("Upload Image by ID")

    id_input = st.text_input("Enter ID (example: 605004)")
    img = st.file_uploader("Select Image", type=["jpg", "jpeg", "png"])

    if st.button("Upload"):
        if not id_input:
            st.error("ID Required")
        elif not img:
            st.error("Image Required")
        else:
            website = get_website_from_id(id_input)
            if not website:
                st.error("Invalid ID, No Website Found")
            else:
                # folder for website
                web_folder = os.path.join(STORAGE, website)
                os.makedirs(web_folder, exist_ok=True)

                # timestamp filename
                ts = int(time.time())
                ext = img.name.split(".")[-1]
                fname = f"{ts}.{ext}"
                save_path = os.path.join(web_folder, fname)

                with open(save_path, "wb") as f:
                    f.write(img.read())

                log_image(fname, website)

                st.success(f"Uploaded to {website} as {fname}")
                st.info("Open Gallery Tab to View")

########################
# TAB 2 GALLERY
########################

with tab2:
    st.subheader("View Stored Images by Website")

    website_query = st.text_input("Enter Website (example: pondicherry.com)")

    if st.button("Show Gallery"):
        imgs = list_imgs(website_query)
        if not imgs:
            st.warning("No Images Found")
        else:
            cols = st.columns(3)
            for i, p in enumerate(imgs):
                cols[i % 3].image(Image.open(p), caption=os.path.basename(p))
