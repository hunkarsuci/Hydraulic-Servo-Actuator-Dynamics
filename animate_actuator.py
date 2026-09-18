import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon
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


def build_animation(time, deflection, rate, command_value, max_deflection, fps, playback_speed):
    # Keep the palette and hierarchy consistent across the mechanical view and
    # the response plot.  The previous version mixed a floating rectangle,
    # detached markers, and unlabeled geometry, which made the animation hard
    # to read at a glance.
    navy = "#102a43"
    ink = "#243b53"
    muted = "#627d98"
    grid = "#d9e2ec"
    cyan = "#2f9aa0"
    cyan_dark = "#176b70"
    red = "#e05252"
    blue_fluid = "#9bd5df"
    coral_fluid = "#f3b1a9"
    background = "#f7fafc"

    fig = plt.figure(figsize=(13, 6.8), facecolor=background)
    layout = fig.add_gridspec(
        2,
        2,
        height_ratios=[1.15, 1.0],
        width_ratios=[1.0, 1.55],
        hspace=0.32,
        wspace=0.24,
    )
    ax_mech = fig.add_subplot(layout[0, 0])
    ax_plot = fig.add_subplot(layout[0, 1])
    ax_status = fig.add_subplot(layout[1, :])

    fig.suptitle(
        "Hydraulic Servo Actuator | Dynamic Response",
        x=0.06,
        y=0.98,
        ha="left",
        fontsize=16,
        fontweight="bold",
        color=navy,
    )

    for axis in (ax_mech, ax_plot, ax_status):
        axis.set_facecolor(background)
        for spine in axis.spines.values():
            spine.set_color(grid)

    # Mechanical cutaway: the command and actual values share the same ruler,
    # while the moving piston and the two fluid chambers explain the motion.
    ax_mech.set_title("Actuator cutaway", loc="left", color=navy, fontweight="bold", pad=10)
    ax_mech.set_xlim(-max_deflection - 11, max_deflection + 17)
    ax_mech.set_ylim(-1.55, 1.45)
    ax_mech.set_yticks([])
    ax_mech.set_xticks([])
    ax_mech.grid(False)

    barrel_left = -max_deflection
    barrel_right = max_deflection
    barrel_bottom = -0.52
    barrel_height = 1.04
    barrel = FancyBboxPatch(
        (barrel_left, barrel_bottom),
        barrel_right - barrel_left,
        barrel_height,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        facecolor="#e8eef5",
        edgecolor=muted,
        linewidth=1.6,
        zorder=2,
    )
    ax_mech.add_patch(barrel)

    piston = Rectangle(
        (-0.9, -0.73),
        1.8,
        1.46,
        facecolor=cyan,
        edgecolor=cyan_dark,
        linewidth=1.5,
        zorder=5,
    )
    left_fluid = Rectangle(
        (barrel_left + 0.18, barrel_bottom + 0.16),
        1.0,
        barrel_height - 0.32,
        facecolor=blue_fluid,
        edgecolor="none",
        alpha=0.9,
        zorder=3,
    )
    right_fluid = Rectangle(
        (0.0, barrel_bottom + 0.16),
        1.0,
        barrel_height - 0.32,
        facecolor=coral_fluid,
        edgecolor="none",
        alpha=0.9,
        zorder=3,
    )
    ax_mech.add_patch(left_fluid)
    ax_mech.add_patch(right_fluid)
    ax_mech.add_patch(piston)

    rod, = ax_mech.plot([], [], color=ink, linewidth=7, solid_capstyle="round", zorder=4)
    rod_end = barrel_right + 8.5
    load = FancyBboxPatch(
        (rod_end - 1.0, -0.42),
        2.0,
        0.84,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor="#f0b429",
        edgecolor="#9c6b0c",
        linewidth=1.2,
        zorder=4,
    )
    ax_mech.add_patch(load)
    load_label = ax_mech.text(rod_end, 0, "LOAD", ha="center", va="center", fontsize=8, fontweight="bold", color=navy, zorder=6)

    ax_mech.text(barrel_left + 0.5, 0.73, "A", color=cyan_dark, fontsize=9, fontweight="bold")
    ax_mech.text(barrel_right - 0.5, 0.73, "B", color="#b33f3f", fontsize=9, fontweight="bold", ha="right")
    ax_mech.text(0, -1.08, "linearized output position", ha="center", color=muted, fontsize=8)
    state_text = ax_mech.text(0.02, 0.96, "", transform=ax_mech.transAxes, va="top", fontsize=9, color=ink)

    ruler_y = -1.31
    ax_mech.plot([barrel_left, barrel_right], [ruler_y, ruler_y], color=muted, linewidth=1)
    for tick in np.linspace(-max_deflection, max_deflection, 5):
        ax_mech.plot([tick, tick], [ruler_y - 0.06, ruler_y + 0.06], color=muted, linewidth=1)
        ax_mech.text(tick, ruler_y - 0.14, f"{tick:.0f}°", ha="center", va="top", fontsize=7, color=muted)
    actual_marker, = ax_mech.plot([], [], "o", color=cyan_dark, markersize=8, zorder=8, label="Actual")
    command_marker, = ax_mech.plot([], [], marker="v", color=red, markersize=9, linestyle="None", zorder=8, label="Command")
    ax_mech.legend(loc="upper right", frameon=False, fontsize=8, ncol=2)

    # Response plot: keep the full command line visible and draw a subtle error
    # band so the tracking behavior is understandable while it evolves.
    ax_plot.set_title("Command tracking", loc="left", color=navy, fontweight="bold", pad=10)
    ax_plot.set_xlim(time[0], time[-1])
    plot_min = min(-2.0, deflection.min() - 2.0, command_value - 2.0)
    plot_max = max(2.0, deflection.max() + 2.0, command_value + 2.0)
    ax_plot.set_ylim(plot_min, plot_max)
    ax_plot.set_xlabel("Time (s)", color=muted)
    ax_plot.set_ylabel("Deflection (deg)", color=muted)
    ax_plot.tick_params(colors=muted)
    ax_plot.grid(True, linestyle="--", linewidth=0.7, color=grid)
    ax_plot.axhline(0, color=grid, linewidth=0.8)
    ax_plot.plot(time, np.full_like(time, command_value), linestyle="--", color=red, linewidth=1.8, label="Command")
    error_band = None
    response_line, = ax_plot.plot([], [], color=cyan_dark, linewidth=2.6, label="Actual")
    current_point, = ax_plot.plot([], [], "o", color=cyan_dark, markersize=7, zorder=5)
    time_marker = ax_plot.axvline(time[0], color=muted, linewidth=1, alpha=0.55)
    ax_plot.legend(loc="lower right", frameon=False, fontsize=8)

    # Status panel replaces the old empty-looking second plot area with a
    # compact progress view: position, rate, and normalized tracking error.
    ax_status.set_title("Live state", loc="left", color=navy, fontweight="bold", pad=8)
    ax_status.set_xlim(-max_deflection, max_deflection)
    ax_status.set_ylim(-0.35, 1.0)
    ax_status.set_yticks([])
    ax_status.set_xlabel("Deflection range (deg)", color=muted)
    ax_status.tick_params(axis="x", colors=muted)
    ax_status.grid(False)
    ax_status.plot([-max_deflection, max_deflection], [0.25, 0.25], color=grid, linewidth=12, solid_capstyle="round")
    status_actual, = ax_status.plot([], [], "o", color=cyan_dark, markersize=12, label="Actual")
    status_command, = ax_status.plot([], [], marker="v", color=red, markersize=11, linestyle="None", label="Command")
    status_text = ax_status.text(0.01, 0.86, "", transform=ax_status.transAxes, color=ink, fontsize=10, va="top")
    ax_status.legend(loc="upper right", frameon=False, fontsize=8, ncol=2)

    frame_step = max(1, int(round(playback_speed / (fps * (time[1] - time[0])))))
    frames = range(0, len(time), frame_step)

    def update(frame):
        nonlocal error_band
        x = deflection[frame]
        piston.set_x(x - 0.9)
        left_fluid.set_x(barrel_left + 0.18)
        left_fluid.set_width(max(0.12, x - barrel_left - 0.9))
        right_fluid.set_x(x + 0.9)
        right_fluid.set_width(max(0.12, barrel_right - x - 0.9))
        rod.set_data([x + 0.9, rod_end], [0.0, 0.0])
        actual_marker.set_data([x], [ruler_y])
        command_marker.set_data([command_value], [ruler_y + 0.2])
        response_line.set_data(time[: frame + 1], deflection[: frame + 1])
        current_point.set_data([time[frame]], [deflection[frame]])
        time_marker.set_xdata([time[frame], time[frame]])
        if error_band is not None:
            error_band.remove()
        error_band = ax_plot.fill_between(
            time[: frame + 1],
            np.full(frame + 1, command_value),
            deflection[: frame + 1],
            color=red,
            alpha=0.08,
        )
        status_actual.set_data([x], [0.25])
        status_command.set_data([command_value], [0.25])
        state_text.set_text(
            f"t = {time[frame]:.3f} s\n"
            f"actual = {deflection[frame]:.2f}°\n"
            f"rate = {rate[frame]:.1f}°/s"
        )
        status_text.set_text(
            f"Command  {command_value:>6.2f}°     "
            f"Actual  {deflection[frame]:>6.2f}°     "
            f"Error  {command_value - deflection[frame]:>6.2f}°"
        )
        return (
            piston,
            left_fluid,
            right_fluid,
            rod,
            actual_marker,
            command_marker,
            response_line,
            current_point,
            error_band,
            state_text,
            time_marker,
            status_actual,
            status_command,
            status_text,
        )

    animation = FuncAnimation(fig, update, frames=frames, interval=1000 / fps, blit=False)
    fig.subplots_adjust(left=0.055, right=0.985, top=0.90, bottom=0.10)
    return fig, animation


def parse_args():
    parser = argparse.ArgumentParser(description="Animate the hydraulic-servo actuator response.")
    parser.add_argument("--command", type=float, default=20.0, help="Step command in degrees.")
    parser.add_argument("--duration", type=float, default=0.5, help="Simulation duration in seconds.")
    parser.add_argument("--dt", type=float, default=0.001, help="Simulation time step in seconds.")
    parser.add_argument("--fps", type=int, default=30, help="Animation frames per second.")
    parser.add_argument(
        "--playback-speed",
        type=float,
        default=1.0,
        help="Playback speed multiplier. Use 0.25 for quarter-speed slow motion.",
    )
    parser.add_argument("--save", type=Path, help="Optional output path, for example actuator_animation.gif.")
    parser.add_argument("--no-show", action="store_true", help="Do not open an interactive Matplotlib window.")
    return parser.parse_args()


def main():
    args = parse_args()
    time, deflection, rate, max_deflection = simulate_response(args.command, args.duration, args.dt)
    fig, animation = build_animation(
        time,
        deflection,
        rate,
        args.command,
        max_deflection,
        args.fps,
        args.playback_speed,
    )

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
