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
    x += v * dt
    t += dt
    a = calc_a(x, v, t)
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


def sim(dt=DEFAULT_DT):
    t = 0
    x = X_0
    v = V_0

    x_archive = []
    v_archive = []
    t_archive = []

    while t < 18.5:
        x_archive.append(x)
        v_archive.append(v)
        t_archive.append(t)

        x, v, t = euler_step(x, v, t, dt)

    return x_archive, v_archive, t_archive


def main():
    x_archive = []
    dt_archive = []
    le = int(abs(START_DT - END_DT) // abs(DDT))
    for i, dt in enumerate(np.linspace(START_DT, END_DT, le)):
        print(f"\r{str(i / le * 100)[:5]} %\t[{'=' * int(i / le * 20)}{' ' * (20 - int(i / le * 20))}]", end='')
        res = sim(dt)
        x_archive.append(res[0][-1])
        dt_archive.append(dt)

    with open("harmonic_os.p", "wb") as f:
        p.dump({"dt": dt_archive, "x": x_archive}, f)


if __name__ == '__main__':
    main()
