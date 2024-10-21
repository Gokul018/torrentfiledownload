import streamlit as st
from transmission_rpc import Client
import time
import os

def add_torrent_file(torrent_file):
    try:
        # Connect to the Transmission client
        client = Client(host='localhost', port=9091, username='your_username', password='your_password')

        # Add the torrent file to Transmission
        torrent = client.add_torrent(torrent_file)
        return torrent.id  # Return the torrent ID for status tracking
    except Exception as e:
        return f"Error: {e}"

def get_torrent_status(torrent_id):
    try:
        client = Client(host='localhost', port=9091, username='your_username', password='your_password')
        torrent = client.get_torrent(torrent_id)
        return torrent.status, torrent.progress
    except Exception as e:
        return "Error", 0

def main():
    st.title("Torrent File Downloader")

    # Upload .torrent file
    uploaded_file = st.file_uploader("Upload a .torrent file", type=["torrent"])

    if st.button("Add Torrent File"):
        if uploaded_file is not None:
            # Save the uploaded file temporarily
            with open("temp.torrent", "wb") as f:
                f.write(uploaded_file.getbuffer())

            torrent_id = add_torrent_file("temp.torrent")
            if isinstance(torrent_id, int):  # Check if a valid torrent ID was returned
                st.success(f"Torrent file added! Torrent ID: {torrent_id}")

                # Monitor the download progress
                with st.spinner("Downloading..."):
                    while True:
                        status, progress = get_torrent_status(torrent_id)
                        if status == "seeding":
                            st.success("Download complete!")
                            break
                        elif status == "downloading":
                            st.progress(progress / 100)  # Convert to percentage
                        else:
                            st.error("Error while downloading.")
                            break
                        time.sleep(5)  # Wait a bit before checking the status again
            else:
                st.error(torrent_id)  # Display the error message
            # Clean up the temporary file
            os.remove("temp.torrent")
        else:
            st.error("Please upload a valid .torrent file.")

if __name__ == '__main__':
    main()
