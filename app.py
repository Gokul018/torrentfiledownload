import streamlit as st
from transmission_rpc import Client

def add_magnet_link(magnet_link):
    try:
        # Connect to the Transmission client
        client = Client('localhost', port=9091, username='your_username', password='your_password')

        # Add the magnet link
        client.add_torrent(magnet_link)
        return "Magnet link added to Transmission!"
    except Exception as e:
        return f"Error: {e}"

def main():
    st.title("Magnet Link Downloader")

    magnet_link = st.text_input("Enter Magnet Link")

    if st.button("Add Magnet Link"):
        if magnet_link:
            result = add_magnet_link(magnet_link)
            st.success(result)
        else:
            st.error("Please enter a valid magnet link.")

if __name__ == '__main__':
    main()
