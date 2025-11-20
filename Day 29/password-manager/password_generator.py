import random
from random import shuffle


class PasswordGenerator:
    LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    def __init__(self):
        self.nr_letters = random.randint(8, 10)
        self.nr_symbols = random.randint(2, 4)
        self.nr_numbers = random.randint(2, 4)

    def generate_password(self):
        password_letters = [random.choice(self.LETTERS) for _ in range(self.nr_letters)]
        password_symbols = [random.choice(self.SYMBOLS) for _ in range(self.nr_symbols)]
        password_numbers = [random.choice(self.NUMBERS) for _ in range(self.nr_numbers)]

        password_list = password_letters + password_symbols + password_numbers
        shuffle(password_list)

        return "".join(password_list)
