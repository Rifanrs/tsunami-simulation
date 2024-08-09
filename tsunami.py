import numpy as np
import pyvista as pv
from pyvista import Plotter
from scipy.ndimage import gaussian_filter

# Parameter yang bisa diubah
Lx = 1000.0  # Panjang domain (m)
Ly = 1000.0  # Lebar domain (m)
D = 10.0     # Kedalaman laut (m)
g = 9.81     # Percepatan gravitasi (m/s^2)
T = 200.0    # Durasi simulasi (s)
dx = 10.0    # Resolusi spasial (m)
dy = 10.0    # Resolusi spasial (m)
dt = 0.1     # Resolusi temporal (s)

# Menghitung jumlah grid point
nx = int(Lx / dx)
ny = int(Ly / dy)
nt = int(T / dt)

# Inisialisasi array
eta = np.zeros((nx, ny))  # Elevasi permukaan air
eta_new = np.zeros((nx, ny))
u = np.zeros((nx, ny))    # Kecepatan aliran x
v = np.zeros((nx, ny))    # Kecepatan aliran y
u_new = np.zeros((nx, ny))
v_new = np.zeros((nx, ny))

# Kondisi awal: gelombang Gaussian di tengah domain
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)
eta = np.exp(-((X - Lx/2)**2 + (Y - Ly/2)**2) / (2 * (Lx/20)**2))

# Fungsi untuk memperbarui kondisi gelombang
def update_wave():
    global eta, eta_new, u, v, u_new, v_new

    # Menghitung kecepatan baru
    u_new[1:-1, 1:-1] = u[1:-1, 1:-1] - g * dt / dx * (eta[2:, 1:-1] - eta[1:-1, 1:-1])
    v_new[1:-1, 1:-1] = v[1:-1, 1:-1] - g * dt / dy * (eta[1:-1, 2:] - eta[1:-1, 1:-1])

    # Menghitung elevasi baru
    eta_new[1:-1, 1:-1] = eta[1:-1, 1:-1] - D * dt / dx * (u_new[1:-1, 1:-1] - u_new[:-2, 1:-1]) - D * dt / dy * (v_new[1:-1, 1:-1] - v_new[1:-1, :-2])

    # Memperbarui kondisi
    eta[:] = eta_new[:]
    u[:] = u_new[:]
    v[:] = v_new[:]

# Setup plot
plotter = pv.Plotter()
plotter.set_background('white')

# Membuat grid 3D
grid = pv.StructuredGrid(X, Y, eta)
plotter.add_mesh(grid, scalars=eta.ravel(), cmap='viridis', show_edges=True)

# Fungsi untuk memperbarui plot
def update_plot():
    update_wave()
    grid.points[:, 2] = eta.ravel()
    plotter.update()

# Callback function for the animation
def animate():
    for _ in range(nt):
        update_plot()
        plotter.update()
        plotter.render()

# Menjalankan animasi dengan key event
plotter.add_key_event("space", animate)

# Menampilkan plot
plotter.show()
