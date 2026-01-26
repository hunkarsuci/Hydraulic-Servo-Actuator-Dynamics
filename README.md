# Hydraulic-Servo Actuator Dynamics

A high-fidelity **2nd-order State Space model** implemented in Python, simulating a commercial aircraft hydraulic-servo actuator. This project models the dynamic response of flight control surfaces while accounting for critical physical, non-linear constraints.

## Overview
The behavior of flight control actuators is fundamentally a 2nd-order system. This repository provides a modular implementation to calculate the dynamic response to commanded deflections ($\delta_C$), incorporating three critical physical restrictions:
* **Restriction of Maximum Moments** (Acceleration Saturation).
* **Restriction of Maximum Adjustment Rate** (Velocity Saturation).
* **Restriction of Maximum Deflections** (Position Saturation).



## 📐 Mathematical Model
The model utilizes a linear state-space representation as a baseline:

$$\dot{x}_1 = x_2$$
$$\dot{x}_2 = -\omega_0^2 \cdot x_1 - 2 \cdot \zeta \cdot \omega_0 \cdot x_2 + \omega_0^2 \cdot u$$

**Variables:**
* $x_1$: Actual deflection ($\delta$).
* $x_2$: Adjustment rate ($\dot{\delta}$).
* $u$: Commanded deflection ($\delta_C$).
* $\omega_0 \approx 60 \text{ rad/s}$: Natural frequency.
* $\zeta \approx 0.4 - 0.8$: Damping ratio.

The core dynamics are governed by the 2nd-order ODE:
$$\ddot{y} = -2 \cdot \zeta \cdot \omega_0 \cdot \dot{y} + \omega_0^2(y_c - y)$$

## 🛠️ Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/hunkarsuci/Hydraulic-Servo-Actuator-Dynamics.git](https://github.com/hunkarsuci/Hydraulic-Servo-Actuator-Dynamics.git)
