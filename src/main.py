import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from gesture_module import GestureModule

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Initialize the gesture module
        self.gesture_module = GestureModule()

        # Open the video source
        self.vid = cv2.VideoCapture(0)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Create a frame for the buttons
        self.btn_frame = tk.Frame(window, bg="white")
        self.btn_frame.pack(fill="both", expand="yes")

        # Add a label for the current language
        self.lang_label = tk.Label(self.btn_frame, text="Language: English")
        self.lang_label.pack(side="left", padx=10)

        # Add buttons to switch the language
        self.btn_english = ttk.Button(self.btn_frame, text="English", command=lambda: self.set_language("en"))
        self.btn_english.pack(side="left", padx=10)
        self.btn_hindi = ttk.Button(self.btn_frame, text="Hindi", command=lambda: self.set_language("hi"))
        self.btn_hindi.pack(side="left", padx=10)

        # After it is called once, the update method will be automatically called every 15 ms
        self.delay = 15
        self.update()

        self.window.mainloop()

    def set_language(self, lang):
        self.gesture_module.set_language(lang)
        self.lang_label.config(text=f"Language: {'English' if lang == 'en' else 'Hindi'}")

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()

        if ret:
            # Process the frame with the gesture module
            frame = self.gesture_module.process_frame(frame)

            # Convert the frame to a format that tkinter can use
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

# Create a window and pass it to the App object
App(tk.Tk(), "Sign Language Detector")
