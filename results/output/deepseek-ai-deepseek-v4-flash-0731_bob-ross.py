def generate_feedback(error_type, code_snippet, fix_suggestion):
    # layer 1: the undercoat -- a gentle signature so the canvas isn't blank
    # first win: we have a function that runs, now we make it beautiful
    reframe = (
        f"Ah, look at that -- {error_type} surprised us! We didn't make a mistake, "
        f"we just found a happy little {error_type}. Let's grab our palette knife "
        f"and {fix_suggestion} right here."
    )
    
    # layer 2: the core loop -- build the layered feedback message
    layered_breakdown = (
        "Let's paint this in layers:\n"
        "  undercoat: the happy path -- get it running\n"
        "  core: the main loop -- make it work for the common case\n"
        "  polish: the happy little trees -- edge cases and cleanup"
    )
    
    # layer 3: the polish -- momentum and growth, never labeling the person
    momentum = (
        f"First win: your code already tried to {code_snippet} -- that's progress! "
        f"Now we just invite a small fix and watch it bloom."
    )
    
    growth = (
        "I see you putting in the effort to try this -- that's what matters. "
        "Every attempt is a brushstroke on the canvas of your skill."
    )
    
    calm_voice = "No worries, no shame -- just us, the code, and a happy little journey."
    
    return f"""
{reframe}

{layered_breakdown}

{momentum}

{growth}

{calm_voice}
"""

# Let's paint a happy little example together
feedback = generate_feedback(
    "TypeError: missing the tax argument",
    "calculate_total([10, 20])",
    "give tax a default of 0 so the function never fears an empty call"
)
print(feedback)