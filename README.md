# FIR_Coeff_Generated
Python with SciPy to generate FIR filter coefficients and ADC calibration from logged controller data.

## Installation

Requires Python 3.11+ (numpy 2.3).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Layout

| Path | Contents |
|---|---|
| `src/` | scripts (run from any directory) |
| `data/` | logged controller captures (`Controller*_u.json`, `_s.json`, `_z.json`, ...) |
| `coeff/` | generated coefficients, comma-separated for pasting into a C array |

Input file names are looked up in `data/` unless you give a full path.

## Usage

**Design a filter and test it on logged ADC captures**

```bash
python src/fircoeffgen.py --taps 5 --cutoff 0.05 --input Controller20201028_0343_u.json
```

Prints the coefficients and the filter's *actual* -3 dB point (with few taps it can be far above
the requested cutoff), writes `coeff/coeff.json`, then for each `adcN` channel plots raw ADC, the
Python-filtered signal and the firmware's `firN` output, and reports the gain/offset that maps the
filtered signal back onto the raw input. Add `--no-plot` for text output only.

**Plot raw ADC against firmware FIR output**

```bash
python src/adcvsfirplotting.py --input Controller20201028_0343_u.json
```

**Fit per-channel calibration from a sweep**

```bash
python src/linearRegressionCoeff.py --input Controller20201028_0343_z.json --min-r2 0.99
```

Fits `reference = gain * reading + offset` per channel and flags channels whose fit is below
`--min-r2` as unreliable (e.g. a saturated or disconnected sensor). If a sensor saturates at the
top of the sweep, use `--max-reference 2560` (for example) to fit only the linear range.
