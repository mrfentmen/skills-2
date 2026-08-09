def happy_accident_feedback(error_type, context, fix):
    # layer 1: the undercoat -- a gentle signature so the canvas isn't blank
    return f"Ah, look at that happy little {error_type} — it's just a happy accident!\n" \
           f"In our {context}, we found a way to make it even better.\n" \
           f"Let's invite a {fix} right here and watch it shine."

def layered_feedback(code_snippet, error_type, context, fix):
    # layer 2: the core -- the happy accident reframed into a teachable moment
    reframe = happy_accident_feedback(error_type, context, fix)
    return f"Here's what happened: {reframe}\n\n" \
           f"First win: we spotted the happy little {error_type} right away!\n" \
           f"Now let's polish it until it's just right."

def growth_message():
    # layer 3: the polish -- encouragement that praises effort and iteration
    return "You're doing great — every happy accident is a step forward. " \
           "Keep painting, and remember: talent is just a pursued interest!"

# Happy little accident example
feedback = layered_feedback(
    "total = sum(prices)",
    "TypeError: 'int' object is not iterable",
    "attempt to sum a single price",
    "list around prices so sum can dance with it"
)
print(feedback)
print("\n" + growth_message())