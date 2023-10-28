import tkinter as tk
from tkinter import Canvas
import meterfeeder as mf
import time

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

class QuantumPulse:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Pulse")
        self.canvas = Canvas(self.root, bg="white", height=400, width=400)
        self.canvas.pack(pady=20)
        
        self.rwba = RandomWalkBiasAmplifier(5)

        self.pulse()

    def pulse(self):
        frequency = mf.rand_uniform()
        
        # Apply bias amplification
        bit = int(frequency > 0.5)
        bias = self.rwba.process_bit(bit)
        if bias is not None:
            if bias == 1:
                frequency += 0.05
            else:
                frequency -= 0.05

        # Ensure frequency is within bounds
        frequency = max(0.1, min(0.9, frequency))

        # Draw the pulsating circle
        self.canvas.delete("circle")
        radius = 50 + (frequency * 100)
        self.canvas.create_oval(200-radius, 200-radius, 200+radius, 200+radius, fill="blue", tags="circle")

        # Schedule the next pulse
        self.root.after(int(1000 * frequency), self.pulse)

if __name__ == "__main__":
    mf.load_library()
    mf.get_devices()

    root = tk.Tk()
    app = QuantumPulse(root)
    root.mainloop()
