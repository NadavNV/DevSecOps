# ex1

def divide(numerator: int, denominator: int):
    quotient = numerator // denominator
    remainder = numerator % denominator
    return quotient, remainder


# print(divide(10, 3))  # Output: 3, 1

# ex2

def calculate_area(length: float, width: float):
    return length * width


# print(calculate_area(5, 10))  # Output: 50

# ex3

def sum_all(*args):
    return sum(args)


# print(sum_all(1, 2, 3, 4, 5))  # Output: 15
# print(sum_all())               # Output: 0

# ex4

def format_message(message: str,/,*,uppercase = False):
    if uppercase:
        return message.upper()
    else:
        return message


# print(format_message("hello"))  # Output: "hello"
# print(format_message("hello", uppercase=True))  # Output: "HELLO"

# Challenge 1

def most_frequent(words: list):
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    most_frequent_word = None
    max_count = -float('inf')

    for word, count in word_counts.items():
        if count > max_count:
            most_frequent_word = word
            max_count = count

    return most_frequent_word


# print(most_frequent(["apple", "banana", "apple", "orange", "banana", "apple"]))  # Output: "apple"

# Challenge 2

def first_unique_char(string: str):
    # print(string)
    char_counts = {}
    for char in string:
        if char in char_counts:
            char_counts[char] += 1
        else:
            char_counts[char] = 1
    # print(char_counts)

    indices = [string.index(char) for char in char_counts.keys() if char_counts[char] == 1]
    # print(indices)

    return min(indices) if indices else -1


# print(first_unique_char("leetcode"))  # Output: 0
# print(first_unique_char("loveleetcode"))  # Output: 2
# print(first_unique_char("aabb"))  # Output: -1
