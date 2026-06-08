import numpy as np

from actuator_model import HydraulicActuator


def test_actuator_moves_toward_positive_command():
    actuator = HydraulicActuator(omega_0=60.0, zeta=0.6, dt=0.001)

    command = 20.0

    initial_position = actuator.x[0]

    for _ in range(50):
        actuator.step(command)

    final_position = actuator.x[0]

    assert final_position > initial_position


def test_actuator_respects_max_deflection():
    actuator = HydraulicActuator(omega_0=60.0, zeta=0.6, dt=0.001)

    command = 1000.0

    for _ in range(5000):
        actuator.step(command)

    assert actuator.x[0] <= actuator.max_deflection
    assert actuator.x[0] >= -actuator.max_deflection


def test_actuator_respects_max_rate():
    actuator = HydraulicActuator(omega_0=60.0, zeta=0.6, dt=0.001)

    command = 1000.0

    for _ in range(100):
        actuator.step(command)

    assert actuator.x[1] <= actuator.max_rate
    assert actuator.x[1] >= -actuator.max_rate


def test_actuator_state_remains_finite():
    actuator = HydraulicActuator(omega_0=60.0, zeta=0.6, dt=0.001)

    command = 20.0

    for _ in range(1000):
        actuator.step(command)

    assert np.isfinite(actuator.x[0])
    assert np.isfinite(actuator.x[1])