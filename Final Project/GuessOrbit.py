import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton
from matplotlib.animation import FuncAnimation
import pandas as pd
import matplotlib
import Calculations

# Set Matplotlib backend to TkAgg for compatibility with tkinter
matplotlib.use('TkAgg')
G = 1.32712440018e11

def guess_orbit(comet_name, df, num_points=1000, perturbation=0.05):
    """
    Generate an estimated (guessed) orbit by perturbing orbital elements and compare to actual orbit.

    Parameters:
    - comet_name: Name of the comet (e.g., '1P/Halley')
    - df: DataFrame containing comet data
    - num_points: Number of points in the orbit
    - perturbation: Fractional perturbation for orbital elements (e.g., 0.05 for ±5%)

    Returns:
    - actual_positions: Array of [x, y, z] positions for the actual orbit
    - guess_positions: Array of [x, y, z] positions for the guessed orbit
    - actual_params: Actual orbital elements [e, q, i, w, Omega, TP]
    - guess_params: Guessed orbital elements [e, q, i, w, Omega, TP]
    """
    # Find comet data
    comet_row = df[(df["Object"].str.lower() == comet_name.lower()) |
                   (df["Object_name"].str.lower() == comet_name.lower())]
    if comet_row.empty:
        raise ValueError(f"No comet found with name {comet_name}")

    # Extract actual orbital elements
    try:
        e = float(comet_row["e"].values[0])
        q = float(comet_row["q"].values[0])
        i = float(comet_row["i"].values[0])
        w = float(comet_row["w"].values[0])
        Omega = float(comet_row["Node"].values[0])
        TP = float(comet_row["TP"].values[0])
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid data for comet {comet_name}: {str(e)}")

    actual_params = [e, q, i, w, Omega, TP]
    a = q / (1 - e)  # Semi-major axis

    # Generate actual orbit positions
    actual_positions = Calculations.orbit_positions(e, a, i, w, Omega, TP, num_points)

    # Perturb orbital elements for the guess
    np.random.seed(42)  # For reproducibility
    e_guess = e * (1 + np.random.uniform(-perturbation, perturbation))
    q_guess = q * (1 + np.random.uniform(-perturbation, perturbation))
    i_guess = i * (1 + np.random.uniform(-perturbation, perturbation))
    w_guess = w * (1 + np.random.uniform(-perturbation, perturbation))
    Omega_guess = Omega * (1 + np.random.uniform(-perturbation, perturbation))
    TP_guess = TP + np.random.uniform(-10, 10)  # Perturb TP by ±10 days
    guess_params = [e_guess, q_guess, i_guess, w_guess, Omega_guess, TP_guess]
    a_guess = q_guess / (1 - e_guess)

    # Ensure valid parameters
    e_guess = np.clip(e_guess, 0, 0.999)  # Keep eccentricity < 1
    q_guess = max(q_guess, 0.01)  # Ensure positive perihelion distance
    a_guess = max(a_guess, 0.01)  # Ensure positive semi-major axis

    # Generate guessed orbit positions
    guess_positions = Calculations.orbit_positions(e_guess, a_guess, i_guess, w_guess, Omega_guess, TP_guess, num_points)

    return actual_positions, guess_positions, actual_params, guess_params


def compare_orbits(actual_positions, guess_positions, noise_level=0.01):
    """
    Compare actual and guessed orbits and perform error analysis.

    Parameters:
    - actual_positions: Array of [x, y, z] positions for actual orbit
    - guess_positions: Array of [x, y, z] positions for guessed orbit
    - noise_level: Assumed standard deviation of positional errors (AU)

    Returns:
    - residuals: Array of position differences
    - error_metrics: Dictionary with mean residual, std residual, chi-squared, reduced chi-squared
    """
    residuals = guess_positions - actual_positions
    mean_residual = np.mean(np.abs(residuals))
    std_residual = np.std(residuals)
    chi_squared = np.sum((residuals / noise_level) ** 2)
    degrees_of_freedom = len(residuals.flatten()) - 6  # 6 parameters
    reduced_chi_squared = chi_squared / degrees_of_freedom

    error_metrics = {
        'mean_residual': mean_residual,
        'std_residual': std_residual,
        'chi_squared': chi_squared,
        'reduced_chi_squared': reduced_chi_squared
    }

    return residuals, error_metrics


