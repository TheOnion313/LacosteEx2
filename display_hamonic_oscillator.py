from matplotlib import pyplot as plt
import pickle as p


def main():
    with open("harmonic_os.p", "rb") as f:
        archive = p.load(f)
        dt_archive, x_archive = archive["dt"], archive["x"]

    plot = plt.subplot()
    plot.plot(dt_archive, x_archive)
    plot.invert_xaxis()

    plt.show()


if __name__ == '__main__':
    main()
