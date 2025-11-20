import data

profit = 0


def report():
    print(f"Water: {data.resources['water']}ml")
    print(f"Milk: {data.resources['milk']}ml")
    print(f"Coffee: {data.resources['coffee']}g")
    print(f"Money: {profit}$")


def check_resources(drink):
    required_ingredients = drink["ingredients"]

    for item in required_ingredients:
        if data.resources[item] < required_ingredients[item]:
            print(f"Sorry, there's not enough {item}.")
            return False
    return True


def process_coins():
    print("Please insert coins.")
    total = int(input("How many quarters?: ")) * 0.25
    total += int(input("How many dimes?: ")) * 0.1
    total += int(input("How many nickles?: ")) * 0.05
    total += int(input("How many pennies?: ")) * 0.01

    return total


def prepare_order(user_choice):
    drink = data.MENU[user_choice]
    are_resources_enough = check_resources(drink)

    if are_resources_enough:
        order_cost = process_coins()
        cost = drink["cost"]
        if order_cost < cost:
            print("Sorry, that's not enough money. Money refunded..")
            return

        if order_cost > cost:
            refund_money = round(order_cost - cost, 2)
            print(f"Here is ${refund_money} dollars in change.")

        global profit
        profit += cost

        for item, amount in drink["ingredients"].items():
            data.resources[item] -= amount

        print(f"Here is your {user_choice}. Enjoy!")


is_on = True
while is_on:
    user_choice = input("What would you like? (espresso/latte/cappuccino):")
    if user_choice == "report":
        report()
    elif user_choice == "off":
        is_on = False
    elif user_choice in data.MENU:
        prepare_order(user_choice)
    else:
        print("Sorry, that's not a valid option. Please choose espresso/latte/cappuccino")
