"""Daily prices for one ticker, with the metadata every Tarutha response carries.

    python3 examples/03_prices.py TLKM
"""
import sys
from datetime import date, timedelta

from tarutha import get

ticker = (sys.argv[1] if len(sys.argv) > 1 else "TLKM").upper()
res = get(f"/v1/equities/{ticker}/prices", **{"from": (date.today() - timedelta(days=45)).isoformat()})
bars = res["data"][-30:]
if not bars:
    sys.exit(f"No price bars for {ticker}.")

closes = [b["close"] for b in bars]
first, last = closes[0], closes[-1]
low, high = min(b["low"] for b in bars), max(b["high"] for b in bars)
blocks = "▁▂▃▄▅▆▇█"
spark = "".join(blocks[int((c - min(closes)) / ((max(closes) - min(closes)) or 1) * 7)] for c in closes)

print(f"{ticker}, last {len(bars)} trading days ({bars[0]['date']} to {bars[-1]['date']})")
print(f"  close  IDR {last:,.0f}  ({(last - first) / first:+.1%} over the window)")
print(f"  range  IDR {low:,.0f} to {high:,.0f}")
print(f"  trend  {spark}")
meta = res["meta"]
print(f"\nsource {meta['source']} · generated {meta['ts']} · request {meta['request_id']}")
