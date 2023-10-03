def main():
    while True:
        print("Main Menu:")
        print("1. Option 1")
        print("2. Option 2")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            option1()
        elif choice == '2':
            option2()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def option1():
    print("You chose Option 1")

def option2():
    print("You chose Option 2")

if __name__ == "__main__":
    main()