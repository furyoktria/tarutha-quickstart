# Tarutha quickstart

Three short examples and a Claude setup for the [Tarutha API](https://tarutha.co):
Indonesian capital-market data with the source and period beside every number.
Prices, exchange filings, depository ownership, government bonds, mutual funds and
news, in one REST API and an MCP server for AI agents.

This repo holds code only and ships no market data. Every example asks the API
when you run it. Python 3.8 or newer, standard library only.

## 1. How current is the data? (no key needed)

```bash
git clone https://github.com/furyoktria/tarutha-quickstart
cd tarutha-quickstart
python3 examples/01_status.py
```

```
Source          Dataset                                 Newest      Lag         Verdict
IDX             IDX daily summary                       2026-09-23  1 weekday   current
KSEI            Instrument ownership                    2026-08     1 month     current
DJPPR           SBN ownership                           2026-08     1 month     current
...
```

Every source and dataset, with its newest record and how far behind it is.

## 2. Who holds a stock, and how that changed

```bash
export TARUTHA_API_KEY=tarutha_...
python3 examples/02_who_holds.py BBCA
```

The script finds the stock's ISIN, then reads KSEI's month-end depository records.
It prints the latest month's holdings across nine investor types (retail,
corporates, mutual funds, pension funds, banks and more), local against foreign,
and the last six months of change in the foreign share. Months where a split or a
new issuance moved the numbers are labeled, so they are not read as buying or
selling. The same routes cover every instrument class KSEI settles, bonds and
sukuk included, not only stocks.

## 3. Prices, with the metadata every response carries

```bash
python3 examples/03_prices.py TLKM
```

The last 30 trading days: close, range and a small trend line, followed by the
response's `source`, generation time and `request_id`.

## Ask Claude

Tarutha also has an MCP server, so Claude can call these routes itself. It has
nine tools, from price history to a one-call company snapshot. Members receive it
as a package, `tarutha-mcp-server-<version>.tgz`. Install it once:

```bash
npm install -g ./tarutha-mcp-server-<version>.tgz
```

Claude Code:

```bash
claude mcp add tarutha \
  --env TARUTHA_API_BASE=https://api.tarutha.co \
  --env TARUTHA_API_KEY=tarutha_YOUR_KEY \
  -- tarutha-mcp
```

Claude Desktop, in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tarutha": {
      "command": "tarutha-mcp",
      "env": {
        "TARUTHA_API_BASE": "https://api.tarutha.co",
        "TARUTHA_API_KEY": "tarutha_YOUR_KEY"
      }
    }
  }
}
```

Then ask, for example:

- "Give me a company snapshot of TLKM."
- "Which investor types hold BBCA, and did foreign holders add or cut last month?"
- "Which IDX stocks got unusual market activity flags this week?"

## Get a key

Keys come with a Tarutha founding membership; [tarutha.co/#pricing](https://tarutha.co/#pricing)
explains how to join. Members sign in to the Terminal at app.tarutha.co and create
keys from the account menu. Keys start with `tarutha_`. Keep them on a server and
out of git.

## Good to know

- Send your own `User-Agent` header. Some default ones, such as Python's urllib,
  are refused at Tarutha's network edge. [`examples/tarutha.py`](examples/tarutha.py)
  does this for you.
- A member's keys share 300 requests a minute. Above that the API answers `429`
  with `RATE_LIMITED` and a `Retry-After` header; the helper waits and retries once.
- Only `/v1/status` and the OpenAPI document answer without a key.
- Full reference: [tarutha.co/docs](https://tarutha.co/docs). OpenAPI document:
  [api.tarutha.co/v1/openapi.json](https://api.tarutha.co/v1/openapi.json).
- Use of the data is covered by the [Tarutha terms](https://tarutha.co/terms).
  Tarutha is independent and not affiliated with IDX, KSEI, OJK or DJPPR.

## License

The code in this repo is MIT. Tarutha is built by
[Teman Bisnis Digital](https://temanbizz.digital).
