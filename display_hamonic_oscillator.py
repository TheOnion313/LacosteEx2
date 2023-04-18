import math

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

    final_euler = x_archive_euler[-1]
    final_midpoint = x_archive_midpoint[-1]
    final_rk4 = x_archive_rk4[-1]

    graph, (plot1, plot2) = plt.subplots(1, 2)
    plot1.plot(dt_archive, abs(x_archive_euler - final_euler))#, s=1)
    plot1.plot(dt_archive, abs(x_archive_midpoint - final_midpoint))#, s=1)
    plot1.plot(dt_archive, abs(x_archive_rk4 - final_rk4))#, s=1)
    plot1.legend(["euler", "midpoint", "rk4"])

    plot1.invert_xaxis()

    plot2.plot(dt_archive, abs(x_archive_euler - final_euler))#, s=1)
    plot2.plot(dt_archive, abs(x_archive_midpoint - final_midpoint))#, s=1)
    plot2.plot(dt_archive, abs(x_archive_rk4 - final_rk4))#, s=1)

    plt.yscale("log")
    plt.xscale("log")
    plot2.legend(["euler_log", "midpoint_log", "rk4_log"])

    plot2.invert_xaxis()

    plt.show()


if __name__ == '__main__':
    main()
