from coffee_maker import CoffeeMaker
from menu import Menu
from money_machine import MoneyMachine

menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

is_on = True
while is_on:

    menu_items = menu.get_items()
    user_choice = input(f"What would you like? ({menu_items}): ").lower().strip()

    if user_choice == "report":
        coffee_maker.report()
        money_machine.report()
    elif user_choice == "off":
        is_on = False
    else:
        drink = menu.find_drink(user_choice)

        if (drink is None):
            continue
        if coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
            coffee_maker.make_coffee(drink)
