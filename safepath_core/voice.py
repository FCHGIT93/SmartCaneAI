import threading
import pyttsx3

from safepath_core.config import VOICE_RATE


class VoiceAssistant:
    def __init__(self):
        self._speaking = False
        self._lock = threading.Lock()

    @property
    def is_speaking(self):
        return self._speaking

    def _speak(self, message):
        with self._lock:
            self._speaking = True

            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", VOICE_RATE)
                engine.say(message)
                engine.runAndWait()
                engine.stop()

            except Exception as error:
                print("Voice error:", error)

            finally:
                self._speaking = False

    def speak_async(self, message):
        if self._speaking:
            return

        threading.Thread(
            target=self._speak,
            args=(message,),
            daemon=True,
        ).start()