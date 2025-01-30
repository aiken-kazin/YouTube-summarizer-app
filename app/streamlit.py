import streamlit as st
from main import get_result


# App Title
st.title("YouTube Video Summarizer")

# Input field for YouTube video link
video_url = st.text_input("Enter YouTube video link:", placeholder="https://www.youtube.com/watch?v=example_id")

# Button to process the link
if st.button("Generate Summary"):
    if video_url:
        # Extract the video ID
         with st.spinner("Processing..."):
            try:
                result = get_result(video_url)
                st.success(result)
            except Exception as e:
                st.error("Error processing the link. Please check the format.")
    else:
        st.error("Please enter a valid video link.")
