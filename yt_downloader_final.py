import yt_dlp
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', d.get('total_bytes_estimate', 1))
        percent = (downloaded / total) * 100
        status_label.config(text=f"Downloading: {percent:.2f}%")
        root.update_idletasks()  # Refresh the UI

def download_video(url):
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL")
        return
    
    ydl_opts = {
        "format": "best",
        "outtmpl": "%(title)s.%(ext)s",  # Saves as video title
        "progress_hooks": [progress_hook],  # Add the progress bar
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download complete!")
        status_label.config(text="Download Complete")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download: {e}")

def start_download():
    url = url_entry.get()
    threading.Thread(target=download_video, args=(url,), daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x200")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(pady=10)

tk.Label(frame, text="Enter YouTube URL:").pack()
url_entry = tk.Entry(frame, width=40)
url_entry.pack(pady=5)

tk.Button(frame, text="Download Video", command=start_download).pack(pady=5)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()