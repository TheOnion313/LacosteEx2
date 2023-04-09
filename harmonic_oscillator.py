import math

import numpy as np
import pickle as p

M = K = ALPHA = BETA = 1
OMEGA = 1.01

DEFAULT_DT = 0.001
START_DT = 1
END_DT = 1e-5
DDT = -1e-5
SIM_TIME = 18.5

X_0 = 0.01
V_0 = 0


def calc_a(x, v, t):
    return (-2 * K * x + ALPHA * math.sin(OMEGA * (t + BETA * v))) / M


def euler_step(x, v, t, dt=DEFAULT_DT):
    a = calc_a(x, v, t)
    x += v * dt
    t += dt
    v += a * dt

    return x, v, t


def midpoint_step(x, v, t, dt=DEFAULT_DT):
    mid_x = x + v * dt / 2
    a_n1 = calc_a(x, v, t)
    mid_v = v + a_n1 * dt / 2

    a_n05 = calc_a(mid_x, mid_v, t + dt / 2)

    new_x = x + v * dt
    new_v = v + a_n05 * dt
    new_t = t + dt

    return new_x, new_v, new_t


def runge_kute4(x, v, t, dt=DEFAULT_DT):
    mid_x = x + v * dt / 2
    k1 = calc_a(x, v, t) * dt
    k2 = calc_a(mid_x, v + k1 / 2, t + dt / 2) * dt
    k3 = calc_a(mid_x, v + k2 / 2, t + dt / 2) * dt
    k4 = calc_a(x + v * dt, v + k3, t + dt)

    new_x = x + v * dt
    new_v = v + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    new_t = t + dt

    return new_x, new_v, new_t


def sim(dt=DEFAULT_DT):
    t = 0

    x_euler = X_0
    v_euler = V_0

    x_midpoint = X_0
    v_midpoint = V_0

    x_rk4 = X_0
    v_rk4 = V_0

    t_archive = []

    x_archive_euler = []
    v_archive_euler = []

    x_archive_midpoint = []
    v_archive_midpoint = []

    x_archive_rk4 = []
    v_archive_rk4 = []

    while t < 18.5:
        t_archive.append(t)

        x_archive_euler.append(x_euler)
        v_archive_euler.append(v_euler)

        x_archive_midpoint.append(x_midpoint)
        v_archive_midpoint.append(v_midpoint)

        x_archive_rk4.append(x_rk4)
        v_archive_rk4.append(v_rk4)

        x_euler, v_euler, t = euler_step(x_euler, v_euler, t, dt)
        x_midpoint, v_midpoint, t = midpoint_step(x_midpoint, v_midpoint, t, dt)
        x_rk4, v_rk4, t = runge_kute4(x_rk4, v_rk4, t, dt)

    return x_archive_euler, v_archive_euler, t_archive, x_archive_midpoint, v_archive_midpoint, x_archive_rk4, v_archive_rk4


def main():
    x_archive_euler = []
    x_archive_midpoint = []
    x_archive_rk4 = []

    dt_archive = []

    le = int(abs(START_DT - END_DT) // abs(DDT))
    for i, dt in enumerate(np.linspace(START_DT, END_DT, le)):
        print(f"\r{str(i / le * 100)[:5]} %\t\t[{'=' * int(i / le * 20)}{' ' * (20 - int(i / le * 20))}]", end='')
        res = sim(dt)

        x_archive_euler.append(res[0][-1])
        x_archive_midpoint.append(res[3][-1])
        x_archive_rk4.append(res[5][-1])

        dt_archive.append(dt)

    with open("harmonic_os.p", "wb") as f:
        p.dump({"dt": dt_archive, "x_euler": x_archive_euler, "x_midpoint": x_archive_midpoint, "x_rk4": x_archive_rk4}, f)


if __name__ == '__main__':
    main()
