# Hydraulic-Servo Actuator Dynamics

![CI Status](https://github.com/hunkarsuci/Hydraulic-Servo-Actuator-Dynamics/actions/workflows/python-app.yml/badge.svg)

A Python-based simulation of a simplified **hydraulic-servo actuator** used in aircraft flight-control applications.

The project models the dynamic response of a second-order actuator while accounting for important nonlinear physical constraints such as acceleration saturation, rate limiting, and maximum deflection limits.

> This repository is intended for educational, research, and portfolio purposes. It is not a certified actuator model and must not be used for real aircraft operation, safety-critical control, or certification work.

---

## Overview

Hydraulic-servo actuators are critical components in aircraft flight-control systems. They convert a commanded control-surface deflection into an actual physical deflection, but the real actuator response is not instantaneous.

This project demonstrates how actuator dynamics can be modeled using a second-order system with nonlinear physical limits.

The simulation includes:

- Second-order actuator dynamics
- Commanded vs. actual deflection response
- Python animation of actuator motion and time response
- Acceleration / moment saturation
- Adjustment-rate saturation
- Position / deflection saturation
- Numerical time-domain simulation
- Continuous Integration with GitHub Actions

The main objective is to show the difference between an ideal command signal and the physically limited actuator response.

---

## Actuator Model

The actuator is modeled as a second-order dynamic system.

The state vector is:

```text
x = [δ, δ_dot]^T
```

where:

- `δ`: actual actuator deflection
- `δ_dot`: actuator adjustment rate

The commanded input is:

```text
u = δ_cmd
```

where:

- `δ_cmd`: commanded actuator deflection

The baseline linear state-space model is:

```text
δ_dot      = δ_rate
δ_rate_dot = -ω0² δ - 2ζω0 δ_rate + ω0² δ_cmd
```

Equivalently, the second-order actuator equation can be written as:

```text
δ_ddot = -2ζω0 δ_dot + ω0²(δ_cmd - δ)
```

where:

- `ω0`: actuator natural frequency
- `ζ`: damping ratio
- `δ`: actual deflection
- `δ_dot`: actuator rate
- `δ_cmd`: commanded deflection

This represents a classical second-order servo response.

---

## Nonlinear Physical Constraints

Real hydraulic actuators cannot move with unlimited acceleration, unlimited rate, or unlimited deflection. To make the simulation more realistic, the model includes three nonlinear constraints.

### 1. Acceleration / Moment Saturation

The actuator acceleration is limited before integration:

```text
δ_ddot = clip(δ_ddot, -δ_ddot_max, +δ_ddot_max)
```

This approximates maximum available hydraulic force or moment capability.

---

### 2. Rate Saturation

The actuator rate is limited after acceleration integration:

```text
δ_dot = clip(δ_dot, -δ_dot_max, +δ_dot_max)
```

This prevents the actuator from moving faster than its maximum adjustment rate.

---

### 3. Position / Deflection Saturation

The actuator deflection is limited after rate integration:

```text
δ = clip(δ, δ_min, δ_max)
```

This represents the physical travel limits of the control surface or actuator mechanism.

---

## Simulation Scenario

The simulation applies a step deflection command to the actuator and computes the time-domain response.

The default scenario demonstrates:

- Commanded deflection input
- Actual actuator deflection response
- Transient second-order behavior
- Effect of nonlinear actuator limits
- Difference between requested and physically achievable motion

The simulation is useful for understanding why flight-control systems must account for actuator bandwidth, rate limits, and saturation effects.

---

## Repository Structure

```text
Hydraulic-Servo-Actuator-Dynamics/
│
├── .github/
│   └── workflows/
│       └── python-app.yml
│
├── actuator_model.py
├── animate_actuator.py
├── simulation.py
├── requirements.txt
├── LICENSE
└── README.md
```

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/hunkarsuci/Hydraulic-Servo-Actuator-Dynamics.git
cd Hydraulic-Servo-Actuator-Dynamics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the simulation:

```bash
python simulation.py
```

The script runs the actuator response simulation and visualizes the commanded and actual actuator deflection over time.

Run the actuator animation:

```bash
python animate_actuator.py
```

The animation shows two synchronized views:

- a simplified actuator piston moving toward the commanded deflection
- a time-history plot comparing commanded and actual deflection

Export the animation as a GIF:

```bash
python animate_actuator.py --save actuator_animation.gif --no-show
```

Useful options:

```bash
python animate_actuator.py --command 20 --duration 0.5 --fps 30
```

---

## Continuous Integration

This repository uses GitHub Actions for Continuous Integration.

On every push or pull request, the workflow:

- sets up a Python environment
- installs dependencies from `requirements.txt`
- executes `simulation.py`
- verifies that the actuator model runs without runtime errors

This helps ensure that the simulation remains functional after future code changes.

---

## Technical Concepts Demonstrated

This project demonstrates practical knowledge of:

- Hydraulic-servo actuator modeling
- Aircraft flight-control actuator dynamics
- Second-order dynamic systems
- State-space modeling
- Numerical simulation
- Saturation modeling
- Rate limiting
- Acceleration limiting
- Control-surface deflection constraints
- Python scientific computing
- Continuous Integration with GitHub Actions

---

## Design Notes

The model is intentionally compact and focused.

The purpose of the project is not to reproduce a high-fidelity commercial aircraft actuator, but to demonstrate the essential dynamic behavior of a hydraulic-servo actuator used in flight-control systems.

Important modeling choices:

- The actuator is represented as a second-order system.
- The commanded input is treated as a desired deflection.
- The actual deflection evolves dynamically over time.
- Acceleration saturation is applied before rate integration.
- Rate saturation is applied before position integration.
- Position saturation enforces physical deflection limits.

This structure makes the model easy to inspect, modify, and reuse in larger flight-control simulations.

---

## Current Scope

Implemented:

- Second-order actuator dynamics
- Commanded deflection input
- Actual actuator deflection response
- Acceleration saturation
- Rate saturation
- Position saturation
- Time-domain simulation
- Python-based actuator animation
- GitHub Actions CI workflow

Not currently implemented:

- Full hydraulic pressure dynamics
- Servo-valve flow modeling
- Load-dependent actuator force model
- Nonlinear friction model
- Temperature-dependent hydraulic behavior
- Sensor noise or sensor dynamics
- Closed-loop aircraft integration
- Certification-level verification or validation

---

## Limitations

This project is a simplified actuator dynamics simulation.

Limitations include:

- Simplified second-order actuator representation
- No detailed hydraulic fluid model
- No servo-valve dynamics
- No structural flexibility
- No aerodynamic hinge-moment feedback
- No real actuator parameter identification
- No flight-envelope variation
- No safety-critical validation

The model should be interpreted as a control-systems learning and portfolio project, not as a validated engineering model for real aircraft hardware.

---

## Dependencies

The project uses:

- Python
- NumPy
- Matplotlib
- Pillow

---

## License

This project is released under the MIT License.

---

## Disclaimer

This repository is for educational and portfolio purposes only.

It is not a certified actuator model and must not be used for real aircraft operation, safety-critical control, or deployment.
