import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit configuration
st.title("Rocket Launch Simulation")
st.write("Simulate the launch of a rocket under Earth's gravity with varying thrust, drag, and mass.")

# Constants
g = 9.81  # Gravity (m/s^2)
Cd = 0.47  # Drag coefficient
A = 10.0  # Cross-sectional area (m^2)
rho0 = 1.225  # Sea level air density (kg/m^3)
h_scale = 15000  # Scale height for atmosphere (m)

# Function to calculate air density based on altitude
def air_density(h):
    return rho0 * np.exp(-h / h_scale)

# Function to calculate drag force
def drag_force(v, h):
    return 0.5 * air_density(h) * v**2 * Cd * A

# Inputs in Streamlit
initial_mass = st.number_input("Initial Mass of Rocket (kg)", min_value=50000, max_value=3000000, value=800000)
initial_thrust = st.number_input("Initial Thrust (N)", min_value=1e6, max_value=5e7, value=3.5e7)
burn_rate = st.number_input("Fuel Burn Rate (kg/s)", min_value=500, max_value=25000, value=14000)
dt = st.slider("Time Step (s)", min_value=0.001, max_value=0.1, value=0.01)
plot_interval = st.slider("Plot Interval (s)", min_value=0.1, max_value=1.0, value=0.5)

# Initial conditions
m = initial_mass  # Initial mass of the rocket (kg)
T = initial_thrust  # Initial thrust (N)
v = 0  # Initial velocity (m/s)
h = 0  # Initial height (m)
time = 0  # Initial time (s)

# Lists to store results for plotting
velocities = []
heights = []
times = []

# Run Simulation
while h >= 0 and m > 50000:  # Stop when height drops or fuel is nearly gone
    Fg = m * g  # Gravity force
    Fd = drag_force(v, h)  # Drag force
    a = (T - Fg - Fd) / m  # Acceleration
    
    # Update velocity and height
    v += a * dt
    h += v * dt
    
    # Update mass due to fuel consumption
    m -= burn_rate * dt
    time += dt
    
    # Store results at intervals
    if time % plot_interval < dt:
        velocities.append(v)
        heights.append(h)
        times.append(time)
    
    # Stage separation logic
    if m <= 150000 and m > 100000:
        T = 2.0e6  # New thrust for stage 2
        burn_rate = 1500  # New burn rate for stage 2

# Plotting results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Velocity vs Time
ax1.plot(times, velocities)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Velocity (m/s)')
ax1.set_title('Velocity vs Time')

# Height vs Time
ax2.plot(times, heights)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Height (m)')
ax2.set_title('Height vs Time')

# Display plots in Streamlit
st.pyplot(fig)
