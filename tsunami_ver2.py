import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)
dx = 500  # Spatial resolution (m)
dy = 500  # Spatial resolution (m)
dt = 2    # Time step (s)
x_max = 200000  # Length of the simulated ocean (m)
y_max = 200000  # Width of the simulated ocean (m)

# Function to calculate wave speed
def wave_speed(depth):
    return np.sqrt(g * depth)

# Get user inputs
H0 = float(input("Enter initial wave height (m): "))
L = float(input("Enter wavelength (m): "))
D = float(input("Enter ocean depth (m): "))
T = float(input("Enter total simulation time (s): "))

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
