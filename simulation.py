import numpy as np
import matplotlib.pyplot as plt
from actuator_model import HydraulicActuator # Import your class

def run_simulation():
    # Initialize the Actuator with parameters from the study
    # omega_0 approx 60 rad/s, zeta approx 0.4 - 0.8
    actuator = HydraulicActuator(omega_0=60.0, zeta=0.6)
    
    # Setup Time Array: 0.5 seconds simulation with 1ms steps
    time = np.arange(0, 0.5, 0.001)
    
    # Input: Step command of 20 degrees (delta_c)
    command_value = 20.0 
    output = []

    # Run the time-stepping loop
    for t in time:
        output.append(actuator.step(command_value))

    # --- Visualization ---
    plt.figure(figsize=(10, 6))
    
    # Plot Command Line
    plt.plot(time, [command_value]*len(time), '--r', label=r'Command ($\delta_C$)')
    
    # Plot Actual Response
    plt.plot(time, output, label=r'Actual Deflection ($\delta$)')
    
    # Formatting the Plot
    plt.title('Hydraulic-Servo Actuator Response with Non-linear Saturation')
    plt.xlabel('Time (s)')
    plt.ylabel('Deflection (deg)')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend(loc='lower right')
    
    # Final check of the results
    plt.show()

if __name__ == "__main__":
    run_simulation()