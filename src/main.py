import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from gesture_module import GestureModule

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.configure(bg="#E9F5F2")

        # App title
        self.title_label = tk.Label(
            window, 
            text="🤟 Sign Language Detector", 
            font=("Segoe UI", 22, "bold"),
            fg="#1B4D3E", 
            bg="#E9F5F2"
        )
        self.title_label.pack(pady=10)

        # Initialize gesture module
        self.gesture_module = GestureModule()

        # Video feed
        self.vid = cv2.VideoCapture(0)
        w = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Rounded video frame background
        self.video_frame = tk.Frame(window, bg="#D7F0E5", bd=2, relief="ridge")
        self.video_frame.pack(pady=10)

        self.canvas = tk.Canvas(self.video_frame, width=w, height=h, bg="#D7F0E5", highlightthickness=0)
        self.canvas.pack()

        # Language selection frame
        self.lang_frame = tk.Frame(window, bg="#E9F5F2")
        self.lang_frame.pack(pady=15)

        self.lang_label = tk.Label(
            self.lang_frame, 
            text="Currently Selected: English 🇬🇧",
            font=("Segoe UI", 12, "bold"),
            fg="#1B4D3E", 
            bg="#E9F5F2"
        )
        self.lang_label.pack(pady=5)

        # Modern buttons using ttk style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TButton",
            font=("Segoe UI", 11, "bold"),
            padding=6,
            relief="flat",
            background="#4BBF9A",
            foreground="white"
        )
        style.map("TButton", background=[("active", "#39A386")])

        self.btn_english = ttk.Button(self.lang_frame, text="English 🇬🇧", command=lambda: self.set_language("en"))
        self.btn_english.pack(side="left", padx=10)

        self.btn_hindi = ttk.Button(self.lang_frame, text="Hindi 🇮🇳", command=lambda: self.set_language("hi"))
        self.btn_hindi.pack(side="left", padx=10)

        # Footer label
        self.footer = tk.Label(
            window,
            text="Developed by Mini 🌸",
            font=("Segoe UI", 10, "italic"),
            fg="#4BBF9A",
            bg="#E9F5F2"
        )
        self.footer.pack(pady=5)

        # Video update loop
        self.delay = 15
        self.update()

        self.window.mainloop()

    def set_language(self, lang):
        self.gesture_module.set_language(lang)
        if lang == "en":
            self.lang_label.config(text="Currently Selected: English 🇬🇧")
        else:
            self.lang_label.config(text="Currently Selected: Hindi 🇮🇳")

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame, _ = self.gesture_module.process_frame(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

# Run the app
App(tk.Tk(), "Sign Language Detector")
