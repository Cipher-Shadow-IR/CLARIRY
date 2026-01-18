import pyttsx3


class TTSSpeaker:
    def speak(self, text):
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(text)
        engine.runAndWait()
