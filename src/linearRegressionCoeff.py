"""Fit per-channel gain/offset calibration from logged sweep data.

Each record looks like {"<channel>": [v0, reading, reference]}. The fit maps the
sensor reading onto the reference value: reference = gain * reading + offset.

Example:
    python src/linearRegressionCoeff.py --min-r2 0.99
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from common import fit_line, load_json


def collect(records):
    channels = {}
    for rec in records:
        for ch, vals in rec.items():
            d = channels.setdefault(ch, {"reading": [], "reference": []})
            d["reading"].append(vals[1])
            d["reference"].append(vals[2])
    return channels


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", default="Controller20201028_0343_z.json", help="sweep file (default: in data/)")
    p.add_argument("--min-r2", type=float, default=0.99, help="flag fits below this r2 as unreliable")
    p.add_argument("--max-reference", type=float, default=None,
                   help="ignore points above this reference value (e.g. where the sensor saturates)")
    p.add_argument("--no-plot", action="store_true")
    args = p.parse_args()

    channels = collect(load_json(args.input))
    failed = []
    for ch, d in channels.items():
        x, y = np.asarray(d["reading"], float), np.asarray(d["reference"], float)
        if args.max_reference is not None:
            keep = y <= args.max_reference
            x, y = x[keep], y[keep]
        try:
            gain, offset, r2 = fit_line(x, y)
        except ValueError as e:
            print("channel {}: cannot fit ({})".format(ch, e))
            failed.append(ch)
            continue
        ok = r2 >= args.min_r2
        if not ok:
            failed.append(ch)
        print("channel {}: gain {:.6f}, offset {:.3f}, r2 {:.5f}, reading range {:.0f}-{:.0f}{}".format(
            ch, gain, offset, r2, x.min(), x.max(), "" if ok else "  <-- UNRELIABLE"))

        if not args.no_plot:
            fig, ax = plt.subplots()
            ax.scatter(x, y, s=12, label="measured")
            xs = np.linspace(x.min(), x.max(), 2)
            ax.plot(xs, gain * xs + offset, color="C1", label="fit")
            ax.set_title("channel {}  r2={:.4f}{}".format(ch, r2, "" if ok else " (UNRELIABLE)"))
            ax.set_xlabel("sensor reading")
            ax.set_ylabel("reference")
            ax.legend()

    if failed:
        print("\n{} channel(s) failed the r2 >= {} check: {}".format(len(failed), args.min_r2, ", ".join(failed)))
    if not args.no_plot:
        plt.show()


if __name__ == "__main__":
    main()
