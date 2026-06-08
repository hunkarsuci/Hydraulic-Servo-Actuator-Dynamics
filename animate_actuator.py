import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle
import numpy as np

from actuator_model import HydraulicActuator


def simulate_response(command_value, duration, dt):
    actuator = HydraulicActuator(omega_0=60.0, zeta=0.6, dt=dt)
    time = np.arange(0.0, duration, dt)
    deflection = np.zeros_like(time)
    rate = np.zeros_like(time)

    for index, _ in enumerate(time):
        deflection[index] = actuator.step(command_value)
        rate[index] = actuator.x[1]

    return time, deflection, rate, actuator.max_deflection


def build_animation(time, deflection, rate, command_value, max_deflection, fps):
    fig, (ax_mech, ax_plot) = plt.subplots(
        1,
        2,
        figsize=(12, 5),
        gridspec_kw={"width_ratios": [1.0, 1.4]},
    )
    fig.suptitle("Hydraulic-Servo Actuator Dynamic Response")

    ax_mech.set_title("Actuator Motion")
    ax_mech.set_xlim(-max_deflection - 10, max_deflection + 10)
    ax_mech.set_ylim(-1.8, 1.8)
    ax_mech.set_xlabel("Deflection (deg)")
    ax_mech.set_yticks([])
    ax_mech.grid(True, axis="x", linestyle="--", alpha=0.35)

    cylinder = Rectangle(
        (-max_deflection, -0.35),
        max_deflection * 2,
        0.7,
        facecolor="#d7dee8",
        edgecolor="#4d5b6a",
        linewidth=1.5,
    )
    piston = Rectangle(
        (-0.6, -0.55),
        1.2,
        1.1,
        facecolor="#2f6f73",
        edgecolor="#17383a",
    )
    rod, = ax_mech.plot([], [], color="#1f2933", linewidth=5, solid_capstyle="round")
    surface, = ax_mech.plot([], [], color="#c44e52", linewidth=4, solid_capstyle="round")
    actual_marker, = ax_mech.plot([], [], "o", color="#2f6f73", markersize=8)
    command_marker, = ax_mech.plot(
        [command_value],
        [1.15],
        marker="v",
        color="#c44e52",
        markersize=9,
        linestyle="None",
        label="Command",
    )
    state_text = ax_mech.text(
        0.02,
        0.95,
        "",
        transform=ax_mech.transAxes,
        va="top",
        fontsize=10,
    )

    ax_mech.add_patch(cylinder)
    ax_mech.add_patch(piston)
    ax_mech.legend(loc="lower right")

    ax_plot.set_title("Command vs Actual Deflection")
    ax_plot.set_xlim(time[0], time[-1])
    ax_plot.set_ylim(
        min(-2.0, deflection.min() - 2.0),
        max(command_value, deflection.max()) + 3.0,
    )
    ax_plot.set_xlabel("Time (s)")
    ax_plot.set_ylabel("Deflection (deg)")
    ax_plot.grid(True, linestyle="--", alpha=0.35)
    ax_plot.plot(time, np.full_like(time, command_value), "--", color="#c44e52", label="Command")
    response_line, = ax_plot.plot([], [], color="#2f6f73", linewidth=2.5, label="Actual")
    current_point, = ax_plot.plot([], [], "o", color="#2f6f73", markersize=6)
    ax_plot.legend(loc="lower right")

    frame_step = max(1, int(round(1.0 / (fps * (time[1] - time[0])))))
    frames = range(0, len(time), frame_step)

    def update(frame):
        x = deflection[frame]
        piston.set_x(x - 0.6)
        rod.set_data([x, max_deflection + 7], [0.0, 0.0])
        surface.set_data([max_deflection + 7, max_deflection + 7], [-0.9, 0.9])
        actual_marker.set_data([x], [0.0])
        response_line.set_data(time[: frame + 1], deflection[: frame + 1])
        current_point.set_data([time[frame]], [deflection[frame]])
        state_text.set_text(
            f"t = {time[frame]:.3f} s\n"
            f"deflection = {deflection[frame]:.2f} deg\n"
            f"rate = {rate[frame]:.2f} deg/s"
        )
        return (
            piston,
            rod,
            surface,
            actual_marker,
            command_marker,
            response_line,
            current_point,
            state_text,
        )

    animation = FuncAnimation(fig, update, frames=frames, interval=1000 / fps, blit=False)
    fig.tight_layout()
    return fig, animation


def parse_args():
    parser = argparse.ArgumentParser(description="Animate the hydraulic-servo actuator response.")
    parser.add_argument("--command", type=float, default=20.0, help="Step command in degrees.")
    parser.add_argument("--duration", type=float, default=0.5, help="Simulation duration in seconds.")
    parser.add_argument("--dt", type=float, default=0.001, help="Simulation time step in seconds.")
    parser.add_argument("--fps", type=int, default=30, help="Animation frames per second.")
    parser.add_argument("--save", type=Path, help="Optional output path, for example actuator_animation.gif.")
    parser.add_argument("--no-show", action="store_true", help="Do not open an interactive Matplotlib window.")
    return parser.parse_args()


def main():
    args = parse_args()
    time, deflection, rate, max_deflection = simulate_response(args.command, args.duration, args.dt)
    fig, animation = build_animation(time, deflection, rate, args.command, max_deflection, args.fps)

    if args.save:
        args.save.parent.mkdir(parents=True, exist_ok=True)
        animation.save(args.save, writer=PillowWriter(fps=args.fps))
        print(f"Saved animation to {args.save}")

    if not args.no_show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    main()
