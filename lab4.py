# Ex1: Book Library
import time


class Book:
    def __init__(self, title: str, author: str, pages: int, is_borrowed=False):
        self.title = title
        self.author = author
        self.pages = pages
        self.is_borrowed = is_borrowed

    def borrow_book(self) -> None:
        self.is_borrowed = True

    def return_book(self) -> None:
        self.is_borrowed = False

    def __str__(self) -> str:
        return (f"Title: {self.title}\nAuthor: {self.author}\nPages: {self.pages}\n"
                f"Currently {'' if self.is_borrowed else "not "}on loan\n")


# book1 = Book("Harry Potter", "J.K. Rowling", 500)
# book2 = Book("The Lord of the Rings", "J. R. R. Tolkien", 700)
# book3 = Book("The Bible", "God", 800)
#
# book1.borrow_book()
# print(book1)
# book2.borrow_book()
# print(book2)
# book1.return_book()
# print(book1)
# print(book3)

# Ex2: Bank Account

class BankAccount:
    def __init__(self, holder: str, balance: float):
        self.account_holder = holder
        self.balance = balance
        self.account_number = time.time()

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient balance")

    def display_balance(self) -> None:
        print(f'Current balance: {self.balance}')


# acc1 = BankAccount('Nadav', 1000.56)
# acc2 = BankAccount('Nir', 2000.78)
#
# acc1.display_balance()
# acc2.display_balance()
# acc1.deposit(500)
# acc1.display_balance()
# acc2.withdraw(30000)
# acc2.withdraw(500)

# Ex3: Student Grade System

class Student:
    def __init__(self, name: str, student_id: int, courses=None):
        self.name = name
        self.student_id = student_id
        self.courses = {} if courses is None else courses
        for course, grade in self.courses.items():
            if grade > 100:
                self.courses[course] = 100
            elif grade < 0:
                self.courses[course] = 0

    def add_course(self, course: str, grade: int = 0) -> None:
        if course in self.courses:
            print('Course already exists')
        elif grade < 0 or grade > 100:
            print('Invalid Grade, must be between 0 and 100')
        else:
            self.courses[course] = grade
            print('Course added successfully')

    def add_grade(self, course: str, grade: int) -> None:
        if course not in self.courses:
            print("Course doesn't exist")
        elif grade < 0 or grade > 100:
            print('Invalid Grade, must be between 0 and 100')
        else:
            self.courses[course] = grade
            print('Grade added successfully')

    def calculate_gpa(self) -> float:
        return sum(self.courses.values()) / len(self.courses) if self.courses else 0

    def display_report_card(self) -> None:
        report = f'Name: {self.name}\nID: {self.student_id}\n\n'
        for course, grade in self.courses.items():
            report += f'{course}: {grade}\n'
        report += f"\nGPA: {self.calculate_gpa()}\n"
        print(report)


# student1 = Student('Nadav', 1, {'DevSecOps': 150})
# student1.display_report_card()
# student2 = Student('Gil', 2)
# student2.display_report_card()
# student1.add_course('DevSecOps')
# student1.add_course('Math', -5)
# student1.add_course('Math', 150)
# student1.add_course('Math', 75)
# student1.display_report_card()
# student2.add_course('English')
# student2.add_grade('English', 80)
# student2.display_report_card()

# Challenge: Server Management System

class Server:
    def __init__(self, hostname: str, ip: str):
        self.hostname = hostname
        self.ip = ip
        self.is_running = False
        self.last_started = None
        # IP validation
        ip = ip.split('.')
        if len(ip) != 4:
            print('Invalid IP address')
        else:
            for byte in ip:
                if not byte.isdigit() or int(byte) > 255:  # negative numbers wouldn't pass the isdigit check
                    print('Invalid IP address')
                    break

    def start(self) -> str:
        start_time = time.time()
        self.is_running = True
        self.last_started = time.ctime(start_time)
        return f'{self.last_started} - Starting server {self.hostname}'

    def stop(self) -> str:
        self.is_running = False
        return f'{time.ctime(time.time())} - Stopping server {self.hostname}'

    def restart(self) -> str:
        self.is_running = False
        start_time = time.time()
        self.is_running = True
        self.last_started = time.ctime(start_time)
        return f'{self.last_started} - Restarting server {self.hostname}'

    def status(self) -> str:
        return (f'{time.ctime(time.time())} - Server {self.hostname} is currently '
                f'{'' if self.is_running else 'not '}running')

    def display(self) -> None:
        print(f'Hostname: {self.hostname}')
        print(f'IP: {self.ip}')
        print(f'Running: {self.is_running}')
        print(f'Last started: {self.last_started}')


# web_server = Server("web-01", "192.168.1.100")
# db_server = Server("db-01", "192.168.1.101")
# # Start servers
# print(web_server.start())  # Should print: "Starting server web-01"
# print(web_server.status())
# print(db_server.status())
#
# # Stopping servers
# print(db_server.stop())    # Should print: "Stopping server db-01"
# db_server.display()
# time.sleep(3)
# db_server.start()
# db_server.display()
# print(web_server.restart())
