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


def calculate_acceleration(loc: np.ndarray, vel: np.ndarray) -> float:
    gravity = np.array([0, 0, -M * g])
    air_friction = -alpha * A * np.linalg.norm(vel) * vel
    # coriolis = -2 * M * np.cross(v_omega, vel)

    force = gravity + air_friction  # + coriolis
    acc = force / M

    return acc


def euler_step(loc: np.ndarray, vel: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray]:
    new_loc = loc + vel * dt

    acc = calculate_acceleration(loc, vel)
    new_vel = vel + acc * dt

    return new_loc, new_vel


def rk4(loc: np.ndarray, vel: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray]:
    acc_n1 = calculate_acceleration(loc, vel)
    k1 = dt * acc_n1
    acc_n05 = calculate_acceleration(loc + vel * dt / 2, vel + k1 / 2)
    k2 = dt * acc_n05
    acc_n05 = calculate_acceleration(loc + vel * dt / 2, vel + k2 / 2)
    k3 = dt * acc_n05
    k4 = dt * calculate_acceleration(loc + vel * dt, vel + k3)

    return loc + vel * dt, vel + (k1 + 2 * k2 + 2 * k3 + k4) / 6


def sim(dt=DEFAULT_DT):
    loc = loc0
    vel = vel0
    t = 0

    loc_archive = [loc]
    t_archive = [t]

    while loc[-1] >= 0:
        loc, vel = rk4(loc, vel, dt)
        t += dt
        loc_archive.append(loc)
        t_archive.append(t)

    # linearly interpolate hit location
    point_0 = loc_archive[-2]
    point_1 = loc_archive[-1]
    t0 = t_archive[-2]
    t1 = t_archive[-1]
    m_x = (point_1[0] - point_0[0]) / dt
    m_y = (point_1[1] - point_0[1]) / dt
    m_z = (point_1[2] - point_0[2]) / dt
    t_hit = t0 + abs(point_0[2] / m_z)

    hit_point = point_0 + np.array([m_x, m_y, m_z]) * (t_hit - t0)
    print(loc_archive[-1])
    loc_archive[-1] = hit_point
    print(hit_point, end="\n\n")
    return loc_archive


def display_route(loc_archive, figure):
    x_vals = [loc[0] for loc in loc_archive]
    y_vals = [loc[1] for loc in loc_archive]
    z_vals = [loc[2] for loc in loc_archive]

    figure.plot3D(x_vals, y_vals, z_vals)


if __name__ == '__main__':
    fig = plt.figure()
    ax = plt.axes()
    leg = []

    hits = []

    for dt in np.linspace(3, 1e-2, 20):
        # leg.append(f"dt = {dt}")
        archive = sim(dt)
        # print(archive)
        # display_route(archive, ax)
        hits.append(archive[-1][:2])

    plt.scatter([hit[0] for hit in hits], [hit[1] for hit in hits], s=1)
    fig.legend(leg)
    plt.show()
