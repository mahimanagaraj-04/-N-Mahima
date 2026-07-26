def calculator():
    while True:
        print("\nSimple Calculator")
        print("1. +")
        print("2. -")
        print("3. *")
        print("4. /")
        print("5. Clear")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "6":
            print("Goodbye!")
            break

        if choice == "5":
            print("Calculator Cleared!")
            continue

        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice!")
            continue

        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))

        if choice == "1":
            print("Result =", a + b)
        elif choice == "2":
            print("Result =", a - b)
        elif choice == "3":
            print("Result =", a * b)
        elif choice == "4":
            if b == 0:
                print("Cannot divide by zero!")
            else:
                print("Result =", a / b)

calculator()
