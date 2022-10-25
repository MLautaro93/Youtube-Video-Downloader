import tkinter as tk
from pytube import YouTube
from urllib import request
from PIL import Image, ImageTk
import io

# Create window
root = tk.Tk()
root.geometry('768x512')
root.resizable(False, False)
root.title('YouTube Video Downloader')
root.config(bg = 'red')

# Variables
link = tk.StringVar()
quality = tk.IntVar(value = 0)

# Labels and entries
header = tk.Label(text = 'Youtube Video Downloader', font = 'arial 15 bold', fg = 'white', bg = 'black')
header.pack()
link_label = tk.Label(text = 'Paste link here:', font = 'arial 10 bold', bg = 'red')
link_label.place(relx = .5, y = 50, anchor = tk.N)
link_entry = tk.Entry(width = 50, textvariable = link)
link_entry.place(relx = .5, y = 75, anchor = tk.N)

# Show function
def show(*args):
    try:
        video = YouTube(link.get())

        # Display title of the video
        title_label = tk.Label(text = video.title, font = 'arial 15 bold', fg = 'white', bg = 'red')
        title_label.place(relx = .5, y = 150, anchor = tk.N)

        # Display thumbnail
        raw_data = request.urlopen(video.thumbnail_url).read()
        img = Image.open(io.BytesIO(raw_data)).resize((320,180))
        image = ImageTk.PhotoImage(img)
        photo_label = tk.Label(image = image)
        photo_label.place(x = 150, y = 200, anchor = tk.NW)
        photo_label.image = image

        # Resolution options
        global options
        options = video.streams.filter(progressive = True).desc()
        resolution_label = tk.Label(text = 'Select resolution: ', font = 'arial 10 bold', bg = 'red')
        resolution_label.place(x = 500, y = 200, anchor = tk.NW)
        for op in options:
            tk.Radiobutton(text = f'{op.resolution} ({round(op.filesize / 1024 ** 2)} MB)',
            variable = quality,
            value = options.index(op),
            bg = 'red').place(x = 500, y = 250 + options.index(op) * 50, anchor = tk.NW)

        # Create download button
        download_button = tk.Button(text = 'Download', command = download)
        download_button.place(relx = .5, y = 425, anchor = tk.N)
        root.bind('<Return>', download)

    except:
        pass
   
# Download function
def download(*args):
    yt = options[quality.get()]
    yt.download()
    info_label = tk.Label(text = 'Download complete', font = 'arial 10 bold', fg = 'white', bg = 'green')
    info_label.place(relx = .5, y = 475, anchor = tk.N) 
    
# Call "show function" when entry box is modified
link.trace('w', show)

root.mainloop()