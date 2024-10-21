import streamlit as st
import libtorrent as lt
import time
import os

def download_magnet(magnet_link, save_path):
    ses = lt.session()
    ses.listen_on(6881, 6891)

    # Add magnet link
    h = ses.add_magnet_uri(magnet_link, {'save_path': save_path})
    
    # Progress loop
    while not h.is_seed():
        s = h.status()
        st.write(f'Downloaded: {s.progress * 100:.2f}%, Download Rate: {s.download_rate / 1000:.2f} kB/s')
        time.sleep(1)

    st.success(f"Download complete: {h.name()}")

# Streamlit UI
st.title("Magnet Link Downloader")

magnet_link = st.text_input("Enter Magnet Link:")
save_path = st.text_input("Enter Save Path:", value=os.path.expanduser("~"))

if st.button("Download"):
    if magnet_link:
        with st.spinner("Downloading..."):
            download_magnet(magnet_link, save_path)
    else:
        st.error("Please enter a valid magnet link.")
