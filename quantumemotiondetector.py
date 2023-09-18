import tkinter as tk
import win32com.client
import time
import sys

class RandomWalkBiasAmplifier:
    def __init__(self, bound):
        self.bound = bound
        self.counter = 0

    def process_bit(self, bit):
        if bit == 1:
            self.counter += 1
        else:
            self.counter -= 1

        if self.counter >= self.bound:
            self.counter = 0
            return 1
        elif self.counter <= -self.bound:
            self.counter = 0
            return 0

        return None

def majority_voting(bits):
    return 1 if bits.count(1) > len(bits) / 2 else 0

def loading_animation(duration):
    end_time = time.time() + duration
    animation_chars = ['|', '/', '-', '\\']
    idx = 0
    while time.time() < end_time:
        sys.stdout.write('\r' + 'Processing... ' + animation_chars[idx % len(animation_chars)])
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    sys.stdout.write('\r' + 'Done!          ')

class QuantumEmotionDetector:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quantum Emotion Detector")

        self.qng = win32com.client.Dispatch("QWQNG.QNG")

        self.emotions = ["happiness", "sadness", "anger", "fear", "surprise", "disgust"]

        self.label = tk.Label(self.window, text="Select an emotion you want to send to the computer:")
        self.label.pack(pady=20)

        self.selected_emotion = tk.StringVar()
        for emotion in self.emotions:
            tk.Radiobutton(self.window, text=emotion.capitalize(), variable=self.selected_emotion, value=emotion).pack(anchor=tk.W)

        self.detect_btn = tk.Button(self.window, text="Detect Emotion", command=self.detect_emotion)
        self.detect_btn.pack(pady=20)

        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack(pady=20)

        self.stats_label = tk.Label(self.window, text="Matches: 0 | Mismatches: 0")
        self.stats_label.pack(pady=20)

        self.matches = 0
        self.mismatches = 0

        self.window.mainloop()

    def detect_emotion(self):
        user_emotion = self.selected_emotion.get()
        if not user_emotion:
            self.result_label.config(text="Please select an emotion first.")
            return

        loading_animation(5)  # Simulate longer processing time

        bits = [int(self.qng.RandUniform > 0.5) for _ in range(100000)]
        majority_result = majority_voting(bits)

        rwba = RandomWalkBiasAmplifier(5)
        rwba_output = [rwba.process_bit(bit) for bit in bits]
        rwba_output = [output for output in rwba_output if output is not None]

        if rwba_output:
            bias = rwba_output[0]
        else:
            bias = majority_result

        index = int(self.qng.RandUniform * len(self.emotions))
        index = (index + bias) % len(self.emotions)

        detected_emotion = self.emotions[index]
        if detected_emotion == user_emotion:
            self.result_label.config(text=f"Detected emotion: {detected_emotion.capitalize()} (Match!)")
            self.matches += 1
        else:
            self.result_label.config(text=f"Detected emotion: {detected_emotion.capitalize()} (No Match)")
            self.mismatches += 1

        self.stats_label.config(text=f"Matches: {self.matches} | Mismatches: {self.mismatches}")

if __name__ == "__main__":
    QuantumEmotionDetector()
