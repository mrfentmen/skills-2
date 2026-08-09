# 8x8 grid, 1px stroke — every pixel justified
# meaning: "text file" reads as a page with lines, not a word processor logo
# test: a person from another culture sees a sheet of paper with writing, not a brand
# restraint pass: dropped the folded corner, the shadow, and the second color
# borrow: gesture borrowed from paper craft: the folded sheet, simplified to a notch

file_icons = {
    "text": [
        "########",
        "#......#",
        "#.####.#",
        "#.####.#",
        "#.####.#",
        "#......#",
        "#......#",
        "########",
    ],
    "image": [
        "########",
        "#......#",
        "#.######",
        "#.#....#",
        "#.#.##.#",
        "#....#.#",
        "#.######",
        "########",
    ],
    "code": [
        "########",
        "#......#",
        "#.##.##.",
        "#.##.##.",
        "#......#",
        "#.##.##.",
        "#.##.##.",
        "########",
    ],
}

# meaning: "image" reads as a picture frame with a mountain, not a camera
# test: a person from another culture sees a framed scene, not a lens
# restraint pass: dropped the sun, the clouds, and the third row of mountains
# borrow: borrowed from landscape painting: the triangle mountain, the frame

# meaning: "code" reads as angle brackets, not a terminal window
# test: a person from another culture sees chevrons, not a keyboard
# restraint pass: dropped the cursor, the prompt, and the border decoration
# borrow: borrowed from typography: the angle bracket pair

for name, rows in file_icons.items():
    print(f"{name}:")
    for row in rows:
        print(row)
    print()