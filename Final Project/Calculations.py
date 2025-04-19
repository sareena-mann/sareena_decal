import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton
from matplotlib.animation import FuncAnimation
import pandas as pd

# Constants
G = 1.32712440018e11  # Solar gravitational constant (km^3/s^2)


def kepler_eq(E, M, e):
    return E - e * np.sin(E) - M


def true_anomaly(E, e):
    return 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))


def orbit_positions(e, a, i, w, Omega, TP, num_points=1000):
    i = np.radians(i)
    w = np.radians(w)
    Omega = np.radians(Omega)

    # Generate mean anomalies over one period
    M_vals = np.linspace(0, 2 * np.pi, num_points)
    positions = []

    for M in M_vals:
        E = newton(kepler_eq, M, args=(M, e))
        nu = true_anomaly(E, e)
        r = a * (1 - e ** 2) / (1 + e * np.cos(nu))

        # Position in orbital plane
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)
        z_orb = 0

        # Rotate to 3D space
        x = r * (np.cos(Omega) * np.cos(w + nu) - np.sin(Omega) * np.sin(w + nu) * np.cos(i))
        y = r * (np.sin(Omega) * np.cos(w + nu) + np.cos(Omega) * np.sin(w + nu) * np.cos(i))
        z = r * (np.sin(w + nu) * np.sin(i))
        positions.append([x, y, z])

    return np.array(positions)


def animate(cometName):
    df = pd.read_csv("near-earth-comets.csv")
    comet_row = df[(df["Object"].str.lower() == cometName.lower()) |
                   (df["Object_name"].str.lower() == cometName.lower())]

    if comet_row.empty:
        raise ValueError(f"No comet found with name {cometName}")

    e = comet_row["e"].values[0]
    a = comet_row["q"].values[0] / (1 - e)  # Compute semi-major axis from perihelion distance
    i = comet_row["i"].values[0]
    w = comet_row["w"].values[0]
    Omega = comet_row["Node"].values[0]
    TP = comet_row["TP"].values[0]
    num_points = 1000

    positions = orbit_positions(e, a, i, w, Omega, TP, num_points)

    # Animation setup
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    line, = ax.plot([], [], [], lw=2, color='blue')
    point, = ax.plot([], [], [], 'ro')  # comet head

    # Set axis limits for clarity
    max_val = np.max(np.abs(positions)) * 1.1
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_zlim(-max_val, max_val)
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    ax.set_title(f"Orbit of {cometName}")

    def init():
        line.set_data([], [])
        line.set_3d_properties([])
        point.set_data([], [])
        point.set_3d_properties([])
        return line, point

    def update(frame):
        line.set_data(positions[:frame, 0], positions[:frame, 1])
        line.set_3d_properties(positions[:frame, 2])
        point.set_data([positions[frame, 0]], [positions[frame, 1]])  # Use list for single point
        point.set_3d_properties([positions[frame, 2]])
        return line, point

    ani = FuncAnimation(fig, update, frames=len(positions), init_func=init,
                        interval=20, blit=True)

    plt.show()
    return ani  # Return animation object to keep it alive