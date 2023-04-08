from matplotlib import pyplot as plt
import pickle as p


def main():
    with open("harmonic_os.p", "rb") as f:
        archive = p.load(f)
        dt_archive, x_archive_euler = archive["dt"], archive["x_euler"]
        x_archive_midpoint = archive["x_midpoint"]
        x_archive_rk4 = archive["x_rk4"]

    plot = plt.subplot()
    plot.plot(dt_archive, x_archive_euler)
    plot.plot(dt_archive, x_archive_midpoint)
    plot.plot(dt_archive, x_archive_rk4)
    plot.legend(["euler", "midpoint", "rk4"])
    plot.invert_xaxis()

    plt.show()


if __name__ == '__main__':
    main()
