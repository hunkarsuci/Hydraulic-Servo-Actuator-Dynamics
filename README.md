# Hydraulic Servo Actuator Dynamics

High-fidelity **2nd-order state-space actuator model** implemented in Python, simulating a **commercial aircraft hydraulic-servo actuator**.  
The model captures the dynamic response of flight control surfaces while enforcing **critical physical and non-linear constraints** commonly encountered in real aircraft actuators.

---

## 🚀 Overview

Flight control actuators in transport and military aircraft are fundamentally **second-order dynamical systems** driven by hydraulic power and servo valves.

This repository provides a **modular and physics-based simulation** of a hydraulic servo actuator responding to commanded surface deflections \( \delta_C \), while enforcing three essential physical limitations:

- **Maximum Moment Limitation**  
  (Acceleration saturation)

- **Maximum Adjustment Rate Limitation**  
  (Velocity saturation)

- **Maximum Deflection Limitation**  
  (Position saturation)

The implementation is suitable for:
- Flight control system simulation
- Actuator modeling for GNC design
- Control law validation
- Educational and research use

---

## 📐 Mathematical Model

The actuator dynamics are modeled using a **linear state-space representation** as a baseline.

### State Variables
- \( x_1 = \delta \): Actual control surface deflection  
- \( x_2 = \dot{\delta} \): Adjustment rate  
- \( u = \delta_C \): Commanded deflection  

### State-Space Equations

\[
\dot{x}_1 = x_2
\]

\[
\dot{x}_2 = -\omega_0^2 x_1 - 2 \zeta \omega_0 x_2 + \omega_0^2 u
\]

Where:
- \( \omega_0 \approx 60 \, \text{rad/s} \) is the natural frequency  
- \( \zeta \approx 0.4 \text{–} 0.8 \) is the damping ratio  

---

### Equivalent 2nd-Order ODE Form

\[
\ddot{y} = -2 \zeta \omega_0 \dot{y} + \omega_0^2 (y_c - y)
\]

This form clearly highlights the **error-driven actuator behavior** commonly used in flight-control modeling.

---

## ⚙️ Non-Linear Physical Constraints

To reflect real hydraulic actuator behavior, the model enforces:

1. **Acceleration Saturation**  
   Limits actuator force / hydraulic moment capability

2. **Velocity Saturation**  
   Models finite hydraulic flow and servo-valve limits

3. **Position Saturation**  
   Enforces mechanical deflection bounds of the control surface

These constraints are applied through **explicit clipping logic** layered on top of the linear dynamics.

---

## 🛠️ Installation & Usage

### Clone the Repository
```bash
git clone https://github.com/hunkarsuci/Hydraulic-Servo-Actuator-Dynamics.git
cd Hydraulic-Servo-Actuator-Dynamics
pip install -r requirements.txt
python simulation.py
