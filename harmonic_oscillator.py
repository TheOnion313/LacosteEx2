import math

import numpy as np
import pickle as p

M = K = ALPHA = BETA = 1
OMEGA = 1.01

DEFAULT_DT = 0.001
START_DT = 3
END_DT = 1e-3
DDT = -1e-3
SIM_TIME = 18.5

X_0 = 1
V_0 = 0


def calc_a(r, t):
    return (-2 * K * r[0] + ALPHA * math.sin(OMEGA * (t + BETA * r[1]))) / M


def f(r, t):
    return np.array([r[1], calc_a(r, t)])


def euler_step(r, t, dt=DEFAULT_DT):
    ddt = f(r, t)

    return r + dt * ddt


def midpoint_step(r, t, dt=DEFAULT_DT):
    r_half = r + dt / 2 * f(r, t)
    return r + dt * f(r_half, t + dt / 2)


def runge_kute4(r, t, dt=DEFAULT_DT):
    k1 = dt * f(r, t)
    k2 = dt * f(r + k1 / 2, t + dt / 2)
    k3 = dt * f(r + k2 / 2, t + dt / 2)
    k4 = dt * f(r + k3, t + dt)

    return r + (k1 + 2 * k2 + 2 * k3 + k4) / 6


def sim(dt=DEFAULT_DT):
    t = 0

    r_euler = np.array([X_0, V_0])
    r_midpoint = np.array([X_0, V_0])
    r_rk4 = np.array([X_0, V_0])

    t_archive = []

    r_archive_euler = []
    r_archive_midpoint = []
    r_archive_rk4 = []

    while t < 18.5:
        t_archive.append(t)

        r_archive_euler.append(r_euler)
        r_archive_midpoint.append(r_midpoint)
        r_archive_rk4.append(r_rk4)

        r_euler = euler_step(r_euler, t, dt)
        r_midpoint = midpoint_step(r_midpoint, t, dt)
        r_rk4 = runge_kute4(r_rk4, t, dt)
        t += dt

    return r_archive_euler, r_archive_midpoint, r_archive_rk4, t_archive


def main():
    x_archive_euler = []
    x_archive_midpoint = []
    x_archive_rk4 = []

    dt_archive = []

    le = int(abs(START_DT - END_DT) // abs(DDT))
    for i, dt in enumerate(np.linspace(START_DT, END_DT, le)):
        print(f"\r{str(i / le * 100)[:5]} %\t\t[{'=' * int(i / le * 20)}{' ' * (20 - int(i / le * 20))}]", end='')
        res = sim(dt)

        x_archive_euler.append(res[0][-1][0])
        x_archive_midpoint.append(res[1][-1][0])
        x_archive_rk4.append(res[2][-1][0])

        dt_archive.append(dt)
    print(f"\r{str(le / le * 100)[:5]} %\t\t[{'=' * int(le / le * 20)}{' ' * (20 - int(le / le * 20))}]", end='')

    with open("harmonic_os.p", "wb") as f:
        p.dump({"dt": dt_archive, "x_euler": x_archive_euler, "x_midpoint": x_archive_midpoint, "x_rk4": x_archive_rk4}, f)


if __name__ == '__main__':
    main()
