import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from gtts import gTTS
import pygame
import io
import cv2
import numpy as np

class GestureModule:
    def __init__(self, model_path='models/gesture_recognizer.task'):
        self.model_path = model_path

        # Initialize pygame mixer only if an audio device is available
        try:
            pygame.mixer.init()
        except pygame.error:
            print("No audio device found. Text-to-speech will be disabled.")
            self.mixer_initialized = False
        else:
            self.mixer_initialized = True

        BaseOptions = mp.tasks.BaseOptions
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        self.options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.IMAGE
        )

        self.recognizer = GestureRecognizer.create_from_options(self.options)
        self.last_spoken_gesture = None
        self.language = 'en'

        # Translation dictionary
        self.translation_dict = {
            "Closed_Fist": {"english": "Fist", "hindi": "मुट्ठी"},
            "Open_Palm": {"english": "Palm", "hindi": "हथेली"},
            "Pointing_Up": {"english": "Pointing Up", "hindi": "ऊपर इशारा"},
            "Thumb_Down": {"english": "Thumb Down", "hindi": "अंगूठा नीचे"},
            "Thumb_Up": {"english": "Thumb Up", "hindi": "अंगूठा ऊपर"},
            "Victory": {"english": "Victory", "hindi": "विजय"},
            "ILoveYou": {"english": "I Love You", "hindi": "मैं तुमसे प्यार करता हूँ"},
        }

    def speak(self, text, lang='en'):
        """Converts text to speech."""
        if not self.mixer_initialized:
            return

        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            pygame.mixer.music.load(audio_fp)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")

    def process_frame(self, frame):
        """Processes each frame, detects gestures, and returns frame + gesture data."""
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        gesture_recognition_result = self.recognizer.recognize(mp_image)

        detected_gesture = None  # Default if no gesture found

        if gesture_recognition_result.gestures:
            for gesture in gesture_recognition_result.gestures:
                gesture_name = gesture[0].category_name
                if gesture_name in self.translation_dict:
                    detected_gesture = gesture_name

                    # Speak only if new gesture detected
                    if gesture_name != self.last_spoken_gesture:
                        english_text = self.translation_dict[gesture_name]["english"]
                        hindi_text = self.translation_dict[gesture_name]["hindi"]

                        if self.language == 'en':
                            self.speak(english_text, lang='en')
                        else:
                            self.speak(hindi_text, lang='hi')

                        self.last_spoken_gesture = gesture_name

                    # Display text on screen
                    cv2.putText(frame, f"English: {self.translation_dict[gesture_name]['english']}",
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.putText(frame, f"Hindi: {self.translation_dict[gesture_name]['hindi']}",
                                (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Return both frame and gesture data
        return frame, detected_gesture

    def set_language(self, lang):
        """Changes the speaking/translation language."""
        self.language = lang
