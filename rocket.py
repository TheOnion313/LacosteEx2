from matplotlib import pyplot as plt
import numpy as np
import math
from typing import *

# simulation constants
DEFAULT_DT = 0.001
start_pitch = 20  # deg
start_yaw = 180  # deg

pitch_rad = math.radians(start_pitch)  # rad
yaw_rad = math.radians(start_yaw)  # rad
start_vel = 500  # m / s
loc0 = np.array([0, 0, 0])  # m, m, m
vel0 = np.array([math.cos(pitch_rad) * math.cos(yaw_rad), math.cos(pitch_rad) * math.sin(yaw_rad), math.sin(pitch_rad)]) * start_vel

# rocket constants
M = 500  # kg
A = 1  # m ^ 2

# physical constants
g = 9.81  # m / s ^ 2
alpha = 0.05  # kg / m ^ 2

israel_longitude = 31.0461  # deg
omega = 1 / (24 * 3600)  # 1/s
v_omega = omega * np.array([0, math.sin(israel_longitude), math.cos(israel_longitude)])


def euler_step(loc: np.ndarray, vel: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray]:
    new_loc = loc + vel * dt

    gravity = np.array([0, 0, -M * g])
    air_friction = -alpha * A * np.linalg.norm(vel) * vel
    coriolis = -2 * M * np.cross(v_omega, vel)

    force = gravity + air_friction + coriolis
    acc = force / M

    new_vel = vel + acc * dt

    return new_loc, new_vel


def sim(dt=DEFAULT_DT):
    loc = loc0
    vel = vel0

    loc_archive = []

    while loc[-1] >= 0:
        loc, vel = euler_step(loc, vel, dt)
        loc_archive.append(loc)

    figure = plt.figure()
    ax = plt.axes(projection="3d")

    x_vals = [loc[0] for loc in loc_archive]
    y_vals = [loc[1] for loc in loc_archive]
    z_vals = [loc[2] for loc in loc_archive]

    ax.plot3D(x_vals, y_vals, z_vals)

    plt.show()


if __name__ == '__main__':
    sim()
