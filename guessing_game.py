"""
Quantum Random Number Prediction Game

This script uses the QWQNG API to generate quantum random numbers and predicts
the user's number (either 0 or 1) based on majority voting and Random Walk Bias Amplification.
"""

import win32com.client
import time
import sys

# Constants
NUM_BITS = 10000
RWBA_BOUND = 5

class RandomWalkBiasAmplifier:
    """Class to amplify bias using a random walk approach."""
    
    def __init__(self, bound):
        self.bound = bound
        self.counter = 0

    def process_bit(self, bit):
        """Process a single bit and adjust the counter based on its value."""
        
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
    """Return the majority value (0 or 1) from a list of bits."""
    
    return 1 if bits.count(1) > len(bits) / 2 else 0

def loading_animation(duration):
    """Display a loading animation for a specified duration."""
    
    end_time = time.time() + duration
    animation_chars = ['|', '/', '-', '\\']
    idx = 0
    while time.time() < end_time:
        sys.stdout.write('\r' + 'Predicting... ' + animation_chars[idx % len(animation_chars)])
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    sys.stdout.write('\r' + 'Prediction complete!   ')

def predict_number():
    """Predict a number between 0 and 1 using the QWQNG API."""
    
    qng = win32com.client.Dispatch("QWQNG.QNG")

    # Get bits from the generator for majority voting
    bits = [int(qng.RandUniform > 0.5) for _ in range(NUM_BITS)]
    base_prediction = majority_voting(bits)

    # Process bits through RWBA
    rwba = RandomWalkBiasAmplifier(RWBA_BOUND)
    rwba_output = [rwba.process_bit(bit) for bit in bits]
    rwba_output = [output for output in rwba_output if output is not None]

    # Adjust prediction based on RWBA
    if rwba_output:
        base_prediction = rwba_output[0]

    return base_prediction

def main():
    """Main game loop."""
    
    total_hits = 0
    total_attempts = 0

    while True:
        loading_animation(5)  # Display loading animation for 5 seconds
        predicted_number = predict_number()

        # Get the user's number
        try:
            user_number = int(input("\nEnter the number you were thinking of (0 or 1) or 'q' to quit: "))
            if user_number not in [0, 1]:
                print("Please enter either 0 or 1.")
                continue
        except ValueError:
            print("Thank you for playing!")
            break

        print(f"I predicted the number: {predicted_number}")

        # Check if the prediction was correct
        if predicted_number == user_number:
            total_hits += 1
            print("I guessed it right!")
        else:
            print("Oops! Better luck next time.")

        total_attempts += 1
        accuracy = (total_hits / total_attempts) * 100
        print(f"Accuracy so far: {accuracy:.2f}%")
        print("-" * 50)

if __name__ == "__main__":
    main()
