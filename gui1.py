import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)
depth = 5000  # Ocean depth (m)
wave_length = 200000  # Wavelength (m)
wave_height = 50  # Initial wave height near the source (m)
duration = 1200  # Total simulation time (s)
dx = dy = 500  # Spatial resolution (m)
dt = 10  # Time step (s)
x_max = y_max = 1000000  # Size of the simulated area (m)

# Function to calculate wave speed
def wave_speed(depth):
    return np.sqrt(g * depth)

def run_simulation(depth, wave_length, wave_height, duration, dx, dy, dt, x_max, y_max):
    # Wave parameters
    speed = wave_speed(depth)
    k = 2 * np.pi / wave_length  # Wave number
    omega = np.sqrt(g * k * np.tanh(k * depth))  # Angular frequency

    # Spatial arrays
    x = np.arange(0, x_max, dx)
    y = np.arange(0, y_max, dy)
    X, Y = np.meshgrid(x, y)

    # Time array
    time = np.arange(0, duration, dt)

    # Initialize wave height array
    heights = np.zeros((len(time), len(y), len(x)))

    # Initial wave shape (tsunami near the source)
    heights[0, :, :] = wave_height * np.exp(-((X - x_max / 2)**2 + (Y - y_max / 2)**2) / (2 * (wave_length / 4)**2))

    # Function to update wave heights over time
    for t in range(1, len(time)):
        phase = omega * time[t]
        heights[t, :, :] = wave_height * np.exp(-((X - speed * time[t] - x_max / 2)**2 + (Y - y_max / 2)**2) / (2 * (wave_length / 4)**2)) * np.cos(k * (X - speed * time[t] - x_max / 2) + phase)

    # Set up the figure and axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, heights[0, :, :], cmap='viridis')

    ax.set_title('Tsunami Simulation')
    ax.set_xlabel('Distance X (m)')
    ax.set_ylabel('Distance Y (m)')
    ax.set_zlabel('Wave Height (m)')
    ax.set_zlim(0, wave_height)

    # Animation function
    def animate(i):
        ax.clear()
        surf = ax.plot_surface(X, Y, heights[i, :, :], cmap='viridis')
        ax.set_title('Tsunami Simulation')
        ax.set_xlabel('Distance X (m)')
        ax.set_ylabel('Distance Y (m)')
        ax.set_zlabel('Wave Height (m)')
        ax.set_zlim(0, wave_height)
        return surf,

    # Create the animation
    ani = animation.FuncAnimation(fig, animate, frames=len(time), interval=50, blit=False)

    plt.show()

# Create the main application window
root = tk.Tk()
root.title("Tsunami Simulation")

# Create sliders for simulation parameters with value display
def create_label_scale(frame, text, from_, to, default, row, col):
    label = ttk.Label(frame, text=text)
    label.grid(row=row, column=col, padx=5, pady=5, sticky='w')
    scale = ttk.Scale(frame, from_=from_, to=to, orient='horizontal')
    scale.grid(row=row+1, column=col, padx=5, pady=5, sticky='ew')
    value_label = ttk.Label(frame, text=str(default))
    value_label.grid(row=row+2, column=col, padx=5, pady=5)

    def update_value_label(event):
        value_label.config(text=f"{scale.get():.2f}")

    scale.set(default)
    scale.bind("<Motion>", update_value_label)
    scale.bind("<ButtonRelease-1>", update_value_label)
    
    return scale

frame = ttk.Frame(root, padding="10")
frame.pack(fill='both', expand=True)

# First column
depth_scale = create_label_scale(frame, "Ocean Depth (m):", 1000, 10000, 5000, 0, 0)
wave_length_scale = create_label_scale(frame, "Wavelength (m):", 50000, 500000, 200000, 3, 0)
wave_height_scale = create_label_scale(frame, "Initial Wave Height (m):", 10, 100, 50, 6, 0)
duration_scale = create_label_scale(frame, "Simulation Duration (s):", 300, 3600, 1200, 9, 0)
dx_scale = create_label_scale(frame, "Spatial Resolution X (m):", 100, 1000, 500, 12, 0)

# Second column
dy_scale = create_label_scale(frame, "Spatial Resolution Y (m):", 100, 1000, 500, 0, 1)
dt_scale = create_label_scale(frame, "Time Step (s):", 1, 100, 10, 3, 1)
x_max_scale = create_label_scale(frame, "Simulation Area Size X (m):", 100000, 2000000, 1000000, 6, 1)
y_max_scale = create_label_scale(frame, "Simulation Area Size Y (m):", 100000, 2000000, 1000000, 9, 1)

# Create a button to start the simulation
def on_run_button():
    depth = float(depth_scale.get())
    wave_length = float(wave_length_scale.get())
    wave_height = float(wave_height_scale.get())
    duration = float(duration_scale.get())
    dx = float(dx_scale.get())
    dy = float(dy_scale.get())
    dt = float(dt_scale.get())
    x_max = float(x_max_scale.get())
    y_max = float(y_max_scale.get())
    
    run_simulation(depth, wave_length, wave_height, duration, dx, dy, dt, x_max, y_max)

run_button = ttk.Button(frame, text="Run Simulation", command=on_run_button)
run_button.grid(row=15, column=0, columnspan=2, padx=5, pady=20)

# Start the GUI event loop
root.mainloop()
