from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from tkinter import ttk
import threading
import urllib.request

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

def download_video(url):
    try:
        filename = "video.mp4"
        urllib.request.urlretrieve(url, filename)
        messagebox.showinfo("Download Complete", f"The video has been downloaded as '{filename}'.")
    except Exception as e:
        messagebox.showerror("Error", "An error occurred during download: " + str(e))

def show_loading():
    loading_label.config(text="Processing...")
    loading_label.place(x=220, y=230)
    get_source_button.config(state=tk.DISABLED)
    copy_button.config(state=tk.DISABLED)
    download_button.config(state=tk.DISABLED)

def hide_loading():
    loading_label.place_forget()
    get_source_button.config(state=tk.NORMAL)
    copy_button.config(state=tk.NORMAL)
    download_button.config(state=tk.NORMAL)

def get_video_source():
    url = url_entry.get()

    if "instagram.com/reel/" not in url:
        messagebox.showerror("Error", "Invalid Instagram Reel link. Please provide a valid link.")
        return

    show_loading()

    def process_request():
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")

        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.implicitly_wait(10)
            driver.get(url)

            video = driver.find_element(By.XPATH, "//video")
            src = video.get_attribute('src')

            if src:
                result_text.config(state=tk.NORMAL)
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, src)
                result_text.config(state=tk.DISABLED)
                copy_button.config(state=tk.NORMAL)
                download_button.config(state=tk.NORMAL)
            else:
                result_text.config(state=tk.NORMAL)
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Video source not found.")
                result_text.config(state=tk.DISABLED)
                copy_button.config(state=tk.DISABLED)
                download_button.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", "An error occurred: " + str(e))
        finally:
            driver.quit()
            hide_loading()

    threading.Thread(target=process_request).start()

# Create the main window
root = tk.Tk()
root.title("Instagram Reel Video Source Extractor")

# Set a custom window size
root.geometry("600x400")

# Set background color
root.configure(bg="#F5F5F5")

# Create GUI components
title_label = ttk.Label(root, text="Instagram Reel Video Source Extractor", font=("Helvetica", 16, "bold"), background="#F5F5F5")
url_label = tk.Label(root, text="Enter Instagram Reel Link:", background="#F5F5F5")
url_entry = tk.Entry(root, width=50)
get_source_button = tk.Button(root, text="Get Video Source", command=get_video_source, background="#388E3C", fg="white")
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, state=tk.DISABLED)
copy_button = tk.Button(root, text="Copy", state=tk.DISABLED, command=lambda: copy_to_clipboard(result_text.get(1.0, tk.END)), background="#1976D2", fg="white")
download_button = tk.Button(root, text="Download", state=tk.DISABLED, command=lambda: download_video(result_text.get(1.0, tk.END).strip()), background="#D32F2F", fg="white")
loading_label = ttk.Label(root, text="", font=("Helvetica", 12, "bold"), background="#F5F5F5")

# Place components on the window
title_label.pack(pady=10)
url_label.pack(pady=5)
url_entry.pack(pady=5)
get_source_button.pack(pady=10)
result_text.pack(pady=10)
copy_button.pack()
download_button.pack()
loading_label.place(x=220, y=230)

# Start the GUI event loop
root.mainloop()
