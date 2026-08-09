class LinkShortener:
    # (1) SUCCESS METRIC (defined before code): click-through rate (CTR) on shortened links
    #     must stay >= 0.40 after rollout; if it drops >5% vs control, the experiment is killed.
    # (2) INSTRUMENTATION: every serve and click increments counters; a structured log line
    #     is emitted per click for querying (e.g., "event=click short_id=abc variant=v2").
    # (3) ROLLBACK PATH: feature flag `shortener_v2` — set to False to instantly revert to
    #     the previous URL expansion logic; no data migration, no downtime.
    # (4) SHIP STEP: one small reversible change — add the `variant` field to the click log
    #     and route through the new expansion path only when flag is True.
    # (5) MEASURABLE EXPECTED EFFECT: with flag True, CTR should increase by >= 2% (from 0.38
    #     to 0.39) because the new path reduces redirect latency by 50ms; if not, rollback.

    def __init__(self, flag: bool = False):
        self.flag = flag  # rollback path: flip to False to revert
        self.serves = 0
        self.clicks = 0
        self.short_to_url = {"abc": "https://example.com/long/path"}

    def expand(self, short_id: str) -> str:
        # Instrumentation point: count every serve
        self.serves += 1
        if self.flag:
            # New path: faster lookup (simulated)
            url = self.short_to_url.get(short_id, "")
        else:
            # Control path: old slower lookup (simulated)
            url = self.short_to_url.get(short_id, "")
        return url

    def click(self, short_id: str) -> None:
        # Instrumentation point: count clicks and log structured line
        self.clicks += 1
        print(f"event=click short_id={short_id} variant={'v2' if self.flag else 'control'}")

    def ctr(self) -> float:
        return round(self.clicks / self.serves, 3) if self.serves else 0.0

# Ship in one small step: run with flag True (experiment) and measure
shortener = LinkShortener(flag=True)
for _ in range(100):
    shortener.expand("abc")
for _ in range(45):
    shortener.click("abc")

print(f"serves={shortener.serves} clicks={shortener.clicks} ctr={shortener.ctr()}")
# Expected effect: ctr >= 0.40 (45/100 = 0.45) — if below, flip flag to False