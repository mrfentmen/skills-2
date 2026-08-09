# parts: 2 functions, 0 deps, 1 file
# scarce: screen real estate (80x24) -- design time is cheap, spend it
# moved rendering into terminal: the screen was already there
# extension point: caller can supply their own formatter

def center(text, width=80):
    return text.center(width)

def box(text, width=80):
    line = '+' + '-' * (width - 2) + '+'
    return '\n'.join([line, f'| {text.ljust(width - 3)}|', line])

demo = box(center("Woz's Garage Tool"))
print(demo)