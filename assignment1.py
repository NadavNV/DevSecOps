# Ex1

n = int(input("Please enter a number: "))
divisors = [1]
for i in range(2, int(n ** 0.5) + 1):
    # We start from 2 because we already included 1, which is always a divisor.
    # It's enough to check up to sqrt(number) because divisors come in pairs:
    # If a is a divisor of n, then (n / a) is also a divisor.
    if n % i == 0:
        divisors.append(i)
        if i * i != n:
            # This check is necessary, otherwise for square numbers we'd count their root twice.
            divisors.append(n // i)
divisors.sort()
print(divisors)

# Ex2

count = 0
running_sum = 0
while True:
    number = float(input(f"Please enter number #{count + 1}" +
                         (f' (avg={running_sum / count}. Sum={running_sum}): ' if count != 0 else ': ')))
    running_sum += number
    count += 1
    if number < 0:
        print("Thank you. Goodbye.")
        break

# Ex3 with challenge

words = []
while True:
    word = input("Please enter a word: ")
    words.append(word.lower())
    # if word.lower() in words:
    if words.count(word.lower()) > 2:
        print(f"You entered the word '{word.lower()}' three times. Goodbye...")
        break

# Ex4 with challenge

# To avoid breaking the DRY principle I would put the code that generates
# the list in a function, but we haven't learned functions yet.
l1 = input("Please enter a list of numbers, separated by spaces: ")
l2 = input("Please enter a list of numbers, separated by spaces: ")
l1 = [float(x) for x in l1.split()]
l2 = [float(x) for x in l2.split()]
l1_score = 0
l2_score = 0
for i in range(min(len(l1), len(l2))):
    if l1[i] > l2[i]:
        l1_score += 1
    elif l1[i] < l2[i]:
        l2_score += 1
if l1_score > l2_score:
    print("The first list is greater than the second list.")
elif l2_score > l1_score:
    print("The second list is greater than the first list.")
else:
    print("It's a tie.")

