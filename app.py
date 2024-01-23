import tkinter as tk
from rtlsdr import RtlSdr
import numpy as np

def get_signal_strength(sdr):
    samples = sdr.read_samples(1024 * 1024)
    power = np.mean(np.abs(samples) ** 2)
    return 10 * np.log10(power)

def update_direction():
    strengths = [get_signal_strength(sdrs[i]) for i in range(4)]
    center_strength = get_signal_strength(sdr_center)

    direction = np.argmax(strengths)
    relative_gain = strengths[direction] - center_strength

    label_direction.config(text=f"Signal direction: {direction + 1}")
    label_gain.config(text=f"Relative gain: {relative_gain} dB")

    draw_arrow(direction)

def draw_arrow(direction):
    canvas.delete("arrow")  # Clear previous arrow

    center_x, center_y = 150, 150  # Center of the canvas
    length = 50

    angles = [45, 135, 225, 315]  # Angles for each direction
    angle = angles[direction]

    x = center_x + length * np.cos(np.radians(angle))
    y = center_y - length * np.sin(np.radians(angle))

    canvas.create_line(center_x, center_y, x, y, arrow=tk.LAST, tags="arrow")

def select_sdr(direction):
    selected_sdr = RtlSdr(device_index=direction)  # Use device_index instead of index
    selected_sdr.gain = gain_sliders[direction].get()
    sdrs[direction] = selected_sdr
    update_direction()

# GUI setup
root = tk.Tk()
root.title("Signal Direction GUI")

sdrs = [None] * 4
sdr_center = RtlSdr(device_index=4)  # Use device_index instead of index

label_direction = tk.Label(root, text="Signal direction: ")
label_gain = tk.Label(root, text="Relative gain: ")

gain_sliders = []
for i in range(4):
    slider = tk.Scale(root, from_=0, to=50, orient="horizontal", label=f"Receiver {i+1} Gain", length=200)
    slider.set(20)  # Initial gain value
    gain_sliders.append(slider)

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

button_front = tk.Button(root, text="Select Front SDR", command=lambda: select_sdr(0))
button_left = tk.Button(root, text="Select Left SDR", command=lambda: select_sdr(1))
button_right = tk.Button(root, text="Select Right SDR", command=lambda: select_sdr(2))
button_rear = tk.Button(root, text="Select Rear SDR", command=lambda: select_sdr(3))

label_direction.pack()
label_gain.pack()

for slider in gain_sliders:
    slider.pack()

button_front.pack()
button_left.pack()
button_right.pack()
button_rear.pack()

root.mainloop()