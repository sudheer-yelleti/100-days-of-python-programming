import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''
list_of_choices = [rock, paper, scissors]
user_choice = int(input("What do you want to choose? Select 1 for Rock, 2 for Paper, or 3 for Scissors: "))
if user_choice >= 0 and user_choice <= 2:
    print(f"You choose {list_of_choices[user_choice - 1]}")
computer_choice = random.randint(0, 2)
print(f"Computer choose {list_of_choices[computer_choice]}")

if user_choice < 0 or user_choice > 2:
    print("Choose a valid number")
elif user_choice == 0 and computer_choice == 2:
    print("You win!")
elif user_choice == 2 and computer_choice == 0:
    print("You lose!")
elif user_choice == computer_choice:
    print("It's a Draw")
elif user_choice > computer_choice:
    print("You Win")
elif user_choice < computer_choice:
    print("You Lose")
else:
    print("You Lose")
