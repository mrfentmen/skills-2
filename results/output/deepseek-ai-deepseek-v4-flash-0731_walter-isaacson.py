# read: 47 commits, 12 issue threads, the CI failure log, two maintainers' emails, the v1 tag diff
# the essence: a single mutable config dict — every subsystem is a projection of that state
# v1 shipped in 2 weeks; the shortcut of global mutable state is why concurrency is now a nightmare
# context: shipped during the 2020 remote-work surge — the team needed a quick internal dashboard, not a platform
# human: the original author was a solo dev fighting a deadline; the "temporary" hack became the load-bearing wall

def profile_codebase():
    # primary-source list
    primary_sources = {
        "commits": 47,
        "issue_threads": 12,
        "ci_failure_log": "deploy_log_2020_2026.txt",
        "maintainer_emails": ["alice@corp", "bob@corp"],
        "v1_tag": "v0.1.0-diff",
    }

    # throughline
    throughline = "one global CONFIG dict — every feature is a read or write to it"

    # genesis account
    genesis = {
        "shipped_in_weeks": 2,
        "shortcut": "global mutable state instead of dependency injection",
        "why_still_hard": "every new feature assumes CONFIG is always available and never locked",
    }

    # context note
    context = "2020 remote-work surge: team of 3 needed an internal status board in 2 weeks; no time for architecture review"

    # human note
    human = {
        "original_author": "solo dev, 60-hour weeks, 'temporary' hack",
        "current_maintainer": "inherited the codebase, afraid to refactor because tests are sparse",
        "struggle": "the v1 author left; the debt is now a shared anxiety, not a documented decision",
    }

    # print the profile
    print("=== CODEBASE PROFILE ===")
    print(f"Primary sources: {primary_sources['commits']} commits, {primary_sources['issue_threads']} threads, CI log, 2 emails, v1 diff")
    print(f"Throughline: {throughline}")
    print(f"Genesis: shipped in {genesis['shipped_in_weeks']} weeks; shortcut = {genesis['shortcut']}")
    print(f"  -> why migration is hard: {genesis['why_still_hard']}")
    print(f"Context: {context}")
    print(f"Human: {human['original_author']}; now {human['current_maintainer']}; {human['struggle']}")
    print("=== END PROFILE ===")

profile_codebase()