"""Fetch independent reference values (JPL Horizons, ERFA, USNO).

Writes positions-horizons.json, earth-orientation-erfa.json and
moon-phases-usno-2024.json into the directory given as argv[1], in the exact
format committed under contracts/reference/. Requires network access and
pyerfa (BSD-3-Clause): `pip install pyerfa`. Compare the output with the
committed files before replacing them (Horizons solutions are occasionally
updated).
"""

import datetime as dt
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import erfa

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

# Epochs in UTC; chosen to span 1950-2049 (inside de440s coverage) and include
# the existing parity-fixture instants.
EPOCHS_UTC = [
    "1950-06-15T12:00:00Z",
    "1985-03-21T06:30:00Z",
    "2000-01-01T12:00:00Z",
    "2024-01-01T12:00:00Z",
    "2024-10-17T18:00:00Z",
    "2049-12-24T03:15:00Z",
]
BODIES = {
    "sun": "10", "moon": "301", "mercury": "199", "venus": "299", "mars": "499",
    "jupiter": "599", "saturn": "699", "uranus": "799", "neptune": "899", "pluto": "999",
    "ceres": "1;", "chiron": "2060;",
    "pallas": "2;", "juno": "3;", "vesta": "4;", "astraea": "5;", "hebe": "6;", "iris": "7;",
    "flora": "8;", "metis": "9;", "hygiea": "10;", "parthenope": "11;", "victoria": "12;",
    "egeria": "13;", "irene": "14;", "eunomia": "15;", "psyche": "16;", "thetis": "17;",
    "melpomene": "18;", "fortuna": "19;", "massalia": "20;",
}
API = "https://ssd.jpl.nasa.gov/api/horizons.api"


def jd_utc(iso):
    t = dt.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")
    d1, d2 = erfa.dtf2d("UTC", t.year, t.month, t.day, t.hour, t.minute, t.second)
    return d1, d2


def horizons(command):
    tlist = " ".join(f"{sum(jd_utc(e)):.9f}" for e in EPOCHS_UTC)
    params = {
        "format": "json", "COMMAND": f"'{command}'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "OBSERVER", "CENTER": "'500@399'", "TLIST": tlist, "TIME_TYPE": "UT",
        "QUANTITIES": "'31'", "ANG_FORMAT": "DEG", "EXTRA_PREC": "YES", "CSV_FORMAT": "YES",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as resp:
        payload = json.load(resp)
    text = payload["result"]
    rows = text.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()
    out = []
    for row in rows:
        cells = [c.strip() for c in row.split(",")]
        nums = [c for c in cells if c and _is_float(c)]
        out.append({"date_ut": cells[0], "lon_deg": float(nums[-2]), "lat_deg": float(nums[-1])})
    source = next((ln.strip() for ln in text.splitlines() if "Target body name" in ln), "")
    ephem = next((ln.strip() for ln in text.splitlines() if ln.strip().startswith("Ephemeris")), "")
    return out, url, source, ephem


def _is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


positions = {}
provenance = {}
for name, command in BODIES.items():
    rows, url, target, ephem = horizons(command)
    assert len(rows) == len(EPOCHS_UTC), (name, rows)
    positions[name] = [{"lon_true_deg": r["lon_deg"], "lat_deg": r["lat_deg"], "horizons_date_ut": r["date_ut"]} for r in rows]
    provenance[name] = {"target": target, "request_url": url}
    time.sleep(0.5)

# ERFA earth orientation at the same instants (UT1 taken = UTC, matching both
# implementations, which have no Delta-UT1 data).
orientation = []
for e in EPOCHS_UTC:
    u1, u2 = jd_utc(e)
    a1, a2 = erfa.utctai(u1, u2)
    t1, t2 = erfa.taitt(a1, a2)
    dpsi, deps = erfa.nut06a(t1, t2)
    eps_mean = erfa.obl06(t1, t2)
    orientation.append({
        "utc": e,
        "jd_utc": u1 + u2,
        "jd_tt": t1 + t2,
        "gmst_deg": float(erfa.gmst06(u1, u2, t1, t2)) * 180 / 3.141592653589793,
        "gast_deg": float(erfa.gst06a(u1, u2, t1, t2)) * 180 / 3.141592653589793,
        "mean_obliquity_deg": float(eps_mean) * 180 / 3.141592653589793,
        "true_obliquity_deg": float(eps_mean + deps) * 180 / 3.141592653589793,
        "nutation_longitude_deg": float(dpsi) * 180 / 3.141592653589793,
    })

today = dt.date.today().isoformat()


def write(name, doc):
    (OUT / name).write_text(json.dumps(doc, indent=2) + "\n")


write("positions-horizons.json", {
    "schema_version": 1,
    "description": "Independent reference positions from JPL Horizons: geocentric apparent ecliptic longitude/latitude of date (observer table quantity 31, CENTER=500@399), referred to the TRUE equinox of date. Subtract earth-orientation-erfa.json nutation_longitude_deg to obtain the mean-equinox longitude used by the Kefer convention.",
    "source": "NASA/JPL Horizons API (https://ssd.jpl.nasa.gov/api/horizons.api); solution DE441 for planets; small bodies per provenance.target",
    "retrieved_at": today,
    "time_scale": "UT input (TIME_TYPE=UT); Kefer implementations take UT1 = UTC",
    "epochs_utc": EPOCHS_UTC, "positions": positions, "provenance": provenance,
})
write("earth-orientation-erfa.json", {
    "schema_version": 1,
    "description": "Earth orientation at the reference epochs computed with ERFA (BSD-3-Clause; IAU SOFA algorithms): IAU 2006 GMST/GAST, IAU 2006 mean obliquity, IAU 2000A nutation. UT1 is taken equal to UTC, matching both implementations; TT from UTC with leap seconds (ERFA flags 1950 and 2049 as 'dubious year').",
    "source": f"pyerfa {erfa.__version__}", "epochs": orientation,
})
with urllib.request.urlopen("https://aa.usno.navy.mil/api/moon/phases/year?year=2024", timeout=60) as resp:
    usno = json.load(resp)
write("moon-phases-usno-2024.json", {
    "schema_version": 1,
    "source": "U.S. Naval Observatory Astronomical Applications API",
    "source_url": "https://aa.usno.navy.mil/api/moon/phases/year?year=2024",
    "retrieved_at": today,
    "time_scale": "UTC, rounded to the minute by the source",
    "phases": [
        {"phase": p["phase"], "utc": f'{p["year"]:04d}-{p["month"]:02d}-{p["day"]:02d}T{p["time"]}:00Z'}
        for p in usno["phasedata"] if p["phase"] in ("New Moon", "Full Moon")
    ],
})
print("ok", {k: len(v) for k, v in positions.items()})
