import yt_dlp
import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
import requests
import os
ffmpeg_location = "/usr/bin/ffmpeg"

# --- Download Audio ---
def download_audio(url):
    # Initialize the progress bar
    progress_bar = st.progress(0)
    progress_text = st.empty()

    def progress_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes:
                percentage = downloaded_bytes / total_bytes
                progress_bar.progress(percentage)
                progress_text.text(f"Downloading: {percentage:.2%}")
        elif d['status'] == 'finished':
            progress_text.text("Video downloaded. Converting to MP3...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'outtmpl': '%(title)s.%(ext)s',
    }
    # --- Download MP3 ---
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])
        if result == 0:
            info_dict = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info_dict)
            mp3_filename = os.path.splitext(filename)[0] + '.mp3'
            return mp3_filename
        else:
            st.error('An error occurred during the download.')
            return None

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css('style/style.css')

# --- Load Assets ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://lottie.host/c44d283b-75aa-487f-a2f7-6b21820b5803/7ZlNDi9ocx.json")

def main():
    # --- Header ---
    st.title('Video to MP3 Converter')
    st.write('***For Educational purposes ONLY***')
    with st.container():
        with st.sidebar:
            st_lottie_spinner(lottie_coding, speed=1, loop=True, quality="high", height=200, width=200) 
            st_lottie(lottie_coding, speed=1, loop=True, quality="high", height=200, width=200)

    url = st.text_input('Enter Video URL:', value="https://youtu.be/GQe7YHqGe8c?si=BbZnZo11usmoJFa6")

    # --- Convert to MP3 ---
    with st.container():
        if st.button('Convert'):
            if url:
                with st.spinner('Processing...'):
                    filename = download_audio(url)
                    if filename and os.path.exists(filename):
                        with open(filename, 'rb') as file:
                            st.download_button(
                                label='Download MP3',
                                data=file,
                                file_name=filename,
                                mime='audio/mpeg'
                            )
                        # Optionally, remove the file after download
                        os.remove(filename)
            else:
                st.warning('Please enter a valid video URL.')

if __name__ == '__main__':
    main()