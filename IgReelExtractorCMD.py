from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request
import threading

def get_video_source(url):
    if "instagram.com/reel/" not in url:
        print("Invalid Instagram Reel link. Please provide a valid link.")
        return

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
            print("Video source URL:")
            print(src)
        else:
            print("Video source not found.")

    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        driver.quit()

def download_video(url):
    try:
        filename = "video.mp4"
        urllib.request.urlretrieve(url, filename)
        print(f"The video has been downloaded as '{filename}'.")
    except Exception as e:
        print("An error occurred during download:", str(e))

def main():
    url = input("Enter Instagram Reel Link: ")

    source_thread = threading.Thread(target=get_video_source, args=(url,))
    source_thread.start()
    source_thread.join()

    download_option = input("Do you want to download the video? (y/n): ").lower()
    if download_option == 'y':
        download_thread = threading.Thread(target=download_video, args=(url,))
        download_thread.start()
        download_thread.join()

if __name__ == "__main__":
    main()