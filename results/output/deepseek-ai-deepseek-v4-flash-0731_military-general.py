def campaign_plan():
    # OBJECTIVE: Ship the tiny "dark mode toggle" feature to production by 17:00 today.
    # TERRAIN: Monolithic Flask app, single deploy pipeline, no test suite, prod DB shared with staging.
    #         Constraints: 4 hours left, no code review, must not break existing auth flow.
    # FORCES: 1 senior dev (me), Python 3.9, Flask, Jinja2, existing CSS variables, CI/CD via Jenkins.
    # ENEMY: (1) CSS specificity clash with legacy inline styles causing toggle to not apply.
    #        (2) Jinja2 template caching serving stale HTML after deploy, making toggle invisible.
    # PLAN: Phase 1 - Add toggle button and JS to flip a `data-theme` attribute on <body>.
    #       Phase 2 - Wire CSS variables to `data-theme` and purge inline styles from base template.
    #       Phase 3 - Deploy, hard-clear cache, smoke test auth.
    # RESERVE: If CSS clash persists, fallback to a server-side session flag that forces dark mode
    #          via a separate stylesheet link, bypassing JS entirely.

    # phase 1: recon the template and inject the toggle control
    base_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            :root { --bg: white; --text: black; }
            [data-theme="dark"] { --bg: #1a1a1a; --text: #f0f0f0; }
            body { background: var(--bg); color: var(--text); }
        </style>
    </head>
    <body>
        <button id="theme-toggle">Dark Mode</button>
        <script>
            const btn = document.getElementById('theme-toggle');
            btn.onclick = () => {
                const body = document.body;
                body.dataset.theme = body.dataset.theme === 'dark' ? 'light' : 'dark';
            };
        </script>
    </body>
    </html>
    """

    # phase 2: simulate the deploy and cache clear
    def deploy_and_clear_cache(html):
        # in reality: push to server, run `rm -rf /tmp/jinja_cache`
        return html.replace("stale", "fresh")

    # phase 3: smoke test auth flow (simulated)
    def smoke_test_auth():
        return "auth ok" if "login" in base_template else "auth broken"

    # reserve: server-side fallback if JS fails
    def reserve_fallback():
        return "<link rel='stylesheet' href='/static/dark.css'>"

    plan = {
        "objective": "ship dark mode toggle by 17:00",
        "terrain": "flask app, no tests, shared DB, 4h deadline",
        "forces": "1 dev, python 3.9, flask, jenkins",
        "enemy": ["css specificity clash", "jinja cache staleness"],
        "plan": ["phase 1: add toggle", "phase 2: css variables", "phase 3: deploy & smoke test"],
        "reserve": "server-side session flag + separate stylesheet"
    }

    print("=== CAMPAIGN PLAN ===")
    for key, value in plan.items():
        print(f"{key}: {value}")

    print("\n=== DEMO ===")
    print("Rendered template (excerpt):")
    print(base_template[:200])
    print("\nDeploy result:", deploy_and_clear_cache("stale html"))
    print("Smoke test:", smoke_test_auth())
    print("Reserve engaged:", reserve_fallback())

campaign_plan()