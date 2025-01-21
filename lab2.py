# Ex1

number = int(input("Please enter a number: "))
if number % 2 == 0:
    print(f"{number} is even.")
else:
    print(f"{number} is odd.")

# Ex2

grade = int(input("Please enter your grade: "))
if grade >= 90:
    print("A")
elif grade >= 80:
    print("B")
elif grade >= 70:
    print("C")
elif grade >= 60:
    print("D")
else:
    print("F")

# Ex3

player1 = input("Player 1, enter your choice: [1]Rock [2]Paper [3]Scissors ")
player2 = input("Player 2, enter your choice: [1]Rock [2]Paper [3]Scissors ")

if player1 == player2:
    print("It's a tie!")
elif (player1 == '1' and player2 == '3') or (player1 == '2' and player2 =='1') or (player1 == '3' and player2 == '2'):
    print('Player 1 wins!')
else:
    print('Player 2 wins!')

# Ex4

year = int(input("Please enter a year: "))

if year % 100 == 0 and year % 400 == 0:
    print(f"{year} is a leap year.")
elif year % 4 == 0 and year % 100 != 0:
    print(f'{year} is a leap year')
else:
    print(f'{year} is not a leap year.')

# Ex5

password = input("Please enter your password: ")
if len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password):
    print("Your password is strong!")
else:
    print("Your password is weak!")

# Ex6

balance = float(input("Please enter your account balance: "))
withdraw = float(input("Please enter amount to withdraw: "))
if withdraw > balance:
    print("Insufficient balance.")
elif withdraw % 10 != 0:
    print("Withdrawal amount must be a multiple of 10.")
else:
    print("Withdrawal successful.")

# Challenge

x = float(input("Enter the first number: "))
y = float(input("Enter the second number: "))
op = input("Enter the operation: ")
sol = float(input("Enter your solution: "))
match op:
    case '+':
        print(sol == x + y)
    case '-':
        print(sol == x - y)
    case '*':
        print(sol == x * y)
    case '/':
        print(sol == x / y)
    case '//':
        print(sol == x // y)
    case '%':
        print(sol == x % y)
    case '**':
        print(sol == x ** y)
    case _:
        print("Invalid operation.")

