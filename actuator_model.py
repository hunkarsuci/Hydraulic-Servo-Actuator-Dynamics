import numpy as np

class HydraulicActuator:
    """
    A 2nd-order State Space model of a hydraulic-servo actuator.
    Includes non-linear constraints: Moment, Rate, and Deflection saturation.
    """
    def __init__(self, omega_0=60.0, zeta=0.6, dt=0.001):
        # --- System Parameters from Dynamics of Actuators Slides ---
        self.omega_0 = omega_0  # Natural Frequency (rad/s)
        self.zeta = zeta        # Damping Ratio (typically 0.4 - 0.8)
        self.dt = dt            # Simulation time step (s)

        # --- State Variables ---
        # self.x[0] = Deflection (delta)
        # self.x[1] = Adjustment Rate (delta_dot)
        self.x = np.array([0.0, 0.0])

        # --- Saturation Limits (Non-linear constraints) ---
        self.max_moment = 20000.0   # Restriction of max acceleration (ddot)
        self.max_rate = 150.0       # Restriction of max adjustment rate (dot)
        self.max_deflection = 25.0  # Restriction of max deflection (delta)

    def step(self, delta_command):
        """
        Computes one time step of the actuator dynamics using Euler integration.
        """
        # 1. Error Signal: Difference between command and actual deflection
        error = delta_command - self.x[0]

        # 2. Acceleration Calculation (Second-Order ODE logic)
        # Formula: ddot = omega_0^2 * error - 2 * zeta * omega_0 * dot
        ddot = (self.omega_0**2) * error - (2 * self.zeta * self.omega_0 * self.x[1])

        # 3. Apply Moment Saturation (Restriction of max Moments)
        ddot = np.clip(ddot, -self.max_moment, self.max_moment)

        # 4. Integrate Acceleration -> Rate (dot)
        self.x[1] += ddot * self.dt

        # 5. Apply Rate Saturation (Restriction of Adjustment Rate)
        self.x[1] = np.clip(self.x[1], -self.max_rate, self.max_rate)

        # 6. Integrate Rate -> Position (delta)
        self.x[0] += self.x[1] * self.dt

        # 7. Apply Position Saturation (Restriction of max Deflection)
        self.x[0] = np.clip(self.x[0], -self.max_deflection, self.max_deflection)

        return self.x[0]