def plot_orbit_comparison(comet_name, actual_positions, guess_positions, residuals):
    """
    Plot actual vs. guessed orbits and residual distribution.

    Parameters:
    - comet_name: Name of the comet
    - actual_positions: Array of [x, y, z] positions for actual orbit
    - guess_positions: Array of [x, y, z] positions for guessed orbit
    - residuals: Array of position differences
    """
    fig = plt.figure(figsize=(12, 8))

    # 3D Orbit Plot
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(actual_positions[:, 0], actual_positions[:, 1], actual_positions[:, 2],
             label='Actual Orbit', color='blue')
    ax1.plot(guess_positions[:, 0], guess_positions[:, 1], guess_positions[:, 2],
             label='Guessed Orbit', color='red', linestyle='--')
    max_val = np.max(np.abs(actual_positions)) * 1.1
    ax1.set_xlim(-max_val, max_val)
    ax1.set_ylim(-max_val, max_val)
    ax1.set_zlim(-max_val, max_val)
    ax1.set_xlabel('X (AU)')
    ax1.set_ylabel('Y (AU)')
    ax1.set_zlabel('Z (AU)')
    ax1.set_title(f"Orbit Comparison for {comet_name}")
    ax1.legend()

    # Residual Plot
    ax2 = fig.add_subplot(122)
    ax2.hist(residuals.flatten(), bins=50, color='gray', alpha=0.7)
    ax2.set_xlabel('Residual (AU)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Residual Distribution')

    plt.tight_layout()
    plt.show()


def animate(cometName):
    df = pd.read_csv("near-earth-comets.csv")

    # Find the comet
    comet_row = df[(df["Object"].str.lower() == cometName.lower()) |
                   (df["Object_name"].str.lower() == cometName.lower())]


    e = float(comet_row["e"].values[0])
    q = float(comet_row["q"].values[0])
    i = float(comet_row["i"].values[0])
    w = float(comet_row["w"].values[0])
    Omega = float(comet_row["Node"].values[0])
    TP = float(comet_row["TP"].values[0])

    # Compute semi-major axis
    a = q / (1 - e)
    num_points = 1000

    # Calculate orbit positions
    positions = Calculations.orbit_positions(e, a, i, w, Omega, TP, num_points)

    # Debug: Check positions
    if np.any(np.isnan(positions)) or np.any(np.isinf(positions)):
        raise ValueError(f"Invalid positions calculated for {cometName}: contains NaN or inf values")
    print("Positions array shape:", positions.shape)
    print("Sample positions:", positions[:5])

    # Animation setup
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    line, = ax.plot([], [], [], lw=2, color='blue', label='Orbit Path')
    point, = ax.plot([], [], [], 'ro', label='Comet')

    # Set axis limits
    max_val = np.max(np.abs(positions)) * 1.1
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_z
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    ax.set_title(f"Orbit of {cometName}")
    ax.legend()

    def init():
        line.set_data([], [])
        line.set_3d_properties([])
        point.set_data([], [])
        point.set_3d_properties([])
        return line, point

    def update(frame):
        line.set_data(positions[:frame, 0], positions[:frame, 1])
        line.set_3d_properties(positions[:frame, 2])
        point.set_data([positions[frame, 0]], [positions[frame, 1]])
        point.set_3d_properties([positions[frame, 2]])
        return line, point

    ani = FuncAnimation(fig, update, frames=len(positions), init_func=init, interval=50, blit=True)

    plt.show()
    return ani