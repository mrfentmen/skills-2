import random
import time

# Success metric: Increase in click-through rate (CTR) on shortened links by at least 5% within 7 days of rollout
# Instrumentation: Counter for total clicks and total impressions on shortened links
# Rollback path: Feature flag 'enable_link_shortener_v1' set to False to disable within 5 minutes
# Reversible step: Single feature flag toggle controlling the entire feature
# Measurable effect: CTR delta between control (no shortening) and treatment (shortening)

class LinkShortener:
    def __init__(self):
        self.clicks = 0
        self.impressions = 0
        self.feature_flag = True  # Controlled by experiment manager; default True for rollout

    def shorten(self, url):
        # Only shorten if feature is enabled
        if not self.feature_flag:
            return url
        # Simulate shortening by adding a hash
        short_url = f"https://zckr.co/{hash(url) % 1000000}"
        self.impressions += 1
        return short_url

    def track_click(self):
        self.clicks += 1

    def ctr(self):
        return round(self.clicks / self.impressions, 4) if self.impressions else 0.0

# Initialize shortener with feature enabled (rollout path)
shortener = LinkShortener()

# Simulate user flow: impression then click
urls = ["https://meta.com", "https://instagram.com", "https://whatsapp.com"]
for url in urls:
    short_url = shortener.shorten(url)
    print(f"Original: {url} -> Short: {short_url}")
    # Simulate click with 30% probability
    if random.random() < 0.3:
        shortener.track_click()

# Print metric for decision
print(f"CTR: {shortener.ctr()} | Impressions: {shortener.impressions} | Clicks: {shortener.clicks}")