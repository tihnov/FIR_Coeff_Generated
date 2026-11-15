"""Shared helpers: project paths, data loading and line fitting."""
import json
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
COEFF_DIR = ROOT / "coeff"


def load_json(path):
    """Load a JSON file; relative paths are resolved against data/."""
    path = Path(path)
    if not path.is_absolute() and not path.exists():
        path = DATA_DIR / path
    with open(path, "r") as f:
        return json.load(f)


def group_captures(records):
    """Turn a list of capture dicts ({"adc0": [...], "fir0": [...]}, ...) into
    {channel: [{"adc": [...], "fir": [...] or None}, ...]}, one entry per capture."""
    channels = {}
    for rec in records:
        for key, adc in rec.items():
            m = re.fullmatch(r"adc(\d+)", key)
            if not m:
                continue
            ch = int(m.group(1))
            channels.setdefault(ch, []).append(
                {"adc": list(adc), "fir": rec.get("fir{}".format(ch))}
            )
    return dict(sorted(channels.items()))


def fit_line(x, y):
    """Least-squares fit y = gain*x + offset. Returns (gain, offset, r2)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size < 2 or np.ptp(x) == 0:
        raise ValueError("need at least two distinct x values to fit a line")
    gain, offset = np.polyfit(x, y, deg=1)
    residual = y - (gain * x + offset)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1.0 - np.sum(residual ** 2) / ss_tot if ss_tot > 0 else 0.0
    return gain, offset, r2
