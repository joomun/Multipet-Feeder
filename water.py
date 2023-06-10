import serial
import time
import tkinter as tk
import tkinter.ttk as ttk

# Set up serial communication
ser = serial.Serial('/dev/ttyUSB0', 19200) # Change COM3 to the port used by your Arduino
time.sleep(2) # Wait for Arduino to reset

# Create GUI window
root = tk.Tk()
root.title("Water Tank Level")

# Create progress bar
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress_bar.pack(pady=10)

# Create label for percentage
percent_label = tk.Label(root, text="")
percent_label.pack(pady=5)

# Function to update progress bar and label
def update_progress():
    # Read water level data from serial communication
    data = ser.readline().decode().strip()
    if data.startswith("Water level:"):
        # Extract water level value
        level = int(data.split(":")[1])

        # Calculate percentage of tank filled
        percent_filled = int((level / 1023) * 100)

        # Update progress bar and label
        progress_bar['value'] = percent_filled
        percent_label.config(text=str(percent_filled) + "%")

    # Schedule next update
    root.after(100, update_progress)

# Start updating progress bar and label
update_progress()

# Start GUI loop
root.mainloop()

