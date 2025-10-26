import art


def add(n1, n2):
    return n1 + n2


def subtract(n1, n2):
    return n1 - n2


def multiply(n1, n2):
    return n1 * n2


def divide(n1, n2):
    return n1 / n2


operation = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide
}
should_continue_with_previous = "no"
while True:
    if should_continue_with_previous == "no":
        print(art.logo)
        first_number = int(input("Enter the first number"))
    operation_type = input("Type the operation( '+', '-','*','/' you want to perform")
    second_number = int(input("Enter the second number"))

    result = operation[operation_type](first_number, second_number)
    print(f"{first_number} {operation_type} {second_number} = {result}")

    should_continue_with_previous = input("Do you want to continue with the previous result?")
    if should_continue_with_previous == "yes":
        first_number = result
