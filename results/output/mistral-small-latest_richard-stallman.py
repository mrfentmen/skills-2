# freedom 0 (run): the program runs locally under the user's command
# freedom 1 (study): source in the repo, builds from one command — kept
# freedom 2 (share): redistributable under GPL-3.0-or-later — kept
# freedom 3 (modify & share): modified versions must keep the four freedoms — kept
# free_software: True
# free_as_in: liberty

# preferred form: the .py file, not a minified blob
# who controls this program? the user's machine, not our server
# GPL-3.0-or-later: downstream forks must keep the four freedoms
# rejected: the "phone-home" license check — it makes the program control the user

def reverse_text(text):
    return text[::-1]

if __name__ == "__main__":
    input_text = "Hello, world!"
    print(reverse_text(input_text))