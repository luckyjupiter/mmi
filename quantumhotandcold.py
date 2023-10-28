import tkinter as tk
import meterfeeder as mf
import math

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

class QuantumHotAndCold:
    def __init__(self):
        # Initialize the main window
        self.window = tk.Tk()
        self.window.title("Quantum Hot and Cold")
        
        # Randomly select a starting target point on the grid
        self.target_x = int(mf.rand_uniform() * 10)
        self.target_y = int(mf.rand_uniform() * 10)
        
        # Apply bias amplification methods to potentially influence the target point
        bits = [int(mf.rand_uniform() > 0.5) for _ in range(1000)]
        if majority_voting(bits) == 1:
            self.target_x = (self.target_x + 1) % 10
        else:
            self.target_x = (self.target_x - 1) % 10

        rwba = RandomWalkBiasAmplifier(5)
        rwba_output = [rwba.process_bit(bit) for bit in bits]
        rwba_output = [output for output in rwba_output if output is not None]
        if rwba_output:
            if rwba_output[0] == 1:
                self.target_y = (self.target_y + 1) % 10
            else:
                self.target_y = (self.target_y - 1) % 10
        
        # Initialize game statistics
        self.attempts = 0
        self.hits = 0
        
        # Create the grid of buttons
        self.grid_buttons = []
        for i in range(10):
            row_buttons = []
            for j in range(10):
                btn = tk.Button(self.window, width=5, height=2, command=lambda x=i, y=j: self.check_guess(x, y))
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            self.grid_buttons.append(row_buttons)
        
        # Feedback label to display game status
        self.feedback_label = tk.Label(self.window, text="")
        self.feedback_label.grid(row=10, column=0, columnspan=10)
        
        # Start the main loop
        self.window.mainloop()

    def check_guess(self, x, y):
        """Check the player's guess and provide feedback."""
        distance = math.sqrt((x - self.target_x)**2 + (y - self.target_y)**2)
        color_intensity = min(255, int(distance * 25.5))
        
        if distance == 0:
            self.hits += 1
            feedback = "You found it!"
            self.target_x = int(mf.rand_uniform() * 10)
            self.target_y = int(mf.rand_uniform() * 10)
        elif distance < 3:
            feedback = "Hot!"
            self.grid_buttons[x][y].config(bg=f"#{255-color_intensity:02x}0000")
        else:
            feedback = "Cold!"
            self.grid_buttons[x][y].config(bg=f"#0000{color_intensity:02x}")
        
        self.attempts += 1
        accuracy = (self.hits / self.attempts) * 100
        
        self.feedback_label.config(text=f"{feedback} Accuracy: {accuracy:.2f}%")
        
if __name__ == "__main__":
    mf.load_library()
    mf.get_devices()
    QuantumHotAndCold()
