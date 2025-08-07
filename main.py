import tkinter as tk
import speech_recognition as sr
import threading

TARGET_WORD = "استغفر الله"  # Arabic word to detect

class VoiceCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Istighfar")
        self.count = 0
        self.listening = False

        self.label = tk.Label(root, text=f"Say Istighfar", font=("Arial", 20))
        self.label.pack(pady=10)

        self.counter_label = tk.Label(root, text=str(self.count), font=("Arial", 48))
        self.counter_label.pack(pady=20)

        self.toggle_button = tk.Button(root, text="Start Taswih", command=self.toggle_listening, font=("Arial", 14))
        self.toggle_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_counter, font=("Arial", 14))
        self.reset_button.pack(pady=10)

    def reset_counter(self):
        self.count = 0
        self.update_counter()   
        if self.listening:
            self.toggle_listening()

    def toggle_listening(self):
        self.listening = not self.listening
        self.toggle_button.config(text="Stop" if self.listening else "Start Taswih")

        if self.listening:
            threading.Thread(target=self.listen_loop, daemon=True).start()

    def listen_loop(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

        while self.listening:
            with mic as source:
                try:
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio, language="ar").strip()
                    print("Recognized:", text)

                    if TARGET_WORD in text:
                        self.count += 1
                        self.update_counter()
                except sr.WaitTimeoutError:
                    print("Timeout, retrying...")
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(f"API Error: {e}")
                    break

    def update_counter(self):
        self.counter_label.config(text=str(self.count))

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceCounterApp(root)
    root.mainloop()
