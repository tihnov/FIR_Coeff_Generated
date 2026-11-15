"""Plot raw ADC against the firmware FIR output, one figure per channel.

Example:
    python src/adcvsfirplotting.py --input Controller20201028_0343_s.json
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from common import group_captures, load_json


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", default="Controller20201028_0343_u.json", help="capture file (default: in data/)")
    args = p.parse_args()

    channels = group_captures(load_json(args.input))
    fig, axes = plt.subplots(len(channels), 1, figsize=(11, 2.5 * len(channels)), sharex=True, squeeze=False)
    for ax, (ch, captures) in zip(axes[:, 0], channels.items()):
        pos = 0
        for i, cap in enumerate(captures):
            x = np.arange(pos, pos + len(cap["adc"]))
            ax.plot(x, cap["adc"], color="C0", lw=0.8, label="adc{}".format(ch) if i == 0 else None)
            if cap["fir"] is not None:
                ax.plot(x, cap["fir"], color="C2", label="fir{}".format(ch) if i == 0 else None)
            pos += len(cap["adc"])
            ax.axvline(pos, color="grey", lw=0.5)
        ax.legend(loc="upper right")
    axes[-1, 0].set_xlabel("sample (vertical lines = capture boundaries)")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
