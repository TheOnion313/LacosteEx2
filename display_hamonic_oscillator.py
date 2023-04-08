from matplotlib import pyplot as plt
import pickle as p


def main():
    with open("harmonic_os.p", "rb") as f:
        archive = p.load(f)
        dt_archive, x_archive_euler = archive["dt"], archive["x_euler"]
        x_archive_midpoint = archive["x_midpoint"]

    plot = plt.subplot()
    plot.plot(dt_archive, x_archive_euler)
    plot.plot(dt_archive, x_archive_midpoint)
    plot.legend(["euler", "midpoint"])
    plot.invert_xaxis()

    plt.show()


if __name__ == '__main__':
    main()
