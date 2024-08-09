import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)
dx = 500  # Spatial resolution (m)
dy = 500  # Spatial resolution (m)
dt = 2  # Time step (s)
x_max = 200000  # Length of the simulated ocean (m)
y_max = 200000  # Width of the simulated ocean (m)

# Function to calculate wave speed
def wave_speed(depth):
    return np.sqrt(g * depth)

def run_simulation(H0, L, D, T, dx, dy, dt, x_max, y_max):
    # Wave parameters
    speed = wave_speed(D)
    k = 2 * np.pi / L  # Wave number
    omega = np.sqrt(g * k * np.tanh(k * D))  # Angular frequency

    # Spatial arrays
    x = np.arange(0, x_max, dx)
    y = np.arange(0, y_max, dy)
    X, Y = np.meshgrid(x, y)

    # Time array
    time = np.arange(0, T, dt)

    # Initialize wave height array
    heights = np.zeros((len(time), len(y), len(x)))

    # Initial single peak wave shape
    initial_position = x_max / 10
    heights[0, :, :] = H0 * np.exp(-((X - initial_position) / 20000)**2)  # Gaussian-shaped peak

    # Function to update wave heights over time
    for t in range(1, len(time)):
        phase = omega * time[t]
        heights[t, :, :] = H0 * np.exp(-((X - speed * time[t] - initial_position) / 20000)**2) * np.cos(phase)

    # Set up the figure and axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, heights[0, :, :], cmap='viridis')

    ax.set_title('Moving Wave Simulation')
    ax.set_xlabel('Distance X (m)')
    ax.set_ylabel('Distance Y (m)')
    ax.set_zlabel('Wave Height (m)')
    ax.set_zlim(-H0, H0)

    # Animation function
    def animate(i):
        ax.clear()
        ax.plot_surface(X, Y, heights[i, :, :], cmap='viridis')
        ax.set_title('Moving Wave Simulation')
        ax.set_xlabel('Distance X (m)')
        ax.set_ylabel('Distance Y (m)')
        ax.set_zlabel('Wave Height (m)')
        ax.set_zlim(-H0, H0)
        return ax,

    # Create the animation
    ani = animation.FuncAnimation(fig, animate, frames=len(time), interval=50, blit=False)

    plt.show()

# Create the main application window
root = tk.Tk()
root.title("Moving Wave Simulation")

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
H0_scale = create_label_scale(frame, "Initial Wave Height (m):", 1, 100, 50, 0, 0)
L_scale = create_label_scale(frame, "Wavelength (m):", 10000, 500000, 200000, 3, 0)
D_scale = create_label_scale(frame, "Ocean Depth (m):", 1000, 10000, 5000, 6, 0)
T_scale = create_label_scale(frame, "Total Simulation Time (s):", 100, 5000, 1200, 9, 0)
dx_scale = create_label_scale(frame, "Spatial Resolution X (m):", 100, 1000, 500, 12, 0)

# Second column
dy_scale = create_label_scale(frame, "Spatial Resolution Y (m):", 100, 1000, 500, 0, 1)
dt_scale = create_label_scale(frame, "Time Step (s):", 1, 100, 2, 3, 1)
x_max_scale = create_label_scale(frame, "Simulation Area Size X (m):", 50000, 500000, 200000, 6, 1)
y_max_scale = create_label_scale(frame, "Simulation Area Size Y (m):", 50000, 500000, 200000, 9, 1)

# Create a button to start the simulation
def on_run_button():
    H0 = float(H0_scale.get())
    L = float(L_scale.get())
    D = float(D_scale.get())
    T = float(T_scale.get())
    dx = float(dx_scale.get())
    dy = float(dy_scale.get())
    dt = float(dt_scale.get())
    x_max = float(x_max_scale.get())
    y_max = float(y_max_scale.get())
    
    run_simulation(H0, L, D, T, dx, dy, dt, x_max, y_max)

run_button = ttk.Button(frame, text="Run Simulation", command=on_run_button)
run_button.grid(row=15, column=0, columnspan=2, padx=5, pady=20)

# Start the GUI event loop
root.mainloop()
