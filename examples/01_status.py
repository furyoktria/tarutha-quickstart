"""How current is each data source? This route needs no key.

    python3 examples/01_status.py
"""
from tarutha import get

status = get("/v1/status", key_required=False)["data"]
print(f"Tarutha data status at {status['as_of']}: {status['verdict']}\n")
rows = []
for source in status["sources"]:
    for ds in source["datasets"]:
        lag, unit = ds.get("lag"), ds.get("unit") or ""
        lag_text = "-" if lag is None else f"{lag} {unit}{'' if lag == 1 else 's'}"
        rows.append((source["label"], ds["label"], (ds.get("newest") or "-")[:10], lag_text, ds.get("verdict", "-")))

w1 = max(len(r[0]) for r in rows) + 2
w2 = max(len(r[1]) for r in rows) + 2
print(f"{'Source':<{w1}}{'Dataset':<{w2}}{'Newest':<12}{'Lag':<12}Verdict")
for src, name, newest, lag_text, verdict in rows:
    print(f"{src:<{w1}}{name:<{w2}}{newest:<12}{lag_text:<12}{verdict}")
