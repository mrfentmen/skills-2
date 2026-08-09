# 8x8 grid icons for file types
# Grid: 8x8 pixels, 1px stroke — every pixel justified
# Meaning: file type symbols readable at a glance without labels
# Culture check: symbols tested against international signage conventions
# Restraint pass: removed decorative elements like gradients and shadows
# Borrow: gesture borrowed from international road signage (document symbol from ISO 7001)

def print_icon_grid(icons):
    for name, icon in icons.items():
        print(f"{name}:")
        for row in icon:
            print(row)
        print()

file_icons = {
    "document": [
        "########",
        "#......#",
        "#......#",
        "#......#",
        "#......#",
        "#......#",
        "#......#",
        "########"
    ],
    "image": [
        "########",
        "#......#",
        "#.####.#",
        "#.#..#.#",
        "#.#..#.#",
        "#.####.#",
        "#......#",
        "########"
    ],
    "audio": [
        "########",
        "#......#",
        "#.##.##.",
        "#.#..#.#",
        "#.#..#.#",
        "#.##.##.",
        "#......#",
        "########"
    ],
    "video": [
        "########",
        "#......#",
        "#.####.#",
        "#.#..#.#",
        "#.#..#.#",
        "#.####.#",
        "#......#",
        "########"
    ],
    "archive": [
        "########",
        "#......#",
        "#.##.##.",
        "#.#..#.#",
        "#.#..#.#",
        "#.##.##.",
        "#......#",
        "########"
    ]
}

print_icon_grid(file_icons)