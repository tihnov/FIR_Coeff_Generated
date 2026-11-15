"""Design FIR low-pass coefficients, run them over logged ADC data, and compare
with the firmware's filtered output.

Example:
    python src/fircoeffgen.py --taps 5 --cutoff 0.05
"""
import argparse
from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

from common import COEFF_DIR, fit_line, group_captures, load_json


class FIR:
    """Direct-form FIR filter processing one sample at a time.

    Products are summed in floating point and rounded once at the end, which
    avoids the per-tap truncation bias of int(x*c) accumulation.
    """

    def __init__(self, coeff):
        if len(coeff) == 0:
            raise ValueError("FIR needs at least one coefficient")
        self.coeff = np.asarray(coeff, dtype=float)
        self.history = deque([0.0] * len(self.coeff), maxlen=len(self.coeff))

    def calculate(self, sample):
        self.history.appendleft(float(sample))  # history[0] = newest sample
        return int(round(float(np.dot(self.coeff, self.history))))


def design(taps, cutoff, window):
    coeff = signal.firwin(taps, cutoff=cutoff, pass_zero=True, window=window)
    w, h = signal.freqz(coeff, worN=8192)
    below = np.abs(h) < 10 ** (-3 / 20)
    actual = w[np.argmax(below)] / np.pi if below.any() else 1.0
    print("coeff ({} taps): {}".format(taps, np.round(coeff, 6)))
    print("requested cutoff {:.3f} x Nyquist, actual -3 dB point {:.3f} x Nyquist".format(cutoff, actual))
    if actual > 1.5 * cutoff:
        print("  WARNING: too few taps to reach the requested cutoff; increase --taps")
    return coeff


def write_coeff(coeff, path):
    # Comma-separated so it can be pasted straight into a C array initialiser.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join("{:.6f},".format(c) for c in coeff))
    print("wrote {}".format(path))


def filter_capture(coeff, samples):
    fir = FIR(coeff)
    return [fir.calculate(s) for s in samples]


def analyse_channel(ch, captures, coeff, plot):
    skip = len(coeff) - 1  # startup transient, dropped from every capture
    raw_all, filt_all = [], []
    for cap in captures:
        filtered = filter_capture(coeff, cap["adc"])
        cap["filtered"] = filtered
        raw_all.extend(cap["adc"][skip:])
        filt_all.extend(filtered[skip:])

    gain, offset, r2 = fit_line(filt_all, raw_all)
    print("adc{}: {} captures, gain {:.6f}, offset {:.3f}, r2 {:.5f}".format(
        ch, len(captures), gain, offset, r2))

    if plot:
        fig, ax = plt.subplots(figsize=(11, 4))
        pos = 0
        for i, cap in enumerate(captures):
            x = np.arange(pos, pos + len(cap["adc"]))
            first = i == 0
            ax.plot(x, cap["adc"], color="C0", lw=0.8, label="adc (raw)" if first else None)
            ax.plot(x, cap["filtered"], color="C1", label="python FIR" if first else None)
            if cap["fir"] is not None:
                ax.plot(x, cap["fir"], color="C2", ls="--", label="firmware fir" if first else None)
            pos += len(cap["adc"])
            ax.axvline(pos, color="grey", lw=0.5)
        ax.set_title("adc{}  (gain {:.4f}, offset {:.2f})".format(ch, gain, offset))
        ax.set_xlabel("sample (vertical lines = capture boundaries)")
        ax.legend()
        fig.tight_layout()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", default="Controller20201028_0343_u.json", help="capture file (default: in data/)")
    p.add_argument("--taps", type=int, default=5)
    p.add_argument("--cutoff", type=float, default=0.05, help="cutoff as a fraction of Nyquist")
    p.add_argument("--window", default="hamming")
    p.add_argument("--out", default=str(COEFF_DIR / "coeff.json"))
    p.add_argument("--no-plot", action="store_true")
    args = p.parse_args()

    coeff = design(args.taps, args.cutoff, args.window)
    write_coeff(coeff, Path(args.out))

    channels = group_captures(load_json(args.input))
    for ch, captures in channels.items():
        analyse_channel(ch, captures, coeff, plot=not args.no_plot)
    if not args.no_plot:
        plt.show()


if __name__ == "__main__":
    main()
