import urllib.request
from pathlib import Path
import requests

# Find the exact place of he raw image URL link and return it.
class MyParser:
    def find_url_image(self, file):
        self.file = file
        decoded_file = file.read_text(encoding='UTF-8')
        for i in range(1000):
            if 'property="og:image"' in (decoded_file.split())[i]:
                url = (decoded_file.split())[i + 1]
        if url:
            raw_url = url.lstrip('"content=""')
            raw_url = raw_url.replace('"', '')
            return raw_url
        else:
            return 0

    def find_url_video(self, file):
        self.file = file
        decoded_file = file.read_text(encoding='UTF-8')
        for i in range(1000):
            if '"og:video"' in (decoded_file.split())[i]:
                url = (decoded_file.split())[i + 1]
        if url:
            raw_url = url.lstrip('"content=""')
            raw_url = raw_url.replace('"', '')
            return raw_url
        else:
            return 0

# Save the image file in a sequence in the same directory
class processSave:
    def saveImage(imagePathURL):
        response = requests.get(imagePathURL)
        image_name = "saved_image_1.png"
        image_counter = 0

        while True:
            if Path(image_name).exists():
                image_counter += 1
                image_name = f'saved_image_{image_counter}.png'
            else:
                Path(image_name).touch()
                break
        out = open(image_name, 'wb')
        out.write(response.content)
        print(f'Saved: {Path(image_name)}')

    def saveVideo(videoPathURL):
        response = requests.get(videoPathURL)
        video_name = "saved_video_1.mp4"
        video_counter = 0

        while True:
            if Path(video_name).exists():
                video_counter += 1
                video_name = f'saved_video_{video_counter}.mp4'
            else:
                Path(video_name).touch()
                break
        out = open(video_name, 'wb')
        out.write(response.content)
        print(f'Saved: {Path(video_name)}')


print("Welcome to instagram Photo/Video Downloader")

url = input("Enter Instagram URL: ")
if len(url) > 45:
    print("This is a private account content")
else:
    headers = {'User-Agent' : 'Mozilla/5.0'}
    try:
        response = urllib.request.urlopen(url)
        source_code = response.read()

        file = Path('source_code.txt')
        file.write_bytes(source_code)
        parser = MyParser()

        while True:
            try:
                img_or_video = input("Please choose [1] for image, [2] for video: ")

                if img_or_video == "1":
                    # Processing the image
                    image_raw_url = parser.find_url_image(file)
                    file.unlink()
                    processSave.saveImage(image_raw_url)
                    break

                elif img_or_video == "2":
                    # Processing the video
                    video_raw_url = parser.find_url_video(file)
                    if video_raw_url:
                        file.unlink()
                        processSave.saveVideo(video_raw_url)
                        break
                else:
                    print("Wrong selection")
            except:
                pass
    except ValueError:
        print("Invalid URL")
