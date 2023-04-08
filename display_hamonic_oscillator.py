from matplotlib import pyplot as plt
import pickle as p
import numpy as np
from math import log


def main():
    with open("harmonic_os.p", "rb") as f:
        archive = p.load(f)
        dt_archive, x_archive_euler = np.array(archive["dt"]), np.array(archive["x_euler"])
        x_archive_midpoint = np.array(archive["x_midpoint"])
        x_archive_rk4 = np.array(archive["x_rk4"])

    dt_log = [log(d) for d in dt_archive]
    euler_log = [log(d) for d in x_archive_euler]
    midpoint_log = [log(d) for d in x_archive_midpoint]
    rk4_log = [log(abs(d)) if d != 0 else -1000 for d in x_archive_rk4]

    graph, (plot1, plot2) = plt.subplots(1, 2)
    plot1.plot(dt_archive, x_archive_euler)
    plot1.plot(dt_archive, x_archive_midpoint)
    plot1.plot(dt_archive, x_archive_rk4)
    plot1.legend(["euler", "midpoint", "rk4"])

    plot1.invert_xaxis()

    plot2.plot(dt_log, euler_log)
    plot2.plot(dt_log, midpoint_log)
    plot2.plot(dt_log, rk4_log)
    plot2.legend(["euler_log", "midpoint_log", "rk4_log"])

    plot2.invert_xaxis()

    plt.show()


if __name__ == '__main__':
    main()
