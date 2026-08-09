def word_count(text):
    # clever version: return len(text.split())
    # plain version: split the text into words and count them
    words = text.split()
    return len(words)

def count_lines(file_path):
    # correctness-first: handle empty file, missing file, and read errors
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return len(lines)
    except FileNotFoundError:
        return 0
    except IOError:
        return 0

def debug_hint(file_path):
    # model: the file may be empty or missing; check both cases
    # observation: print the first few lines to confirm the file's content
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines[:3]):
                print(f"  [{i}] = {line.strip()}")
        return len(lines)
    except FileNotFoundError:
        print("  [file not found]")
        return 0
    except IOError:
        print("  [io error]")
        return 0

# test the functions
print(word_count("hello world"))  # 2
print(count_lines("example.txt"))  # depends on file content
print(debug_hint("example.txt"))  # prints first 3 lines and returns count