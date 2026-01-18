import time


class FakeAudioSpeaker:
    def speak(self, text):
        print(text)
        time.sleep(2)
