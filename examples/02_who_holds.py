"""Who holds a stock, by investor type, and how the foreign share moved month by month.

Reads KSEI's month-end depository records through Tarutha.

    python3 examples/02_who_holds.py BBCA
"""
import sys
from datetime import date

from tarutha import get

TYPES = {
    "id": "Individuals (retail)", "cp": "Corporates", "mf": "Mutual funds",
    "pf": "Pension funds", "is": "Insurance", "ib": "Banks and financial inst.",
    "sc": "Securities companies", "fd": "Foundations", "ot": "Other",
}

ticker = (sys.argv[1] if len(sys.argv) > 1 else "BBCA").upper()
today = date.today()
since = f"{today.year - 1}-{today.month:02d}"  # the last twelve months

# 1. Everything in this route family is keyed on ISIN, so find it from the ticker.
rows = get("/v1/instruments", q=ticker, limit=50)["data"]
match = next((r for r in rows if r.get("code") == ticker and r.get("isin")), None)
if match is None:
    sys.exit(f"No instrument with code {ticker}.")
isin = match["isin"]

# 2. Who holds it, month by month.
ownership = get(f"/v1/instruments/{isin}/ownership", **{"from": since})["data"]
if not ownership:
    sys.exit(f"No ownership rows for {ticker} since {since}.")
latest = max(ownership, key=lambda r: r["period"])
held = latest["local"]["total"] + latest["foreign"]["total"]

print(f"{ticker} ({isin}), {latest['period']}")
if latest.get("custody_pct") is not None:
    print(f"{latest['custody_pct']:.1f}% of the issued amount sits in KSEI custody; "
          "the shares below are of custody.")
print(f"\n{'Investor type':<28}{'Local':>8}{'Foreign':>10}")
for code, label in sorted(TYPES.items(), key=lambda kv: -(latest["local"][kv[0]] + latest["foreign"][kv[0]])):
    local = 100 * latest["local"][code] / held if held else 0
    foreign = 100 * latest["foreign"][code] / held if held else 0
    print(f"{label:<28}{local:>7.1f}%{foreign:>9.1f}%")
print(f"{'Total':<28}{100 * latest['local']['total'] / held:>7.1f}%"
      f"{100 * latest['foreign']['total'] / held:>9.1f}%")

# 3. How the foreign share moved.
flows = get(f"/v1/instruments/{isin}/flows", **{"from": since})["data"]
print("\nForeign share of custody, change per month")
for f in sorted(flows, key=lambda r: r["period"])[-6:]:
    pp = f.get("foreign_pct_change_pp")
    move = "   n/a" if pp is None else f"{pp:+6.2f} pp"
    note = "" if f.get("is_position_signal") else f"  ({f.get('signal')}: not a position change)"
    print(f"  {f['period']}  {move}{note}")
print("\nMonth-end snapshots: this is net change in holdings, not trading volume.")
